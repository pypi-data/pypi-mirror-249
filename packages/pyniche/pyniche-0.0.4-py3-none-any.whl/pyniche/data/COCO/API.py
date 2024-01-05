"""
API methods
---
- i/o
    - load
    - save

- subsetting
    - subset_by_dir
    - subset_by_image_ids

- getters
    - get_filenames_from_dir
    - get_ids_from_imgs
    - get_img_by_filename
    - get_img_by_image_id
    - get_ann_by_image_id

- concatenate
- reindex_coco
"""

# native imports
import json
import os
import numpy as np
import pyniche


class COCO_API:
    def __init__(self, data=None, path_json=None):
        # members
        self.data = None  # dict of COCO keys
        self.path_json = path_json

        # init
        if data is not None:
            # 1. user provided dict
            self.data = data
        else:
            # 2. user provided path to json
            self.load()

    def load(self):
        with open(self.path_json, "r") as f:
            self.data = json.load(f)

    def save(self, path):
        with open(path, "w") as f:
            json.dump(self.data, f)

    def new_instance(self, imgs_coco, ann_coco):
        # re-index images and annotations
        imgs_coco, ann_coco = reindex_coco(imgs_coco, ann_coco)

        # new instance
        new_json = dict(
            {
                "info": self.info(),
                "licenses": self.licenses(),
                "categories": self.categories(),
                "images": imgs_coco,
                "annotations": ann_coco,
            }
        )
        return COCO_API(data=new_json)

    # subsetting
    def subset_by_dir(self, dir_img):
        # get images from dir
        filenames = self.get_filenames_from_dir(dir_img)
        imgs_coco = self.get_img_by_filename(filenames)

        # get ann by ids of images
        ids = self.get_ids_from_imgs(imgs_coco)
        ann_coco = self.get_ann_by_image_id(ids)

        # return
        return self.new_instance(imgs_coco, ann_coco)

    def subset_by_image_ids(self, ids):
        if isinstance(ids, int):
            # if int, it's a single id
            ids = [ids]
        elif isinstance(ids, list):
            # if list, it's a list of ids
            ids = ids
        elif isinstance(ids, tuple):
            # if tuple, it's a range
            ids = list(np.arange(ids[0], ids[1] + 1))

        # filter images
        imgs_coco = self.get_img_by_image_id(ids)
        ann_coco = self.get_ann_by_image_id(ids)

        # return
        return self.new_instance(imgs_coco, ann_coco)

    # getters
    def get_filenames_from_dir(self, dir_img):
        filenames = [f for f in os.listdir(dir_img) if ".jpg" in f or ".png" in f]
        return filenames

    def get_ids_from_imgs(self, imgs_coco):
        ids = [i["id"] for i in imgs_coco]
        return ids

    def get_img_by_filename(self, filenames):
        imgs_coco = [i for i in self.images() if i["file_name"] in filenames]
        return imgs_coco

    def get_img_by_image_id(self, ids):
        imgs_coco = [i for i in self.images() if i["id"] in ids]
        return imgs_coco

    def get_ann_by_image_id(self, ids):
        ann_coco = [a for a in self.annotations() if a["image_id"] in ids]
        return ann_coco

    # concat
    def concatenate(self, coco):
        """
        both self and coco are COCO_API instances
        """
        # check the self data and max id
        imgs_self = self.images()
        ann_self = self.annotations()
        max_img_id_self = max([i["id"] for i in imgs_self])
        max_ann_id_self = max([a["id"] for a in ann_self])
        # check the coco data and reinex
        imgs_coco = coco.images()
        ann_coco = coco.annotations()
        imgs_coco, ann_coco = reindex_coco(
            imgs_coco,
            ann_coco,
            base_img=max_img_id_self + 1,
            base_ann=max_ann_id_self + 1,
        )

        # concatenate
        imgs_new = imgs_self + imgs_coco
        ann_new = ann_self + ann_coco
        return self.new_instance(imgs_new, ann_new)

    # COCO keys
    def info(self):
        return self.data["info"]

    def licenses(self):
        return self.data["licenses"]

    def categories(self):
        return self.data["categories"]

    def images(self):
        return self.data["images"]

    def annotations(self):
        return self.data["annotations"]


def reindex_coco(images, annotations, base_img=0, base_ann=0):
    """
    re-index images and annotations, starting from base
    """
    # re-index images
    for i, img in enumerate(images):
        img["id"] = base_img + i
        for ann in annotations:
            if ann["image_id"] == img["id"]:
                ann["image_id"] = img["id"]
    # re-index annotations
    for i, ann in enumerate(annotations):
        ann["id"] = base_ann + i
    return images, annotations


# # IMPLEMENTATION -----
# PATH = os.path.join("/Users", "niche", "_03_Papers", "2024", "cowsformer", "data")


# def get_json(setname):
#     """
#     arguments
#     ---
#     setname: side, top, holstein

#     prerequisite
#     ---
#     PATH is the root path of the data
#     """
#     return os.path.join(PATH, "coco_{}.json".format(setname))


# def get_dir(setname, task):
#     """
#     arguments
#     ---
#     setname: 1a_angle_t2s, 1b_angle_s2t, 2_light, 3_breed, 4_all
#     task: train, test

#     prerequisite
#     ---
#     PATH is the root path of the data
#     """
#     return os.path.join(PATH, setname, task)

from pyniche.data.COCO.API import COCO_API
pyniche.
import pyniche.data as pd
pd.
# coco_side = COCO_API(PATH_JSON["side"])
# coco_top = COCO_API(PATH_JSON["top"])
# coco_holstein = COCO_API(PATH_JSON["holstein"])

# dir_tgt = get_dir("1a_angle_t2s", "test")
# imgs_tgt = [f for f in os.listdir(dir_tgt) if ".jpg" in f or ".png" in f]
# imgs_tgt

# imgs_coco = [i for i in coco_side.images() if i["file_name"] in imgs_tgt]
# ids_coco = [i["id"] for i in imgs_coco]
# ann_coco = [a for a in coco_side.annotations() if a["image_id"] in ids_coco]

# imgs_coco, ann_coco = reindex_coco(imgs_coco, ann_coco)

# new_json = dict(
#     {
#         "info": coco_side.info(),
#         "licenses": coco_side.licenses(),
#         "categories": coco_side.categories(),
#         "images": imgs_coco,
#         "annotations": ann_coco,
#     }
# )


# len(ann_coco)

# len(imgs_coco)

# len(imgs_tgt)
