from django.apps import AppConfig
from django.conf import settings
from pathlib import Path
import torch

from .vit.ViT import VisionTransformer
from .vit.baseline import Model

class RoadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'road'

    device = "cuda" if torch.cuda.is_available() else "cpu"
    # model = torch.load(settings.MODELS.joinpath('AI4VN_ViT_model_final.pth')).to(device).eval()
    extractor = VisionTransformer(version='ViT-B_16', pretrained=None)
    model = Model(extractor = extractor, nclasses=8).to(device)
    pretrained = torch.load(settings.MODELS.joinpath('AI4VN_ViT_model_final.pth'))
    model.load_state_dict(pretrained['model_state_dict']).to(device).eval()

    path = settings.BASE_DIR