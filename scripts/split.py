######################################################################################
### Filename: split.py
### Version: 1.0
### Description: Splits image filenames into train, val, test, and trainval sets.
### Output: Four files (train-.txt, value.txt, test.txt, trainvalue.txt) under ImageSets/Main
######################################################################################

import os  # For file and directory operations
import argparse  # For handling command-line arguments
import random  # For shuffling image list
import math  # For rounding up split counts
# Default paths
DEFAULT_IMAGE_DIR = "../BCCD/JPEImages/"  # Path to images
DEFAULT_OUTPUT_DIR = "../BCCD/ImageSets/Main/"  # Output path for split files

def create_split_files(images_dir, output_dir, trainval_ratio=0.9, train_ratio=0.8):
    os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

    all_images = [img.split('.')[0] for img in os.listdir(images_dir)]  # Get all image filenames (without extension)
    random.shuffle(all_images)  # Shuffle to randomize split

    total = len(all_images)  # Total number of images
    trainval_count = math.ceil(trainval_ratio * total)  # Calculate number for trainval set
    train_count = math.ceil(trainval_count * train_ratio)  # Calculate number for train set

    trainval_set = sorted(all_images[:trainval_count])  # First part goes to trainval
    test_set = sorted(all_images[trainval_count:])  # Remaining goes to test
    train_set = sorted(trainval_set[:train_count])  # First part of trainval is train
    val_set = sorted(trainval_set[train_count:])  # Remaining part of trainval is val

    sets = {
        "trainvalue.txt": trainval_set,  # Train + validation filenames
        "train-.txt": train_set,  # Training filenames
        "value.txt": val_set,  # Validation filenames
        "test.txt": test_set  # Test filenames
    }

    for filename, data in sets.items():  # Write each set to corresponding file
        with open(os.path.join(output_dir, filename), "w") as f:  # Open output file
            for line in data:
                f.write(f"{line}\n")  # Write image name (one per line)

    print(f"Total: {total} | TrainVal: {len(trainval_set)} | Test: {len(test_set)} | Train: {len(train_set)} | Val: {len(val_set)}")  # Print split summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split image dataset for training and validation.")  # Define argument parser
    parser.add_argument("--images", default=DEFAULT_IMAGE_DIR, help="Directory containing JPEG images.")  # Image directory argument
    parser.add_argument("--output", default=DEFAULT_OUTPUT_DIR, help="Directory to save split text files.")  # Output directory argument
    args = parser.parse_args()  # Parse arguments

    create_split_files(args.images, args.output)  # Run the split function
