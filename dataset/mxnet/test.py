######################################################################################
### 
### Filename: visualize_batch.py
### Version: 1.0
### Description: Loads and visualizes batches from .rec files using MXNet's ImageDetIter.
###              Draws bounding boxes on images for RBC, WBC, and Platelets classes.
######################################################################################

from mxnet import gluon, image, nd
import matplotlib.pyplot as plt

# Configuration
data_shape = (480, 640)
batch_size = 64
data_dir = '../../BCCD/'

def get_iterators(data_shape, batch_size):
    class_names = ["RBC", "WBC", "Platelets"]
    num_class = len(class_names)

    train_iter = image.ImageDetIter(
        batch_size=batch_size,
        data_shape=(3, data_shape[0], data_shape[1]),
        path_imgrec=data_dir + 'train.rec',
        path_imgidx=data_dir + 'train.idx',
        shuffle=True,
        mean=True,
        rand_crop=1,
        min_object_covered=0.95,
        max_attempts=200
    )

    val_iter = image.ImageDetIter(
        batch_size=batch_size,
        data_shape=(3, data_shape[0], data_shape[1]),
        path_imgrec=data_dir + 'val.rec',
        shuffle=False,
        mean=True
    )

    return train_iter, val_iter, class_names, num_class

# Load iterators and one test batch
train_data, test_data, class_names, num_class = get_iterators(data_shape, batch_size)
batch = test_data.next()

def box_to_rect(box, color, linewidth=3):
    """Convert bounding box tensor to a matplotlib rectangle."""
    box = box.asnumpy()
    return plt.Rectangle(
        (box[0], box[1]), box[2] - box[0], box[3] - box[1],
        fill=False, edgecolor=color, linewidth=linewidth
    )

# Visualization
_, axes = plt.subplots(3, 3, figsize=(6, 6))
for i in range(3):
    for j in range(3):
        index = 3 * i + j
        img = batch.data[0][index]
        labels = batch.label[0][index]

        img = img.transpose((1, 2, 0)).clip(0, 255).asnumpy() / 255.0
        ax = axes[i][j]
        ax.imshow(img)

        for label in labels:
            label[1] *= data_shape[1]  # xmin
            label[3] *= data_shape[1]  # xmax
            label[2] *= data_shape[0]  # ymin
            label[4] *= data_shape[0]  # ymax

            if label[0] == 0:
                rect = box_to_rect(label[1:5], 'red', 0.5)
            elif label[0] == 1:
                rect = box_to_rect(label[1:5], 'green', 0.5)
            elif label[0] == 2:
                rect = box_to_rect(label[1:5], 'blue', 0.5)
            else:
                rect = box_to_rect(label[1:5], 'black', 1)

            ax.add_patch(rect)

        ax.axis('off')

plt.tight_layout()
plt.show()
