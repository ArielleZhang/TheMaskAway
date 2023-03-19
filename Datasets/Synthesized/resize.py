from PIL import Image
import os, sys
import argparse


parser = argparse.ArgumentParser(
    description="Resize image"
)

parser.add_argument(
    "--path",
    type=str,
    default="E:/1-EngSci3/1-ECE324/Triple-Dots/Mask_Data/Images_masked_N95",
    help="Path to either the folder containing images or the image itself",
)

parser.add_argument(
    "--size",
    type=int,
    default=256,
    help="Height and width of the image",
)

args = parser.parse_args()

size = (args.size, args.size)


for root, dirs, files in os.walk(args.path):
    for idx, file in enumerate(files):

        if idx % 100 == 0:
            print("Processing", idx/len(files)*100, "done" )
        img = Image.open(args.path + "/" + file)
        
        img_resize = img.resize(size)
        os.makedirs(args.path + "/resized", exist_ok=True)
        img_resize.save(args.path + "/resized/" + file)
        
        img_resize_lanczos = img.resize((256, 256), Image.LANCZOS)
        os.makedirs(args.path + "/lanczos", exist_ok=True)
        img_resize_lanczos.save(args.path + "/lanczos/" + file)
    