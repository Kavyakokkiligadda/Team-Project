######################################################################################
### Filename: visualize_one.py
### Version: 1.0
### Description: Generates labeled image from a single Pascal VOC XML annotation.
### Output: Displays and saves a labeled image with bounding boxes and class names.
######################################################################################

import xml.etree.ElementTree as ET  # For parsing XML annotation files
import cv2  # OpenCV for image processing and visualization

# Set image and annotation path
image_path = "../BCCD/JPEGImages/BloodImage_00023.jpg"  # Path to the image
annotation_path = "Annotation/BloodImage_00023.xml"  # Path to the corresponding annotation file

# Load image
image = cv2.imread(image_path)  # Read image using OpenCV

# Parse XML file
tree = ET.parse(annotation_path)  # Parse the XML tree
root = tree.getroot()  # Get root of the XML

# Iterate over objects and draw bounding boxes
for obj in root.iter("object"):  # Loop through each object in XML
    name = obj.find("name").text  # Get object class name
    bndbox = obj.find("bndbox")  # Get bounding box tag
    xmin = int(float(bndbox.find("xmin").text))  # X-coordinate of top-left corner
    ymin = int(float(bndbox.find("ymin").text))  # Y-coordinate of top-left corner
    xmax = int(float(bndbox.find("xmax").text))  # X-coordinate of bottom-right corner
    ymax = int(float(bndbox.find("ymax").text))  # Y-coordinate of bottom-right corner

    # Choose color based on class
    if name.startswith("R"):  # RBC
        color = (0, 255, 0)  # Green
    elif name.startswith("W"):  # WBC
        color = (0, 0, 255)  # Red
    elif name.startswith("P"):  # Platelets
        color = (255, 0, 0)  # Blue
    else:
        color = (0, 255, 255)  # Yellow for unknown class

    # Draw rectangle and label
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 1)  # Draw bounding box
    cv2.putText(image, name, (xmin + 10, ymin + 15),  # Put class label text
                cv2.FONT_HERSHEY_SIMPLEX, 1e-3 * image.shape[0], color, 1)  # Adjust font size to image

# Show and save image
cv2.imshow("Labeled Image", image)  # Display the image with Annotation
cv2.imwrite("test.jpg", image)  # Save the output image
cv2.waitKey(0)  # Wait for a key press
cv2.destroyAllWindows()  # Close all OpenCV windows
