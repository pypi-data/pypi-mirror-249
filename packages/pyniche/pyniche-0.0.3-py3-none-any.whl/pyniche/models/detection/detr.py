"""
# Reference:
https://lightning.ai/docs/pytorch/stable/common/lightning_module.html
https://github.com/NielsRogge/Transformers-Tutorials/blob/master/DETR/Fine_tuning_DetrForObjectDetection_on_custom_dataset_(balloon).ipynb
"""

# torch imports
import torch
from transformers import DetrForObjectDetection, DetrImageProcessor
import lightning as l


class Detr(l.LightningModule):
    def __init__(
        self,
        n_classes=1,
        lr=1e-4,
        lr_backbone=1e-5,
        weight_decay=1e-4,
    ):
        super().__init__()
        backbone = "facebook/detr-resnet-50"
        kargs = {
            "revision": "no_timm",
            "ignore_mismatched_sizes": True,
            "num_labels": n_classes,
        }
        self.model = DetrForObjectDetection.from_pretrained(backbone, **kargs)
        self.processor = DetrImageProcessor.from_pretrained(backbone)
        self.lr = lr
        self.lr_backbone = lr_backbone
        self.weight_decay = weight_decay

    def forward(self, pixel_values, pixel_mask):
        outputs = self.model(
            pixel_values=pixel_values,
            pixel_mask=pixel_mask,
        )
        return outputs

    def common_step(self, batch, batch_idx):
        pixel_values = batch["pixel_values"]
        pixel_mask = batch["pixel_mask"]
        labels = [{k: v.to(self.device) for k, v in t.items()} for t in batch["labels"]]

        # forward pass
        outputs = self.model(
            pixel_values=pixel_values,
            pixel_mask=pixel_mask,
            labels=labels,
        )

        # calculate loss
        loss = outputs.loss
        loss_dict = outputs.loss_dict

        return loss, loss_dict, outputs, labels

    def training_step(self, batch, batch_idx):
        loss, loss_dict, _, _ = self.common_step(batch, batch_idx)
        self.log("train_loss", loss)
        for k, v in loss_dict.items():
            self.log("train_" + k, v.item())

        return loss

    def validation_step(self, batch, batch_idx):
        loss, loss_dict, _, _ = self.common_step(batch, batch_idx)
        self.log("val_loss", loss)
        for k, v in loss_dict.items():
            self.log("val_" + k, v.item())

        return loss

    def test_step(self, batch, batch_idx):
        pixel_values = batch["pixel_values"]
        outputs = self(pixel_values=pixel_values)
        # FIXME: this is not working
        loss, loss_dict, outputs, labels = self.common_step(batch, batch_idx)

        orig_target_sizes = torch.stack(
            [target["orig_size"] for target in labels], dim=0
        )
        results = self.processor.post_process_object_detection(
            outputs, target_sizes=orig_target_sizes
        )

        return results

    def predict_step(self, batch, batch_idx):
        pass

    def configure_optimizers(self):
        param_dicts = [
            # params for transformer
            {
                "params": [
                    p
                    for n, p in self.named_parameters()
                    if "backbone" not in n and p.requires_grad
                ]
            },
            # params for resnet
            {
                "params": [
                    p
                    for n, p in self.named_parameters()
                    if "backbone" in n and p.requires_grad
                ],
                "lr": self.lr_backbone,
            },
        ]
        optimizer = torch.optim.AdamW(
            param_dicts,
            lr=self.lr,
            weight_decay=self.weight_decay,
        )

        return optimizer


def convert_to_xywh(boxes):
    xmin, ymin, xmax, ymax = boxes.unbind(1)
    return torch.stack((xmin, ymin, xmax - xmin, ymax - ymin), dim=1)


def prepare_for_coco_detection(predictions):
    coco_results = []
    for original_id, prediction in predictions.items():
        if len(prediction) == 0:
            continue

        boxes = prediction["boxes"]
        boxes = convert_to_xywh(boxes).tolist()
        scores = prediction["scores"].tolist()
        labels = prediction["labels"].tolist()

        coco_results.extend(
            [
                {
                    "image_id": original_id,
                    "category_id": labels[k],
                    "bbox": box,
                    "score": scores[k],
                }
                for k, box in enumerate(boxes)
            ]
        )
    return coco_results
