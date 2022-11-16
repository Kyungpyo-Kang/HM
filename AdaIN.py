from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms
from torchvision.utils import make_grid
from types import FunctionType
from typing import Any, BinaryIO, List, Optional, Tuple, Union
import net
import numpy as np
from function import adaptive_instance_normalization, coral
from urllib.request import urlopen


def _log_api_usage_once(obj: Any) -> None:

 
    module = obj.__module__
    if not module.startswith("torchvision"):
        module = f"torchvision.internal.{module}"
    name = obj.__class__.__name__
    if isinstance(obj, FunctionType):
        name = obj.__name__
    torch._C._log_api_usage_once(f"{module}.{name}")

def to_image(
    tensor: Union[torch.Tensor, List[torch.Tensor]],
    format: Optional[str] = None,
    **kwargs,
) -> None:
    

    if not torch.jit.is_scripting() and not torch.jit.is_tracing():
        _log_api_usage_once(to_image)
    grid = make_grid(tensor, **kwargs)
    # Add 0.5 after unnormalizing to [0, 255] to round to nearest integer
    ndarr = grid.mul(255).add_(0.5).clamp_(0, 255).permute(1, 2, 0).to("cpu", torch.uint8).numpy()
    im = Image.fromarray(ndarr)
    
    return im



def test_transform(size, crop):
    transform_list = []
    if size != 0:
        transform_list.append(transforms.Resize(size))
    if crop:
        transform_list.append(transforms.CenterCrop(size))
    transform_list.append(transforms.ToTensor())
    transform = transforms.Compose(transform_list)
    return transform


def style_transfer(vgg, decoder, content, style, alpha=1.0,
                   interpolation_weights=None):
    assert (0.0 <= alpha <= 1.0)
    content_f = vgg(content)
    style_f = vgg(style)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if interpolation_weights:
        _, C, H, W = content_f.size()
        feat = torch.FloatTensor(1, C, H, W).zero_().to(device)
        base_feat = adaptive_instance_normalization(content_f, style_f)
        for i, w in enumerate(interpolation_weights):
            feat = feat + w * base_feat[i:i + 1]
        content_f = content_f[0:1]
    else:
        feat = adaptive_instance_normalization(content_f, style_f)
    feat = feat * alpha + content_f * (1 - alpha)
    return decoder(feat)


def main(vgg_path, decoder_path, content, style, alpha=1.0, interpolation_weights=None, preserve_color = True):


    do_interpolation = False

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    
    decoder = net.decoder
    vgg = net.vgg

    decoder.eval()
    vgg.eval()

    decoder.load_state_dict(torch.load(decoder_path))
    vgg.load_state_dict(torch.load(vgg_path))
    vgg = nn.Sequential(*list(vgg.children())[:31])

    vgg.to(device)
    decoder.to(device)

    content_tf = test_transform(512, True)
    style_tf = test_transform(512, True)
    
    
    try : 
        content_image = Image.open(content)
    except : 
        content_image = Image.open(urlopen(content)) # url형태로 받는 경우 urlopen을 이용해 이미지 로드
    
    try : 
        style_image = Image.open(style)
    except : 
        style_image = Image.open(urlopen(style))

    content = content_tf(content_image)
    style = style_tf(style_image)

    if preserve_color:
        style = coral(style, content)

    style = style.to(device).unsqueeze(0)
    content = content.to(device).unsqueeze(0)

    with torch.no_grad():
        output = style_transfer(vgg, decoder, content, style, alpha)

    output = output.cpu()


    result_output = to_image(output)
    output = {'content_image':content_image,'style_image':style_image, 'output_image':result_output}

    return output

