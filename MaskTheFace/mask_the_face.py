# Author: aqeelanwar
# Created: 27 April,2020, 10:22 PM
# Email: aqeel.anwar@gatech.edu

import argparse
import dlib
from utils.aux_functions import *



# Command-line input setup
parser = argparse.ArgumentParser(
    description="MaskTheFace - Python code to mask faces dataset"
)
parser.add_argument(
    "--path",
    type=str,
    default="",
    help="Path to either the folder containing images or the image itself",
)
parser.add_argument(
    "--mask_type",
    type=str,
    default="surgical",
    choices=["surgical", "N95", "KN95", "cloth", "gas", "inpaint", "random", "all"],
    help="Type of the mask to be applied. Available options: all, surgical_blue, surgical_green, N95, cloth",
)

parser.add_argument(
    "--pattern",
    type=str,
    default="",
    help="Type of the pattern. Available options in masks/textures",
)

parser.add_argument(
    "--pattern_weight",
    type=float,
    default=0.0,
    help="Weight of the pattern. Must be between 0 and 1",
)

parser.add_argument(
    "--color",
    type=str,
    default="#FFFFFF",
    help="Hex color value that need to be overlayed to the mask",
)

parser.add_argument(
    "--color_weight",
    type=float,
    default=1.0,
    help="Weight of the color intensity. Must be between 0 and 1",
)

parser.add_argument(
    "--code",
    type=str,
    # default="cloth-masks/textures/check/check_4.jpg, cloth-#e54294, cloth-#ff0000, cloth, cloth-masks/textures/others/heart_1.png, cloth-masks/textures/fruits/pineapple.png, N95, surgical_blue, surgical_green",
    default="",
    help="Generate specific formats",
)


parser.add_argument(
    "--verbose", dest="verbose", action="store_true", help="Turn verbosity on"
)
parser.add_argument(
    "--write_original_image",
    dest="write_original_image",
    action="store_true",
    help="If true, original image is also stored in the masked folder",
)
parser.set_defaults(feature=False)

args = parser.parse_args()
args.write_path = args.path + "_masked"

# Set up dlib face detector and predictor
args.detector = dlib.get_frontal_face_detector()
path_to_dlib_model = "dlib_models/shape_predictor_68_face_landmarks.dat"
if not os.path.exists(path_to_dlib_model):
    download_dlib_model()

args.predictor = dlib.shape_predictor(path_to_dlib_model)

# Extract data from code
mask_code = "".join(args.code.split()).split(",")
args.code_count = np.zeros(len(mask_code))
args.mask_dict_of_dict = {}


for i, entry in enumerate(mask_code):
    mask_dict = {}
    mask_color = ""
    mask_texture = ""
    mask_type = entry.split("-")[0]
    if len(entry.split("-")) == 2:
        mask_variation = entry.split("-")[1]
        if "#" in mask_variation:
            mask_color = mask_variation
        else:
            mask_texture = mask_variation
    mask_dict["type"] = mask_type
    mask_dict["color"] = mask_color
    mask_dict["texture"] = mask_texture
    args.mask_dict_of_dict[i] = mask_dict

# Check if path is file or directory or none
is_directory, is_file, is_other = check_path(args.path)
display_MaskTheFace()

if is_directory:
    path, dirs, files = os.walk(args.path).__next__()
    file_count = len(files)
    dirs_count = len(dirs)
    if len(files) > 0:
        print_orderly("Masking image files", 60)

    # Process files in the directory if any
    for f in tqdm(files):
        image_path = path + "/" + f
        write_path = path + "_masked"
        if not os.path.isdir(write_path):
            os.makedirs(write_path)
            # masks will be stored at this dir
            os.makedirs(write_path + "/mask")

        if is_image(image_path):
            # Proceed if file is image
            if args.verbose:
                str_p = "Processing: " + image_path
                tqdm.write(str_p)

            split_path = f.rsplit(".")
            masked_image, mask, mask_binary_array, original_image = mask_image(
                image_path, args
            )
            for i in range(len(mask)):
                w_path = (
                    write_path
                    + "/"
                    + split_path[0]
                    + "."
                    + split_path[1]
                )

                # also need to obtain and stores the masks
                mask_path = (
                    write_path
                    + "/mask/"
                    + split_path[0]
                    + "."
                    + split_path[1]
                )

                img = masked_image[i]
                img_mask = np.expand_dims(mask_binary_array[i], -1)
                img_mask = np.repeat(img_mask, 3, -1)
                img_mask = np.where(img_mask > 0, 0, 255)
                # print(img_mask)

                # for i, row in enumerate(img_mask):
                #     row = np.where(row > 0, 0, 255 )
                #     # row = np.repeat(row, 3, 1)
                #     img_mask[i] = row
                # 
                # print(img_mask[180])
                # print(img[180])
                cv2.imwrite(mask_path, img_mask)
                cv2.imwrite(w_path, img)

    print_orderly("Masking image directories", 60)

    # Process directories withing the path provided
    for d in tqdm(dirs):
        dir_path = args.path + "/" + d
        dir_write_path = args.write_path + "/" + d
        if not os.path.isdir(dir_write_path):
            os.makedirs(dir_write_path)
        _, _, files = os.walk(dir_path).__next__()

        # Process each files within subdirectory
        for f in files:
            image_path = dir_path + "/" + f
            if args.verbose:
                str_p = "Processing: " + image_path
                tqdm.write(str_p)
            write_path = dir_write_path
            if is_image(image_path):
                # Proceed if file is image
                split_path = f.rsplit(".")
                masked_image, mask, mask_binary, original_image = mask_image(
                    image_path, args
                )
                for i in range(len(mask)):
                    w_path = (
                        write_path
                        + "/"
                        + split_path[0]
                        + "_"
                        + mask[i]
                        + "."
                        + split_path[1]
                    )
                    print("the path is: ", w_path)
                    w_path_original = write_path + "/" + f
                    img = masked_image[i]
                    # Write the masked image
                    cv2.imwrite(w_path, img)
                    # cv2.imwrite(w_path, )
                    if args.write_original_image:
                        # Write the original image
                        cv2.imwrite(w_path_original, original_image)

            if args.verbose:
                print(args.code_count)

# Process if the path was a file
elif is_file:
    print("Masking image file")
    image_path = args.path
    write_path = args.path.rsplit(".")[0]
    if is_image(image_path):
        # Proceed if file is image
        # masked_images, mask, mask_binary_array, original_image
        masked_image, mask, mask_binary_array, original_image = mask_image(
            image_path, args
        )
        for i in range(len(mask)):
            w_path = write_path + "_" + mask[i] + "." + args.path.rsplit(".")[1]
            img = masked_image[i]
            img_mask = mask_binary_array[i]

            cv2.imwrite(w_path, img)
else:
    print("Path is neither a valid file or a valid directory")
print("Processing Done")
