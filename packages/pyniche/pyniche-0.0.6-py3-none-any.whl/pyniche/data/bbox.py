from numpy import outer
import torch


def resize_bbox(bbox, target_size):
    """
    param
    ---
    bbox: all floating numbers: [x, y, w, h]
    target_size: a tensor of [h, w] ***** very important! *****

    return
    ---
    a new bbox with the same aspect ratio, but resized to fit the target size
    """
    bx, by, bw, bh = bbox
    th, tw = target_size
    new_x = bx * tw
    new_y = by * th
    new_w = bw * tw
    new_h = bh * th
    return torch.tensor([new_x, new_y, new_w, new_h])


def xywh2xyxy(xywh, in_xy="center"):
    """
    param
    ---
    xywh: all floating numbers: [x, y, w, h]
    in_xy: "center" or "top-left" of the input bbox xy
        - Note that the output from DETR is in "center" format

    return
    ---
    xyxy: all floating numbers: [x1, y1, x2, y2] from top-left to bottom-right
    """
    x, y, w, h = xywh
    if in_xy == "center":
        dw, dh = int(w / 2), int(h / 2)
        x1 = x - dw
        y1 = y - dh
        x2 = x + dw
        y2 = y + dh
    elif in_xy == "top-left":
        x1 = x
        y1 = y
        x2 = x + w
        y2 = y + h
    return torch.tensor([x1, y1, x2, y2])
