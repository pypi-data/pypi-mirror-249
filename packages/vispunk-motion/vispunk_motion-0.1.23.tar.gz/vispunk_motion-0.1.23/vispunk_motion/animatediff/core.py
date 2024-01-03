from typing import Optional
import random

import torch

from ..custom_nodes.ComfyUI_AnimateDiff_Evolved.animatediff.nodes import (
    AnimateDiffLoaderWithContext,
)
from ..custom_nodes.custom.nodes import (
    CheckpointLoaderSimple,
    VAELoader,
    AnimateDiffLoraLoader,
)
from ..nodes import (
    # CheckpointLoaderSimple,
    CLIPSetLastLayer,
    KSampler,
    VAEDecode,
    VAEDecodeTiled,
    # VAELoader,
)


class MotionLoRA:
    def __init__(
        self,
        motion_lora_path: str = "v2_lora_ZoomIn.ckpt"
    ):
        (self.motion_lora,) = AnimateDiffLoraLoader().load_motion_lora(
            motion_lora_path,
            1.0,
        )


class BaseAnimator:
    def __init__(
        self,
        sd_checkpoint: str = "realisticVisionV51_v51VAE.safetensors",
        vae: str = "vae-ft-mse-840000-ema-pruned.safetensors",
        motion_module_path: str = "mm_sd_v15_v2.ckpt",
    ):
        self.motion_module_path = motion_module_path
        
        model, clip, _ = CheckpointLoaderSimple().load_checkpoint_from_path(
            sd_checkpoint,
        )
        # (model,) = FreeU().patch(model)
        # (clip,) = CLIPSetLastLayer().set_last_layer(clip, -1)
        (vae,) = VAELoader().load_vae(vae)
        self.model = model
        self.clip = clip
        self.vae = vae
        self.DEV = True
    
    def sample(
        self,
        latents,
        conditions,
        seed:Optional[int]=None,
        steps=20,
        cfg=8.0,
        sampler_name="euler",
        scheduler="normal",
        motion_lora=None,
    ):
        (animatediff_model,) = AnimateDiffLoaderWithContext().load_mm_and_inject_params(
            self.model,
            self.motion_module_path,
            beta_schedule="sqrt_linear (AnimateDiff)",
            motion_lora=motion_lora,
        )
        positive, negative = conditions.encode(self)
        (latents,) = KSampler().sample(
            animatediff_model,
            seed=(random.randint(0, 0xffffffffffffffff) if seed is None else seed),
            steps=steps,
            cfg=cfg,
            sampler_name=sampler_name,
            scheduler=scheduler,
            positive=positive,
            negative=negative,
            latent_image=latents.encode(self),
            denoise=latents.denoise if hasattr(latents, "denoise") else 1.0,
        )
        
        # Trim first and last 4 frames due to looping
        latents = { "samples": latents["samples"][2:-2] }
        
        # Decode every other sample and use RIFE to interpolate
        # latents = { "samples": torch.stack([l for i, l in enumerate(latents["samples"]) if i % 2 == 0]) }

        if self.DEV:
            (images,) = VAEDecodeTiled().decode(self.vae, latents, 512)
        else:
            (images,) = VAEDecode().decode(self.vae, latents)
        return images, latents
