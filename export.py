######################################################################################
### Filename: export.py
### Version: 1.0
### Description: Generates a CSV file from XML Annotation in Pascal VOC format.
### Each record includes: filename, cell type, and bounding box coordinates.
######################################################################################

import os  # For path and file handling
import xml.etree.ElementTree as ET  # For parsing XML files
from glob import glob  # For file pattern matching
import pandas as pd  # For creating and exporting DataFrame

annotation_files = glob('BCCD/Annotation/*.xml')  # Collect all XML annotation files

records = []  # List to hold extracted data

for xml_file in annotation_files:  # Process each XML file
    base_name = os.path.basename(xml_file).replace('.xml', '.jpg')  # Get corresponding image filename
    tree = ET.parse(xml_file)  # Parse XML structure
    root = tree.getroot()  # Get root element of XML

    for obj in root.findall('object'):  # Iterate over each object tag
        label = obj.find('name').text  # Extract object label
        xmin = int(obj.find('bndbox/xmin').text)  # Extract xmin coordinate
        xmax = int(obj.find('bndbox/xmax').text)  # Extract xmax coordinate
        ymin = int(obj.find('bndbox/ymin').text)  # Extract ymin coordinate
        ymax = int(obj.find('bndbox/ymax').text)  # Extract ymax coordinate
        records.append([base_name, label, xmin, xmax, ymin, ymax])  # Append record to list

df = pd.DataFrame(records, columns=['filename', 'cell_type', 'xmin', 'xmax', 'ymin', 'ymax'])  # Create DataFrame

df.to_csv('test-.csv', index=False)  # Export DataFrame to CSV without row index
