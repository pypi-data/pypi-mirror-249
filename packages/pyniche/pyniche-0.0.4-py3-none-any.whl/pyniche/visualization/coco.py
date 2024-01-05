import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import numpy as np
import colorsys


def show_dataset(dataset, idx=None):
    # COCO API
    coco = dataset.coco

    # get image id from idx
    img_ids = list(coco.imgs.keys())
    if idx is None:
        idx = random.randint(0, len(img_ids))
    img_id = img_ids[idx]
    image = dataset._load_image(img_id)

    # Get all distinct categories and create a color for each of them
    categories = coco.loadCats(coco.getCatIds())
    num_classes = len(categories)
    hsv_tuples = [(x / num_classes, 1.0, 1.0) for x in range(num_classes)]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = [(int(r * 255), int(g * 255), int(b * 255)) for r, g, b in colors]
    random.shuffle(colors)

    # Display the image
    plt.figure(figsize=(10, 10))
    plt.imshow(image)

    # Add the bounding boxes
    ax = plt.gca()
    annotation_ids = coco.getAnnIds(imgIds=img_id, iscrowd=None)
    annotations = coco.loadAnns(annotation_ids)
    annotation = annotations[0]
    annotation["bbox"]
    annotation["segmentation"][0]

    for annotation in annotations:
        # Draw bounding box
        bbox = annotation["bbox"]
        box = patches.Rectangle(
            (bbox[0], bbox[1]),
            bbox[2],
            bbox[3],
            linewidth=2,
            edgecolor="r",
            facecolor="none",
        )
        ax.add_patch(box)

        # Draw segmentation
        if "segmentation" in annotation:
            category_id = annotation["category_id"]
            color = (
                colors[categories.index(category_id)]
                if category_id in categories
                else "r"
            )
            for seg in annotation["segmentation"]:
                poly = np.array(seg).reshape((int(len(seg) / 2), 2))
                polygon = patches.Polygon(
                    poly, linewidth=1, edgecolor=color, facecolor=color, alpha=0.5
                )
                ax.add_patch(polygon)

        # Draw label
        label = coco.loadCats(annotation["category_id"])[0]["name"]
        plt.text(
            bbox[0],
            bbox[1] - 10,
            label,
            color="white",
            fontsize=12,
            bbox={"facecolor": "red", "alpha": 0.5},
        )
