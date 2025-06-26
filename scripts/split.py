######################################################################################
### Author/Developer: Kavya Kokkiligadda
### Filename: split.py
### Version: 1.0
### Description: Splits image filenames into train, val, test, and trainval sets.
### Output: Four files (train.txt, val.txt, test.txt, trainval.txt) under ImageSets/Main
######################################################################################

import os 
import argparse
import random
import math

# Default paths
DEFAULT_IMAGE_DIR = "../BCCD/JPEGImages/"
DEFAULT_OUTPUT_DIR = "../BCCD/ImageSets/Main/"

def create_split_files(images_dir, output_dir, trainval_ratio=0.9, train_ratio=0.8):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get list of image base names (without extension)
    all_images = [img.split('.')[0] for img in os.listdir(images_dir)]
    random.shuffle(all_images)

    total = len(all_images)
    trainval_count = math.ceil(trainval_ratio * total)
    train_count = math.ceil(trainval_count * train_ratio)

    trainval_set = sorted(all_images[:trainval_count])
    test_set     = sorted(all_images[trainval_count:])
    train_set    = sorted(trainval_set[:train_count])
    val_set      = sorted(trainval_set[train_count:])

    # Mapping output filenames to data
    sets = {
        "trainval.txt": trainval_set,
        "train.txt": train_set,
        "val.txt": val_set,
        "test.txt": test_set
    }

    # Write to files
    for filename, data in sets.items():
        with open(os.path.join(output_dir, filename), "w") as f:
            for line in data:
                f.write(f"{line}\n")

    # Console summary
    print(f"Total: {total} | TrainVal: {len(trainval_set)} | Test: {len(test_set)} | Train: {len(train_set)} | Val: {len(val_set)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split image dataset for training and validation.")
    parser.add_argument("--images", default=DEFAULT_IMAGE_DIR, help="Directory containing JPEG images.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_DIR, help="Directory to save split text files.")
    args = parser.parse_args()

    create_split_files(args.images, args.output)
