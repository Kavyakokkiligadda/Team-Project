######################################################################################
### Blood Cell Detection - Visualization Tool
### Author: kavya Kokkiligadda
### 
### Project: Blood Cell Detection - Visualization Tool
### Description: This script reads image data and bounding box annotations from a CSV,
### draws the labeled boxes on each image, and saves the output to a new folder.
######################################################################################
# 📦 Required libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patches
import os
def get_image_files(folder_path, file_ext):
    """
    Returns all filenames with a given extension from a directory.
    
    Args:
        folder_path (str): Directory to search in.
        file_ext (str): File extension (e.g., 'jpg').

    Returns:
        Tuple: (List of filenames, total count)
    """
    files = [f for f in os.listdir(folder_path) if f.endswith(file_ext)]
    return files, len(files)

# Load image file names from the target directory
image_files, total_images = get_image_files("BCCD/JPEGImages", "jpg")

# Load annotation CSV
annotations = pd.read_csv("test.csv", header=None)
annotations.columns = ['filename', 'cell_type', 'xmin', 'xmax', 'ymin', 'ymax']

# Process each image
for img_name in image_files:
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])  # Full image space
    plt.axis('off')

    # Load and display image
    img_path = os.path.join("BCCD/JPEGImages", img_name)
    image = plt.imread(img_path)
    plt.imshow(image)

    # Filter annotations for this image
    image_rows = annotations[annotations.filename == img_name]
    # Draw bounding boxes for each object in the image
    for _, row in image_rows.iterrows():
        xmin, xmax, ymin, ymax = map(float, [row.xmin, row.xmax, row.ymin, row.ymax])
        width, height = xmax - xmin, ymax - ymin
        label = row.cell_type

        if label == 'RBC':
            ax.annotate('RBC', xy=(xmax - 40, ymin + 20))
            color = 'red'
        elif label == 'WBC':
            ax.annotate('WBC', xy=(xmax - 40, ymin + 20))
            color = 'blue'
        elif label == 'Platelets':
            ax.annotate('Platelets', xy=(xmax - 40, ymin + 20))
            color = 'green'
        else:
            continue  # Skip unknown labels
        box = patches.Rectangle((xmin, ymin), width, height, edgecolor=color, facecolor='none')
        ax.add_patch(box)
    # Create output folder if it doesn’t exist
    os.makedirs("imagesBox", exist_ok=True)
        # Save the visualized image
    output_path = os.path.join("imagesBox", img_name)
    fig.savefig(output_path, dpi=90, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {img_name} -> imagesBox/")
print("✅ All images have been processed and saved.")
