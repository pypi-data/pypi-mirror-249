"""
This module is used to process HuggingFace's DETR COCO dataset to be used with LightningDataModule.
"""

# native
import numpy as np

# local imports
from pyniche.data.base import BaseDataModule

# deep learning
import torch
from transformers import DetrImageProcessor
import albumentations as A

# CONSTANTS
PROCESSOR = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")


class DetectDataModule(BaseDataModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collate_fn(self, batch):
        """
        Turn a list of structs into a struct of arrays.

        param
        ---
        batch
            - sample 1
                - pixel_values
                - pixel_mask
                - labels
                    - image_id
                    - annotations
                        - id
                        - image_id
                        - category_id
                        - bbox
                        - iscrowd
                        - area
                        - segmentation
            - sample 2
                - pixel_values
                - pixel_mask
                - labels

        return
        ---
        a dict
            - pixel_values
                - sample 1
                - sample 2
                ...
            - pixel_mask
                - sample 1
                - sample 2
                ...
            - labels
                - sample 1
                - sample 2
                ...
        """
        # pixel_values = [item["pixel_values"] for item in batch]
        # labels = [item["labels"] for item in batch]
        # encoding = PROCESSOR.pad(pixel_values, return_tensors="pt")
        # # create a struct containing arrays
        # batch = {}
        # batch["pixel_values"] = encoding["pixel_values"]
        # batch["pixel_mask"] = encoding["pixel_mask"]
        # batch["labels"] = labels
        new_batch = {}
        new_batch["pixel_values"] = torch.stack(
            [item["pixel_values"] for item in batch]
        )
        new_batch["pixel_mask"] = torch.stack([item["pixel_mask"] for item in batch])
        new_batch["labels"] = [item["labels"] for item in batch]
        return new_batch

    def _collate_fn_train(self, batch):
        return self._collate_fn(batch)

    def _collate_fn_val(self, batch):
        return self._collate_fn(batch)

    def _collate_fn_test(self, batch):
        return self._collate_fn(batch)

    def _transform_train(self, examples):
        """
        input
        ---
        examples (a struct of arrays, SOA)
            image
                image 1
                image 2
                ...
            image_id
                image_id 1
                image_id 2
                ...
            ...
            annotations
                annotation 1
                    id
                        id 1
                        id 2
                        ...
                    image_id
                        image_id 1
                        image_id 1
                        ...
                    ...
                annotation 2
                    ...
                ...

        output
        ---
        batch (an array of structs, AOS)
            example 1
                pixel_values
                pixel_mask
                labels
                    size
                    image_id
                    class_labels
                        label 1
                        label 2
                        ...
                    boxes
                        box 1
                        box 2
                        ...
                    area
                        area 1
                        area 2
                        ...
                    iscrowd
                        iscrowd 1
                        iscrowd 2
                        ...
                    orig_size
            example 2
            ...
        """
        transform = A.Compose(
            [
                # A.HorizontalFlip(p=0.5),
                # A.VerticalFlip(p=0.5),
                # A.RandomBrightnessContrast(p=1),
            ],
            bbox_params=A.BboxParams(format="coco", label_fields=["category"]),
        )
        batch = process(examples, transform)
        return batch

    def _transform_val(self, examples):
        transform = A.Compose(
            [],
            bbox_params=A.BboxParams(format="coco", label_fields=["category"]),
        )
        batch = process(examples, transform)
        return batch

    def _transform_test(self, examples):
        transform = A.Compose(
            [],
            bbox_params=A.BboxParams(format="coco", label_fields=["category"]),
        )
        batch = process(examples, transform)
        return batch


def process(examples, transform):
    transformed_images = []
    transformed_anns = []
    for image, image_id, annotations in zip(
        examples["image"], examples["image_id"], examples["annotations"]
    ):
        # image
        image = np.array(image.convert("RGB"))[:, :, ::-1]
        # annotations
        out = transform(
            image=image,
            bboxes=annotations["bbox"],
            category=annotations["category_id"],
        )
        ann = {
            "image_id": image_id,
            "annotations": [
                {
                    "id": annotations["id"][i],
                    "image_id": annotations["image_id"][i],
                    "category_id": out["category"][i],
                    "bbox": out["bboxes"][i],
                    "iscrowd": annotations["iscrowd"][i],
                    "area": annotations["area"][i],
                    "segmentation": annotations["segmentation"][i],
                }
                for i in range(len(annotations["id"]))
            ],
        }
        # append
        transformed_images.append(out["image"])
        transformed_anns.append(ann)
    # process the transformed data
    batch = PROCESSOR(
        images=transformed_images,
        annotations=transformed_anns,
        return_tensors="pt",
    )
    return batch
