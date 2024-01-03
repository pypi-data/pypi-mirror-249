from typing import List, Optional

from PIL import Image, ImageOps
import numpy as np
import torch

from ..nodes import (
    EmptyLatentImage,
    LatentComposite,
    LoadImage,
    VAEEncode,
)


class Latent:
    def __init__(self, size = (512, 512), num_frames = 16):
        self.size = size
        self.num_frames = num_frames

    def encode(self, *args, **kwargs):
        (empty_latent,) = EmptyLatentImage().generate(*self.size, self.num_frames)
        return empty_latent


class EmptyLatent(Latent):
    pass


class ConstantLatent(Latent):
    def __init__(
        self,
        latent,
        size = (512, 512),
        denoise: float = 0.8,
        num_frames = 16,
        vae = None,
    ):
        Latent.__init__(self, size, num_frames)
        self.latent = latent
        self.denoise = denoise
        self.vae = vae

    def encode(self, animator, *args, **kwargs):
        latent = Latent.encode(self)
        (latent,) = LatentComposite().composite(
            latent,
            self.latent,
            x=0, y=0,
        )
        return latent


class ConstantImageLatent(Latent):
    def __init__(
        self,
        image_path: Optional[str] = None,
        image: Optional[Image.Image] = None,
        size = (512, 512),
        denoise: float = 0.8,
        num_frames = 16,
        vae = None,
    ):
        Latent.__init__(self, size, num_frames)
        self.image_path = image_path
        self.image = image
        self.denoise = denoise
        self.vae = vae

    def load_pil_image(self, image: Image.Image):
        i = ImageOps.exif_transpose(image)
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        if 'A' in i.getbands():
            mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
            mask = 1. - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
        return (image, mask)

    def encode(self, animator, *args, **kwargs):
        latent = Latent.encode(self)
        if self.image_path:
            image, _ = LoadImage().load_image(self.image_path)
        elif self.image:
            image, _ = self.load_pil_image(self.image)
        (image_latent,) = VAEEncode().encode(
            self.vae or animator.vae,
            image,
        )
        (latent,) = LatentComposite().composite(
            latent,
            image_latent,
            x=0, y=0,
        )
        return latent

class InterpolatedImageLatent(Latent):
    def __init__(
        self,
        image_paths: List[str] = [],
        images: List[Image.Image] = [],
        denoise: float = 0.8,
        size = (512, 512),
        num_frames = 16,
        vae = None,
    ):
        Latent.__init__(self, size, num_frames)
        self.image_paths = image_paths
        self.images = images
        self.denoise = denoise
        self.vae = vae

    def encode(self, animator, *args, **kwargs):
        image_latents = []
        if len(self.image_paths):
            for path in self.image_paths:
                latent_encoder = ConstantImageLatent(
                    path,
                    size=self.size,
                    num_frames=self.num_frames,
                    vae=self.vae,
                )
                image_latents.append(latent_encoder.encode(animator))
        elif len(self.images):
            for image in self.images:
                latent_encoder = ConstantImageLatent(
                    image=image,
                    size=self.size,
                    num_frames=self.num_frames,
                    vae=self.vae,
                )
                image_latents.append(latent_encoder.encode(animator))

        remaining_steps = self.num_frames - 1
        interpolated_latents = [image_latents[0]["samples"][0]]
        num_interpolations = len(image_latents[:-1])
        for i, latent_1, latent_2 in zip(range(num_interpolations), image_latents[:-1], image_latents[1:]):
            num_steps = int(np.round(remaining_steps / (num_interpolations - i)))
            for step in range(1, num_steps + 1):
                interpolated_latents.append((1 - step / num_steps) * latent_1["samples"][0] + (step / num_steps) * latent_2["samples"][0])
            remaining_steps -= num_steps
        return { "samples": torch.stack(interpolated_latents) }
