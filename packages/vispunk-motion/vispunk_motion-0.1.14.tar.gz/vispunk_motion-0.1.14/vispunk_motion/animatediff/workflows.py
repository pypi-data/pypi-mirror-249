from typing import List

from PIL import Image
import numpy as np

from .core import BaseAnimator
from .latents import EmptyLatent
from . import controls
from ..rife.core import interpolate_frames_im


def interpolate(
    animator: BaseAnimator,
    image_1: Image,
    image_2: Image,
    prompt: str = "",
    num_frames: int = 16,
) -> List[Image.Image]:
    controlnet_path = "/drive3/ComfyUI/models/controlnet/control_v11f1e_sd15_tile.pth"
    # controlnet_path = "/drive3/ComfyUI/models/controlnet/refnet.ckpt"

    conditions = [
        controls.Prompt(prompt, "(worst quality, low quality: 1.4)"),
        controls.ControlCondition(
            controlnet_path,
            control_image=image_1,
            keyframes=[
                { "frame":  i, "strength": max(0.05, 1.0 - i * 0.1) } for i in range(16)
            ],
        ),
        controls.ControlCondition(
            controlnet_path,
            control_image=image_2,
            keyframes=[
                { "frame":  num_frames-1-i, "strength": max(0.05, 1.0 - i * 0.1) } for i in range(16)
            ],
        ),
    ]
    condition = controls.ConditioningStack(conditions)

    latents = EmptyLatent(num_frames=num_frames)

    frames_t, _ = animator.sample(
        latents,
        condition,
        cfg=8.0,
        steps=20,
        sampler_name="euler_ad",
        # seed=seed,
        # loop=loop,
    )

    frames: List[Image.Image] = []
    for frame in frames_t:
        img = 255.0 * frame.cpu().numpy()
        img = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
        frames.append(img)
    return interpolate_frames_im(frames, exp=2)
