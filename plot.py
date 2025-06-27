######################################################################################
### Blood Cell Detection - Visualization Tool
### Author:
### Project: Blood Cell Detection - Visualization Tool
### Description: This script reads image data and bounding box Annotation from a CSV,
### draws the labeled boxes on each image, and saves the output to a new folder.
######################################################################################

# 📦 Required libraries
import pandas as pd  # For data manipulation
import matplotlib.pyplot as plt  # For image display and saving
from matplotlib import patches  # For drawing bounding boxes
import os  # For file and directory operations

def get_image_files(folder_path, file_ext):
    """
    Returns all filenames with a given extension from a directory.
    Args:
        folder_path (str): Directory to search in.
        file_ext (str): File extension (e.g., 'jpg').
    Returns:
        Tuple: (List of filenames, total count)
    """
    files = [f for f in os.listdir(folder_path) if f.endswith(file_ext)]  # Filter files by extension
    return files, len(files)  # Return the list and count

# Load image file names from the target directory
image_files, total_images = get_image_files("BCCD/JPEImages", "jpg")  # Get all .jpg files

# Load annotation CSV
Annotation = pd.read_csv("test-.csv", header=None)  # Load CSV without header
Annotation.columns = ['filename', 'cell_type', 'xmin', 'xmax', 'ymin', 'ymax']  # Set column names

# Process each image
for img_name in image_files:  # Loop through all image files
    fig = plt.figure()  # Create a new figure
    ax = fig.add_axes([0, 0, 1, 1])  # Use entire figure for plotting
    plt.axis('off')  # Hide axis

    img_path = os.path.join("BCCD/JPEImages", img_name)  # Build full path to image
    image = plt.imread(img_path)  # Read image
    plt.imshow(image)  # Display image

    image_rows = Annotation[Annotation.filename == img_name]  # Filter Annotation for this image

    for _, row in image_rows.iterrows():  # Iterate through each annotation row
        xmin, xmax, ymin, ymax = map(float, [row.xmin, row.xmax, row.ymin, row.ymax])  # Convert coords
        width, height = xmax - xmin, ymax - ymin  # Calculate box dimensions
        label = row.cell_type  # Get label

        if label == 'RBC':  # Red Blood Cell
            ax.annotate('RBC', xy=(xmax - 40, ymin + 20))  # Annotate label
            color = 'red'  # Set box color
        elif label == 'WBC':  # White Blood Cell
            ax.annotate('WBC', xy=(xmax - 40, ymin + 20))
            color = 'blue'
        elif label == 'Platelets':  # Platelets
            ax.annotate('Platelets', xy=(xmax - 40, ymin + 20))
            color = 'green'
        else:
            continue  # Skip if unknown label

        box = patches.Rectangle((xmin, ymin), width, height, edgecolor=color, facecolor='none')  # Create box
        ax.add_patch(box)  # Add box to image

    os.makedirs("imagesBox", exist_ok=True)  # Create output folder if it doesn't exist
    output_path = os.path.join("imagesBox", img_name)  # Set path to save image
    fig.savefig(output_path, dpi=90, bbox_inches='tight')  # Save image
    plt.close()  # Close figure
    print(f"✅ Saved: {img_name} -> imagesBox/")  # Print confirmation

print("✅ All images have been processed and saved.")  # Final message
