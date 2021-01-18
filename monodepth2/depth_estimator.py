from __future__ import absolute_import, division, print_function

import os
import sys
import glob
import argparse
import numpy as np
import PIL.Image as pil

import torch
from torchvision import transforms, datasets

import monodepth2.networks as networks
from monodepth2.layers import disp_to_depth
from monodepth2.utils import download_model_if_doesnt_exist
model = "mono_640x192"
download_model_if_doesnt_exist("mono_640x192")
model_path = os.path.join("models", "mono_640x192")
print("-> Loading model from ", model_path)
encoder_path = os.path.join(model_path, "encoder.pth")
depth_decoder_path = os.path.join(model_path, "depth.pth")

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

# LOADING PRETRAINED MODEL
print("   Loading pretrained encoder")
encoder = networks.ResnetEncoder(18, False)
loaded_dict_enc = torch.load(encoder_path, map_location=device)

# extract the height and width of image that this model was trained with
feed_height = loaded_dict_enc['height']
feed_width = loaded_dict_enc['width']
filtered_dict_enc = {k: v for k, v in loaded_dict_enc.items() if k in encoder.state_dict()}
encoder.load_state_dict(filtered_dict_enc)
encoder.to(device)
encoder.eval()

print("   Loading pretrained decoder")
depth_decoder = networks.DepthDecoder(
    num_ch_enc=encoder.num_ch_enc, scales=range(4))

loaded_dict = torch.load(depth_decoder_path, map_location=device)
depth_decoder.load_state_dict(loaded_dict)

depth_decoder.to(device)
depth_decoder.eval()
print("finished preprocessing!")

def put_depths_in_dict(input_image):
    

    original_width, original_height = input_image.size
    input_image = input_image.resize((feed_width, feed_height), pil.LANCZOS)
    input_image = transforms.ToTensor()(input_image).unsqueeze(0)

    # PREDICTION
    input_image = input_image.to(device)
    features = encoder(input_image)
    
    outputs = depth_decoder(features)

    output_tensor = outputs[("disp", 0)]
    depth_mat = output_tensor.detach().cpu().numpy()[0][0]

    return np.mean(depth_mat), np.unravel_index(depth_mat.argmax(), depth_mat.shape)
"""
try:
    input_image = pil.open("/Users/kushagrapandey/HackDavis2021/monodepth2/assets/test_image.jpg").convert('RGB')
    print(put_depths_in_dict(input_image))
except:
    pass
"""