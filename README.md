# 🧬 BCCD Blood Cell Detection Dataset

This project is focused on identifying and labeling human blood cells in microscope images using object detection techniques. The dataset has been arranged in Pascal VOC format and includes image Annotation for three major blood cell types.

---

## 📁 Dataset Structure

```
BCCD_Dataset/
├── BCCD/
│   ├── Annotation/       # XML annotation files (bounding boxes)
│   ├── ImageSets/         # Train/test/val split text files
│   └── JPEImages/        # Input images
├── dataset/
│   └── mxnet/             # MXNet processing utilities
├── scripts/
│   ├── split.py           # Generates train/test/val sets
│   └── visualize.py       # Draws bounding boxes on images
├── export.py              # Converts VOC XML to CSV format
├── plot.py                # Plots bounding boxes using CSV
├── example.jpg            # Sample output visualization
├── LICENSE
└── README.md
```

---

## 🔍 Dataset Labels

The dataset identifies three types of blood cells:
- **RBC** – Red Blood Cells  
- **WBC** – White Blood Cells  
- **Platelets**

Each label is annotated with bounding boxes in VOC format XML files.

---

## 🛠️ Script Descriptions

### `export.py`
Converts the annotated XML files into a structured CSV (`test-.csv`) with the following columns:
- Filename
- Class label
- Coordinates (x1, y1, x2, y2)

### `plot.py`
Uses `test-.csv` to visualize bounding boxes on each image and saves them in a new output directory.

---

## 🖼️ Sample Visualization

![example](./example.jpg)

---

## 📐 Image Details

- **Format**: JPEG
- **Resolution**: 640 × 480 pixels
- **Annotation Format**: Pascal VOC XML

Example `.xml` snippet:

```xml
<object>
    <name>WBC</name>
    <bndbox>
        <xmin>260</xmin>
        <ymin>177</ymin>
        <xmax>491</xmax>
        <ymax>376</ymax>
    </bndbox>
</object>
```

---

## ⚙️ Intended Usage

You can use this dataset with models like:
- **Faster R-CNN**
- **YOLO**
- **SSD**

Also compatible with MXNet via `.rec` file conversion and `ImageDetIter`.

---

