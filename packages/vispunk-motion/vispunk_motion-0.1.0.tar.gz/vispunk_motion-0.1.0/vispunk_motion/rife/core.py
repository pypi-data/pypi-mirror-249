from queue import Queue
from typing import List
import _thread

from PIL import Image
from torch.nn import functional as F
import torch
import numpy as np

from vispunk_motion.utils.config import settings
from vispunk_motion.rife.model.pytorch_msssim import ssim_matlab
from vispunk_motion.rife.train_log.RIFE_HDv3 import Model


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.set_grad_enabled(False)
if torch.cuda.is_available():
    torch.backends.cudnn.enabled = True
    torch.backends.cudnn.benchmark = True


model = Model()
model.load_model(settings.RIFE_MODEL_FOLDER, -1)
print("Loaded v3.x HD model.")

model.eval()
model.device()


def interpolate_frames_t(source_frames: torch.Tensor, exp: int = 1, fp16 = False) -> List[Image.Image]:
    source_frames_arr = [255.0 * f.cpu().numpy() for f in source_frames]
    return [Image.fromarray(np.clip(f, 0, 255).astype(np.uint8)) for f in interpolate_frames_arr(source_frames_arr, exp, fp16)]


def interpolate_frames_im(source_frames: List[Image.Image], exp: int = 1, fp16 = False) -> List[Image.Image]:
    frames_arr = interpolate_frames_arr(
        [np.array(f) for f in source_frames],
        exp,
        fp16,
    )
    return [Image.fromarray(f) for f in frames_arr]


def interpolate_frames_arr(source_frames: List[np.ndarray], exp: int = 1, fp16 = False) -> List[np.ndarray]:

    lastframe = source_frames[0]
    h, w, _ = lastframe.shape

    final_frames = []


    def clear_write_buffer(write_buffer):
        while True:
            item = write_buffer.get()
            if item is None:
                break
            final_frames.append(item)

    def build_read_buffer(read_buffer, videogen):
        try:
            for frame in videogen:
                read_buffer.put(frame)
        except:
            pass
        read_buffer.put(None)

    def make_inference(I0, I1, n):
        global model
        middle = model.inference(I0, I1, scale=1.0)
        if n == 1:
            return [middle]
        first_half = make_inference(I0, middle, n=n//2)
        second_half = make_inference(middle, I1, n=n//2)
        if n%2:
            return [*first_half, middle, *second_half]
        else:
            return [*first_half, *second_half]

    def pad_image(img):
        if fp16:
            return F.pad(img, padding).half()
        else:
            return F.pad(img, padding)

    tmp = 32
    ph = ((h - 1) // tmp + 1) * tmp
    pw = ((w - 1) // tmp + 1) * tmp
    padding = (0, pw - w, 0, ph - h)
    write_buffer = Queue(maxsize=500)
    read_buffer = Queue(maxsize=500)
    _thread.start_new_thread(build_read_buffer, (read_buffer, source_frames))
    _thread.start_new_thread(clear_write_buffer, (write_buffer,))

    I1 = torch.from_numpy(np.transpose(lastframe, (2,0,1))).to(device, non_blocking=True).unsqueeze(0).float() / 255.
    I1 = pad_image(I1)
    temp = None # save lastframe when processing static frame

    while True:
        if temp is not None:
            frame = temp
            temp = None
        else:
            frame = read_buffer.get()
        if frame is None:
            break
        I0 = I1
        I1 = torch.from_numpy(np.transpose(frame, (2,0,1))).to(device, non_blocking=True).unsqueeze(0).float() / 255.
        I1 = pad_image(I1)
        I0_small = F.interpolate(I0, (32, 32), mode='bilinear', align_corners=False)
        I1_small = F.interpolate(I1, (32, 32), mode='bilinear', align_corners=False)
        ssim = ssim_matlab(I0_small[:, :3], I1_small[:, :3])

        break_flag = False
        if ssim > 0.996:        
            frame = read_buffer.get() # read a new frame
            if frame is None:
                break_flag = True
                frame = lastframe
            else:
                temp = frame
            I1 = torch.from_numpy(np.transpose(frame, (2,0,1))).to(device, non_blocking=True).unsqueeze(0).float() / 255.
            I1 = pad_image(I1)
            I1 = model.inference(I0, I1, scale=1)
            I1_small = F.interpolate(I1, (32, 32), mode='bilinear', align_corners=False)
            ssim = ssim_matlab(I0_small[:, :3], I1_small[:, :3])
            frame = (I1[0] * 255).byte().cpu().numpy().transpose(1, 2, 0)[:h, :w]
        
        if ssim < 0.2:
            output = []
            for i in range((2 ** exp) - 1):
                output.append(I0)
        else:
            output = make_inference(I0, I1, 2**exp-1)

        write_buffer.put(lastframe)
        for mid in output:
            mid = (((mid[0] * 255.).byte().cpu().numpy().transpose(1, 2, 0)))
            write_buffer.put(mid[:h, :w])
        lastframe = frame
        if break_flag:
            break

    write_buffer.put(lastframe)

    return final_frames
