from controlnet_aux import HEDdetector
from diffusers import (
    EulerDiscreteScheduler,
    StableDiffusionXLPipeline,
    StableDiffusionXLImg2ImgPipeline,
    StableDiffusionXLInpaintPipeline,
)
from diffusers.models import AutoencoderKL
from diffusers.pipelines.controlnet.multicontrolnet import MultiControlNetModel
import torch

from utils.config import settings


# SDXL_PIPE = StableDiffusionXLPipeline.from_pretrained(
#     "stabilityai/stable-diffusion-xl-base-1.0",
#     torch_dtype=torch.float16, use_safetensors=True,
#     variant="fp16", safety_checker=None,
#     vae=AutoencoderKL.from_pretrained(
#         "madebyollin/sdxl-vae-fp16-fix",
#         torch_dtype=torch.float16,
#         cache_dir=settings.MODELS_FOLDER,
#     ),
#     cache_dir=settings.MODELS_FOLDER,
# )

INPAINT_PIPE = StableDiffusionXLInpaintPipeline.from_pretrained(
    "diffusers/stable-diffusion-xl-1.0-inpainting-0.1",
    torch_dtype=torch.float16,
    variant="fp16",
    cache_dir="/drive3/models",
)