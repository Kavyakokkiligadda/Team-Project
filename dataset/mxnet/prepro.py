######################################################################################
### Author/Developer: Kavya Kokkiligadda
### Filename: gen_rec.py
### Version: 1.0
### Description: Converts Pascal VOC XML annotations into MXNet-compatible .lst files
###              for object detection tasks. Generates train.lst and val.lst.
######################################################################################

import os
import random
import xml.etree.ElementTree as ET

# Define classes and dataset path
classes = ["RBC", "WBC", "Platelets"]
dataset_path = "../../BCCD"
train_split_ratio = 0.9  # 90% for training, 10% for validation

def generate_lst_files(classes, base_dir, ratio=1.0):
    assert 0 <= ratio <= 1, "Ratio must be between 0 and 1"

    images_dir = os.path.join(base_dir, "JPEGImages")
    annotations_dir = os.path.join(base_dir, "Annotations")

    image_files = sorted(os.listdir(images_dir))
    annotation_files = sorted(os.listdir(annotations_dir))

    assert len(image_files) == len(annotation_files), "Mismatch between images and annotations"

    total = len(image_files)
    indices = list(range(total))
    random.shuffle(indices)

    train_indices = indices[:int(total * ratio)]
    val_indices = indices[int(total * ratio):]

    with open("train.lst", "w") as train_f:
        print("📄 Writing train.lst...")

        val_f = open("val.lst", "w") if val_indices else None
        if val_f:
            print("📄 Writing val.lst...")

        for idx in range(total):
            img_name = image_files[idx]
            xml_name = annotation_files[idx]

            img_path = os.path.join(images_dir, img_name)
            xml_path = os.path.join(annotations_dir, xml_name)

            tree = ET.parse(xml_path)
            root = tree.getroot()

            width = float(root.find("size/width").text)
            height = float(root.find("size/height").text)

            record = [str(idx), f"4\t5\t{width}\t{height}"]

            for obj in root.iter("object"):
                label = obj.find("name").text
                if label not in classes:
                    continue

                class_id = classes.index(label)
                bndbox = obj.find("bndbox")
                xmin = float(bndbox.find("xmin").text) / width
                ymin = float(bndbox.find("ymin").text) / height
                xmax = float(bndbox.find("xmax").text) / width
                ymax = float(bndbox.find("ymax").text) / height

                record += [str(class_id), str(xmin), str(ymin), str(xmax), str(ymax)]

            record.append(img_path)
            final_line = "\t".join(record) + "\n"

            if idx in train_indices:
                train_f.write(final_line)
            else:
                if val_f:
                    val_f.write(final_line)

        if val_f:
            val_f.close()

    print("✅ .lst generation complete.")

# Run the function
generate_lst_files(classes, dataset_path, train_split_ratio)
