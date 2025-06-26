######################################################################################
### Author/Developer: Kavya Kokkiligadda
### Filename: export.py
### Version: 1.0
### Description: Generates a CSV file from XML annotations in Pascal VOC format.
### Each record includes: filename, cell type, and bounding box coordinates.
######################################################################################

import os
import xml.etree.ElementTree as ET
from glob import glob
import pandas as pd

# Collect all XML annotation files
annotation_files = glob('BCCD/Annotations/*.xml')

# List to hold extracted data
records = []

# Process each XML file
for xml_file in annotation_files:
    # Derive image filename from XML filename
    base_name = os.path.basename(xml_file).replace('.xml', '.jpg')

    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract object details
    for obj in root.findall('object'):
        label = obj.find('name').text
        xmin = int(obj.find('bndbox/xmin').text)
        xmax = int(obj.find('bndbox/xmax').text)
        ymin = int(obj.find('bndbox/ymin').text)
        ymax = int(obj.find('bndbox/ymax').text)

        # Add the row to the records list
        records.append([base_name, label, xmin, xmax, ymin, ymax])

# Create a DataFrame from the extracted data
df = pd.DataFrame(records, columns=['filename', 'cell_type', 'xmin', 'xmax', 'ymin', 'ymax'])

# Export the DataFrame to CSV
df.to_csv('test.csv', index=False)
