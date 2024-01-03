from pydantic import BaseSettings


class Settings(BaseSettings):
    DEV: bool = False

    # Video models
    TILE_CONTROLNET: str = "./models/control_v11f1e_sd15_tile.pth"
    AD_SD_CHECKPOINT: str = "./models/photon_v1.safetensors"
    AD_VAE_CHECKPOINT: str = "./models/vae-ft-mse-840000-ema-pruned.safetensors"
    AD_MM_CHECKPOINT: str = "./models/mm_sd_v15_v2.ckpt"
    RIFE_MODEL_FOLDER: str = "./models/rife"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
