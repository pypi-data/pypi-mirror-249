from typing import Dict, List
from pathlib import Path
import json
import os

from PIL import Image, ImageOps
from PIL.PngImagePlugin import PngInfo
from moviepy.editor import ImageSequenceClip
import numpy as np
import torch

from vispunk_motion.custom_nodes.ComfyUI_Advanced_ControlNet.control.nodes import (
    TimestepKeyframeGroup,
    load_controlnet,
)
# from vispunk_motion.custom_nodes.ComfyUI_AnimateDiff_Evolved.animatediff.context import ContextSchedules
from vispunk_motion.custom_nodes.ComfyUI_AnimateDiff_Evolved.animatediff.model_utils import BetaSchedules#, raise_if_not_checkpoint_sd1_5
from vispunk_motion.custom_nodes.ComfyUI_AnimateDiff_Evolved.animatediff.nodes import (
    InjectionParams,
    # InjectorVersion,
    ModelPatcher,
    # calculate_model_hash,
    # ejectors,
    # get_available_models,
    # injected_model_hashs,
    # injectors,
    # load_motion_module,
    logger,
    # motion_modules,
    # set_mm_injected_params,
    # load_torch_file,
    # MotionWrapper,
    # calculate_parameters,
    # model_management,
    get_available_motion_loras,
    MotionLoraList,
    MotionLoraInfo,
)
import vispunk_motion.comfy.sd
import vispunk_motion.folder_paths as folder_paths


class AnimateDiffLoraLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "lora_name": (get_available_motion_loras(),),
                "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.001}),
            },
            "optional": {
                "prev_motion_lora": ("MOTION_LORA",),
            }
        }
    
    RETURN_TYPES = ("MOTION_LORA",)
    CATEGORY = "Animate Diff 🎭🅐🅓"
    FUNCTION = "load_motion_lora"

    def load_motion_lora(self, lora_name: str, strength: float, prev_motion_lora: MotionLoraList=None):
        if prev_motion_lora is None:
            prev_motion_lora = MotionLoraList()
        else:
            prev_motion_lora = prev_motion_lora.clone()
        # check if motion lora with name exists
        lora_path = lora_name
        if not Path(lora_path).is_file():
            raise FileNotFoundError(f"Motion lora with name '{lora_name}' not found.")
        # create motion lora info to be loaded in AnimateDiff Loader
        lora_info = MotionLoraInfo(name=lora_name, strength=strength)
        prev_motion_lora.add_lora(lora_info)

        return (prev_motion_lora,)


class AnimateDiffCombine:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "frame_rate": (
                    "INT",
                    {"default": 8, "min": 1, "max": 24, "step": 1},
                ),
                "loop_count": ("INT", {"default": 0, "min": 0, "max": 100, "step": 1}),
                "save_image": (["Enabled", "Disabled"],),
                "filename_prefix": ("STRING", {"default": "AnimateDiff"}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    CATEGORY = "Animate Diff"
    FUNCTION = "generate_gif"

    def generate_clip(
        self,
        images,
        frame_rate: int,
        loop_count: int,
        save_image="Enabled",
        filename_prefix="AnimateDiff",
        prompt=None,
        extra_pnginfo=None,
        generate_gif=True,
        generate_mp4=False,
    ):
        # convert images to numpy
        pil_images: List[Image.Image] = []
        for image in images:
            img = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
            pil_images.append(img)

        # save image
        output_dir = (
            folder_paths.get_output_directory()
            if save_image == "Enabled"
            else folder_paths.get_temp_directory()
        )
        (
            full_output_folder,
            filename,
            counter,
            subfolder,
            _,
        ) = folder_paths.get_save_image_path(filename_prefix, output_dir)

        metadata = PngInfo()
        if prompt is not None:
            metadata.add_text("prompt", json.dumps(prompt))
        if extra_pnginfo is not None:
            for x in extra_pnginfo:
                metadata.add_text(x, json.dumps(extra_pnginfo[x]))

        # save first frame as png to keep metadata
        # file = f"{filename}_{counter:05}_.png"
        # file_path = os.path.join(full_output_folder, file)
        # pil_images[0].save(
        #     file_path,
        #     pnginfo=metadata,
        #     compress_level=4,
        # )

        # save gif
        if generate_gif:
            file = f"{filename}_{counter:05}_.gif"
            file_path = os.path.join(full_output_folder, file)
            pil_images[0].save(
                file_path,
                save_all=True,
                append_images=pil_images[1:],
                duration=round(1000 / frame_rate),
                loop=loop_count,
                compress_level=4,
            )
            print("Saved gif to", file_path, os.path.exists(file_path))

        # save mp4
        if generate_mp4:
            mp4_file = f"{filename}_{counter:05}_.mp4"
            mp4_file_path = os.path.join(full_output_folder, mp4_file)
            clip = ImageSequenceClip([np.array(i) for i in pil_images], fps=frame_rate)
            clip.write_videofile(mp4_file_path)
            print("Saved mp4 to", mp4_file_path, os.path.exists(mp4_file_path))

        previews = [
            {
                "filename": file,
                "subfolder": subfolder,
                "type": "output" if save_image == "Enabled" else "temp",
            }
        ]
        return {"ui": {"images": previews}}


class CheckpointLoaderSimple:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "ckpt_name": (folder_paths.get_filename_list("checkpoints"), ),
                             }}
    RETURN_TYPES = ("MODEL", "CLIP", "VAE")
    FUNCTION = "load_checkpoint"

    CATEGORY = "loaders"

    def load_checkpoint_from_path(self, ckpt_path, output_vae=True, output_clip=True):
        out = vispunk_motion.comfy.sd.load_checkpoint_guess_config(
            ckpt_path,
            output_vae=output_vae,
            output_clip=output_clip,
            embedding_directory=folder_paths.get_folder_paths("embeddings"),
        )
        return out[:3]


class CheckpointLoaderSimpleWithNoiseSelect:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ckpt_name": (folder_paths.get_filename_list("checkpoints"), ),
                "beta_schedule": (BetaSchedules.ALIAS_LIST, )
            },
        }
    RETURN_TYPES = ("MODEL", "CLIP", "VAE")
    FUNCTION = "load_checkpoint"

    CATEGORY = "Animate Diff"

    def load_checkpoint(self, ckpt_path, beta_schedule, output_vae=True, output_clip=True):
        out = vispunk_motion.comfy.sd.load_checkpoint_guess_config(ckpt_path, output_vae=output_vae, output_clip=output_clip, embedding_directory=folder_paths.get_folder_paths("embeddings"))
        # register chosen beta schedule on model - convert to beta_schedule name recognized by ComfyUI
        beta_schedule_name = BetaSchedules.to_name(beta_schedule)
        out[0].model.register_schedule(given_betas=None, beta_schedule=beta_schedule_name, timesteps=1000, linear_start=0.00085, linear_end=0.012, cosine_s=8e-3)
        return out


class VAELoader:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "vae_name": (folder_paths.get_filename_list("vae"), )}}
    RETURN_TYPES = ("VAE",)
    FUNCTION = "load_vae"

    CATEGORY = "loaders"

    #TODO: scale factor?
    def load_vae(self, vae_path):
        sd = vispunk_motion.comfy.utils.load_torch_file(vae_path)
        vae = vispunk_motion.comfy.sd.VAE(sd=sd)
        return (vae,)


def load_motion_module(model_path: str):
    model_name = model_path.split("/")[-1]
    logger.info(f"Loading motion module {model_name}")
    mm_state_dict = load_torch_file(model_path)
    motion_module = MotionWrapper(mm_state_dict=mm_state_dict, mm_type=model_name)

    parameters = calculate_parameters(mm_state_dict, "")
    usefp16 = model_management.should_use_fp16(model_params=parameters)
    if usefp16:
        logger.info("Using fp16, converting motion module to fp16")
        motion_module.half()
    offload_device = model_management.unet_offload_device()
    motion_module = motion_module.to(offload_device)
    motion_module.load_state_dict(mm_state_dict)

    return motion_module


class AnimateDiffLoader:
    def __init__(self) -> None:
        self.version = InjectorVersion.V1_V2

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "latents": ("LATENT",),
                "model_name": (get_available_models(),),
                "unlimited_area_hack": ([False, True],),
            },
        }

    @classmethod
    def IS_CHANGED(s, model: ModelPatcher, _):
        unet = model.model.diffusion_model
        return calculate_model_hash(unet) not in injected_model_hashs

    RETURN_TYPES = ("MODEL", "LATENT")
    CATEGORY = "Animate Diff"
    FUNCTION = "inject_motion_modules"

    def inject_motion_modules(
        self,
        model: ModelPatcher,
        latents: Dict[str, torch.Tensor],
        model_name: str,
        unlimited_area_hack: bool,
    ):
        if model_name not in motion_modules:
            motion_modules[model_name] = load_motion_module(model_name)

        motion_module = motion_modules[model_name]
        # check that latents don't exceed max frame size
        init_frames_len = len(latents["samples"])
        init_frames_len = 16
        if init_frames_len > motion_module.encoding_max_len:
            # TODO: warning and cutoff frames instead of error
            raise ValueError(f"AnimateDiff model {model_name} has upper limit of {motion_module.encoding_max_len} frames, but received {init_frames_len} latents.")
        # set motion_module's video_length to match latent length
        motion_module.set_video_length(init_frames_len)

        model = model.clone()
        unet = model.model.diffusion_model
        unet_hash = calculate_model_hash(unet)
        need_inject = unet_hash not in injected_model_hashs

        injection_params = InjectionParams(
            video_length=init_frames_len,
            unlimited_area_hack=unlimited_area_hack,
        )

        if unet_hash in injected_model_hashs:
            (mm_type, version) = injected_model_hashs[unet_hash]
            if version != self.version or mm_type != motion_module.mm_type:
                # injected by another motion module, unload first
                logger.info(f"Ejecting motion module {mm_type} version {version} - {motion_module.version}.")
                ejectors[version](unet)
                need_inject = True
            else:
                logger.info(f"Motion module already injected, only injecting params.")
                set_mm_injected_params(model, injection_params)

        if need_inject:
            logger.info(f"Injecting motion module {model_name} version {motion_module.version}.")
            
            injectors[self.version](unet, motion_module, injection_params)
            unet_hash = calculate_model_hash(unet)
            injected_model_hashs[unet_hash] = (motion_module.mm_type, self.version)

        return (model, latents)


class AnimateDiffLoaderAdvanced:
    def __init__(self) -> None:
        self.version = InjectorVersion.V1_V2

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "latents": ("LATENT",),
                "model_name": (get_available_models(),),
                "unlimited_area_hack": ("BOOLEAN", {"default": False},),
                "context_length": ("INT", {"default": 16, "min": 0, "max": 1000}),
                "context_stride": ("INT", {"default": 1, "min": 1, "max": 1000}),
                "context_overlap": ("INT", {"default": 4, "min": 0, "max": 1000}),
                "context_schedule": (ContextSchedules.CONTEXT_SCHEDULE_LIST,),
                "closed_loop": ("BOOLEAN", {"default": False},),
            },
        }

    @classmethod
    def IS_CHANGED(s, model: ModelPatcher, _):
        unet = model.model.diffusion_model
        return calculate_model_hash(unet) not in injected_model_hashs

    RETURN_TYPES = ("MODEL", "LATENT")
    CATEGORY = "Animate Diff"
    FUNCTION = "inject_motion_modules"

    def inject_motion_modules(
        self,
        model: ModelPatcher,
        latents: Dict[str, torch.Tensor],
        model_name: str,
        unlimited_area_hack: bool,
        context_length: int,
        context_stride: int,
        context_overlap: int,
        context_schedule: str,
        closed_loop: bool
    ):
        raise_if_not_checkpoint_sd1_5(model)

        if model_name not in motion_modules:
            motion_modules[model_name] = load_motion_module(model_name)

        motion_module = motion_modules[model_name]
        
        init_frames_len = len(latents["samples"])
        # if latents exceed context_length, use sliding window
        if init_frames_len > context_length and context_length > 0:
            logger.info("Criteria for sliding context met.")
            # check that context_length don't exceed max frame size
            if context_length > motion_module.encoding_max_len:
                raise ValueError(f"AnimateDiff model {model_name} has upper limit of {motion_module.encoding_max_len} frames, but received context frames of {context_length} latents.")
            # set motion_module's video_length to match context length
            motion_module.set_video_length(context_length)
            injection_params = InjectionParams.init_with_context(
                video_length=init_frames_len,
                unlimited_area_hack=unlimited_area_hack,
                context_frames=context_length,
                context_stride=context_stride,
                context_overlap=context_overlap,
                context_schedule=context_schedule,
                closed_loop=closed_loop
            )
        # otherwise, do normal AnimateDiff operation
        else:
            logger.info("Criteria for sliding context not met - will do full-latent sampling.")
            if init_frames_len > motion_module.encoding_max_len:
                # TODO: warning and cutoff frames instead of error
                raise ValueError(f"AnimateDiff model {model_name} has upper limit of {motion_module.encoding_max_len} frames, but received {init_frames_len} latents.")
            # set motion_module's video_length to match latent amount
            motion_module.set_video_length(init_frames_len)
            injection_params = InjectionParams(
                video_length=init_frames_len,
                unlimited_area_hack=unlimited_area_hack,
            )

        model = model.clone()
        unet = model.model.diffusion_model
        unet_hash = calculate_model_hash(unet)
        need_inject = unet_hash not in injected_model_hashs

        if unet_hash in injected_model_hashs:
            (mm_type, version) = injected_model_hashs[unet_hash]
            if version != self.version or mm_type != motion_module.mm_type:
                # injected by another motion module, unload first
                logger.info(f"Ejecting motion module {mm_type} version {version} - {motion_module.version}.")
                ejectors[version](unet)
                need_inject = True
            else:
                logger.info(f"Motion module already injected, only injecting params.")
                set_mm_injected_params(model, injection_params)

        if need_inject:
            logger.info(f"Injecting motion module {model_name} version {motion_module.version}.")
            
            injectors[self.version](unet, motion_module, injection_params)
            unet_hash = calculate_model_hash(unet)
            injected_model_hashs[unet_hash] = (motion_module.mm_type, self.version)

        return (model, latents)


class ControlNetLoaderAdvanced:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "control_net_name": (folder_paths.get_filename_list("controlnet"), ),
            },
            "optional": {
                "timestep_keyframe": ("TIMESTEP_KEYFRAME", ),
            }
        }
    
    RETURN_TYPES = ("CONTROL_NET", )
    FUNCTION = "load_controlnet"

    CATEGORY = "adv-controlnet/loaders"

    def load_controlnet(self, control_net_path, timestep_keyframe: TimestepKeyframeGroup=None):
        print(control_net_path)
        controlnet = load_controlnet(control_net_path, timestep_keyframe)
        return (controlnet,)


class LoadPILImage:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {"required":
                    {"image": (sorted(files), {"image_upload": True})},
                }

    CATEGORY = "image"

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "load_image"
    def load_image(self, pil_image: Image.Image):
        i = ImageOps.exif_transpose(pil_image)
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        if 'A' in i.getbands():
            mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
            mask = 1. - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
        return (image, mask)


def Fourier_filter(x, threshold, scale):
    # FFT
    x_freq = torch.fft.fftn(x.float(), dim=(-2, -1))
    x_freq = torch.fft.fftshift(x_freq, dim=(-2, -1))

    B, C, H, W = x_freq.shape
    mask = torch.ones((B, C, H, W), device=x.device)

    crow, ccol = H // 2, W //2
    mask[..., crow - threshold:crow + threshold, ccol - threshold:ccol + threshold] = scale
    x_freq = x_freq * mask

    # IFFT
    x_freq = torch.fft.ifftshift(x_freq, dim=(-2, -1))
    x_filtered = torch.fft.ifftn(x_freq, dim=(-2, -1)).real

    return x_filtered.to(x.dtype)


class FreeU:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "model": ("MODEL",),
                             "b1": ("FLOAT", {"default": 1.1, "min": 0.0, "max": 10.0, "step": 0.01}),
                             "b2": ("FLOAT", {"default": 1.2, "min": 0.0, "max": 10.0, "step": 0.01}),
                             "s1": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 10.0, "step": 0.01}),
                             "s2": ("FLOAT", {"default": 0.2, "min": 0.0, "max": 10.0, "step": 0.01}),
                              }}
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "patch"

    CATEGORY = "_for_testing"

    def patch(self, model, b1=1.1, b2=1.2, s1=0.9, s2=0.2):
        model_channels = model.model.model_config.unet_config["model_channels"]
        scale_dict = {model_channels * 4: (b1, s1), model_channels * 2: (b2, s2)}
        def output_block_patch(h, hsp, transformer_options):
            scale = scale_dict.get(h.shape[1], None)
            if scale is not None:
                h[:,:h.shape[1] // 2] = h[:,:h.shape[1] // 2] * scale[0]
                hsp = Fourier_filter(hsp, threshold=1, scale=scale[1])
            return h, hsp

        m = model.clone()
        m.set_model_output_block_patch(output_block_patch)
        return (m, )
