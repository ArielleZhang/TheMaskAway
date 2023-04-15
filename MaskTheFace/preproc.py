from PIL import Image
import os, sys
import argparse
from PIL import ExifTags

parser = argparse.ArgumentParser(
    description="Preprocess the images"
)

parser.add_argument(
    "--input",
    type=str,
    default="E:/1-EngSci3/1-ECE324/Triple-Dots/Datasets/faces/validation/masks",
    help="Path to the folder containing images",
)

parser.add_argument(
    "--mask_dir",
    type=str,
    default="E:/1-EngSci3/1-ECE324/Triple-Dots/Datasets/faces/Validation/masks",
    help="Path to the mask dir"
)

parser.add_argument(
    "--size",
    type=int,
    default=512,
    help="Height and width of the image",
)

parser.add_argument(
    "--resize",
    action="store_true",
    help="Resize the images"
)

parser.add_argument(
    "--compare_dir",
    action="store_true",
    help="Compare and remove non exisitng images from original img dir"
)

parser.add_argument(
    "--convert",
    action='store_true',
    help="Convert all input images to png"

)

parser.add_argument(
    "--crop",
    action='store_true',
    help="Crop the images to the center"
)

args = parser.parse_args()

if args.crop:

    for root, dirs, files in os.walk(args.mask_dir):
        for idx, file in enumerate(files):

            if idx % 100 == 0:
                print("Processing", idx/len(files)*100, "done" )
                
            image = Image.open(args.mask_dir + "/" + file)
            image = image.resize((args.size+80,args.size+80))

            # Crop the image to a square aspect ratio
            width, height = image.size
            left = 40
            top = 55
            right = width - 40
            bottom = height - 25
            cropped = image.crop((left, top, right, bottom))
            os.makedirs(args.mask_dir + "/cropped", exist_ok=True)
            cropped.save(args.mask_dir + "/cropped/" + file)

if args.resize:

    size = (args.size, args.size)

    for root, dirs, files in os.walk(args.input):
        for idx, file in enumerate(files):

            if idx % 100 == 0:
                print("Processing", idx/len(files)*100, "done" )
                
            img = Image.open(args.input + "/" + file)
            img_resize_lanczos = img.resize(size, Image.LANCZOS)
            os.makedirs(args.input + "/resized", exist_ok=True)
            img_resize_lanczos.save(args.input + "/resized/" + file)

if args.compare_dir:
    print("Comparing directories")
    mask_files = set()
    images = set()
    for root, dirs, files in os.walk(args.input):
        images = set(files)
    for root, dirs, files in os.walk(args.mask_dir):
        mask_files = set(files)
    
    for image in images:
        if image not in mask_files:
            os.remove(args.input + "/" + image)
            print(f"Removing {args.input}/{image}")


# loop over all files in the input directory
if args.convert:
    counter = 0
    os.makedirs(args.input+"/out", exist_ok=True)
    for filename in os.listdir(args.input):
        if filename.lower().endswith(('.png')):
            # construct input and output file paths
            input_path = os.path.join(args.input, filename)
            output_filename = filename.replace('.png', '.png')
            # output_filename = f"Benedict{counter}.png"
            counter += 1
            output_path = args.input+"/out/"+output_filename
            print(output_path)
            # open input image using PIL
            with Image.open(input_path) as img:
                exif = img._getexif()
                if exif:
                    # check the exif metadata for orientation information
                    exif = dict((ExifTags.TAGS[k], v) for k, v in img._getexif().items() if k in ExifTags.TAGS)
                    if 'Orientation' in exif:
                        # transpose the image according to its orientation
                        orientation = exif['Orientation']
                        if orientation == 1:
                            pass
                        elif orientation == 2:
                            img = img.transpose(Image.FLIP_LEFT_RIGHT)
                        elif orientation == 3:
                            img = img.rotate(180)
                        elif orientation == 4:
                            img = img.transpose(Image.FLIP_TOP_BOTTOM)
                        elif orientation == 5:
                            img = img.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)
                        elif orientation == 6:
                            img = img.rotate(-90)
                        elif orientation == 7:
                            img = img.rotate(90).transpose(Image.FLIP_LEFT_RIGHT)
                        elif orientation == 8:
                            img = img.rotate(90)
                            
                # convert the image to RGB format (if it is not already in RGB format)
                rgb_img = img.convert('RGB')
                # save the image in PNG format
                rgb_img.save(output_path, format='PNG')
            
            # print message indicating successful conversion
            print(f'{filename} converted to PNG format and saved as {output_filename} in {args.input}')