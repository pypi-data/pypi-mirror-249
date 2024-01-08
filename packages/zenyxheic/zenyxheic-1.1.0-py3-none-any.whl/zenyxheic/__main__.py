from PIL import Image
from pillow_heif import register_heif_opener
from zenyx import printf
import os
import sys

register_heif_opener()

import os


def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            print(f"Directory created: {directory_path}")
        except OSError as e:
            print(f"Error creating directory {directory_path}: {e}")
    
    print(f"Saving to heic_converted")


def list_files_in_directory(directory_path):
    file_paths = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths


def convert_heic_to_png(heic_path: str, mode: int):
    try:
        modes: dict[int, list[str, str]] = {
            0: ["png", "PNG"],
            1: ["jpg", "JPEG"]
        }

        png_path = heic_path.replace(heic_path.split("\\")[-2], "heic_converted")
        png_path = png_path[:-4] + png_path[-4:].replace("heic", modes[mode][0]).replace(
            "HEIC", modes[mode][0]
        )

        # Open HEIC image
        heic_image = Image.open(heic_path)
        
        max_size = (1920, 1920)
        heic_image.thumbnail(max_size)
        # Save as PNG
        heic_image.save(png_path, format=modes[mode][1])

        printf(f"@!✓ Success:$& {os.path.basename(heic_path)} ⟹  {os.path.basename(png_path)}")
    except Exception as e:
        printf(f"@!✗ Error:$& {e}")

def main(mode: int):
    mode = int(mode)
    if mode < 0 or mode > 1:
        raise Exception("Mode does not exist: 0 - PNG; 1 - JPEG")

    printf.clear_screen()
    printf.title("HEIC ⟹  PNG")
    files_list = list_files_in_directory("input")

    ensure_directory_exists("heic_converted")

    for file_path in files_list:
        if not str(os.path.basename(file_path)).lower().endswith("heic"):
            continue
        convert_heic_to_png(file_path, mode)

if __name__ == "__main__":
    args: list[str] = sys.argv
    main(args[1])