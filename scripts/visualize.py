######################################################################################
### Author/Developer: Kavya Kokkiligadda
### Filename: visualize_one.py
### Version: 1.0
### Description: Generates labeled image from a single Pascal VOC XML annotation.
### Output: Displays and saves a labeled image with bounding boxes and class names.
######################################################################################

import xml.etree.ElementTree as ET
import cv2

# Set image and annotation path
image_path = "../BCCD/JPEGImages/BloodImage_00023.jpg"
annotation_path = "Annotations/BloodImage_00023.xml"

# Load image
image = cv2.imread(image_path)

# Parse XML file
tree = ET.parse(annotation_path)
root = tree.getroot()

# Iterate over objects and draw bounding boxes
for obj in root.iter("object"):
    name = obj.find("name").text
    bndbox = obj.find("bndbox")
    xmin = int(float(bndbox.find("xmin").text))
    ymin = int(float(bndbox.find("ymin").text))
    xmax = int(float(bndbox.find("xmax").text))
    ymax = int(float(bndbox.find("ymax").text))

    # Choose color based on class
    if name.startswith("R"):
        color = (0, 255, 0)   # Green for RBC
    elif name.startswith("W"):
        color = (0, 0, 255)   # Red for WBC
    elif name.startswith("P"):
        color = (255, 0, 0)   # Blue for Platelets
    else:
        color = (0, 255, 255) # Yellow for unknown

    # Draw rectangle and label
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 1)
    cv2.putText(image, name, (xmin + 10, ymin + 15),
                cv2.FONT_HERSHEY_SIMPLEX, 1e-3 * image.shape[0], color, 1)

# Show and save image
cv2.imshow("Labeled Image", image)
cv2.imwrite("test.jpg", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
