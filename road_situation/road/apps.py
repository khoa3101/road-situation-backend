from django.apps import AppConfig
from django.conf import settings
from pathlib import Path
import torch




class RoadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'road'

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = torch.load(settings.MODELS.joinpath('AI4VN_ViT_model_final.pth')).to(device).eval()

    path = settings.BASE_DIR