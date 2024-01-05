# native imports
import os

# torch imports
import torch
import lightning.pytorch as pl
from lightning.pytorch.callbacks import ModelCheckpoint
from lightning.pytorch.loggers import TensorBoardLogger

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class NicheTrainer:
    def __init__(self):
        # core
        self.model = None  # lightning module
        self.data = None  # lightning data module
        self.trainer = None  # lightining trainer

        # outputs
        self.loggers = None  # lightning loggers
        self.callbacks = None  # lightning callbacks
        self.out = dict(
            {
                "dir": None,
                "best_loss": None,
                "best_path": None,
            }
        )

    def set_model(
        self,
        model_class: pl.LightningModule,
        model_checkpoint: str = None,
        **kwargs,  # varied arguments for the model
    ):
        """
        parameters
        ---
        model_class: l.LightningModule
            the lightning module class, e.g., transformers.DetrModel
        model_pretrained: str
            path to the pretrained model, e.g., facebook/detr-resnet-50
        model_checkpoint: str
            local path to the checkpoint, e.g., model.ckpt
        model_config: any
            model configuration, e.g., transformers.DetrConfig

        examples
        ---

        """
        if model_checkpoint:
            self.model = model_class.load_from_checkpoint(
                model_checkpoint,
                **kwargs,
            )
        else:
            self.model = model_class()
        self.model.to(DEVICE)

    def set_data(
        self,
        dataclass: pl.LightningDataModule,
        **kwargs,  # varied arguments for the dataclass
    ):
        self.data = dataclass(**kwargs)

    def set_out(
        self,
        dir_out: str,
    ):
        self.out["dir"] = dir_out
        if not os.path.exists(self.out["dir"]):
            os.makedirs(self.out["dir"])

    def fit(
        self,
        epochs: int = 100,
    ):
        self.loggers = get_logger(self.out["dir"])
        self.callbacks = get_checkpoint(self.out["dir"])
        self.trainer = pl.Trainer(
            max_epochs=epochs,
            callbacks=self.callbacks,
            logger=self.loggers,
        )
        self.trainer.fit(self.model, self.data)

    def val(self):
        self.trainer = pl.Trainer()
        out = self.trainer.validate(self.model, self.data)
        return out

    def get_best_loss(
        self,
        rm_threshold: float = 1e5,
    ):
        self.out["best_loss"] = self.callbacks.best_model_score.item()
        self.out["best_path"] = self.callbacks.best_model_path
        if self.out["best_loss"] > rm_threshold:
            os.remove(self.out["best_path"])
        return self.out["best_loss"]


def get_logger(dir_out):
    # training configuration
    logger = TensorBoardLogger(
        save_dir=dir_out,
        name=".",  # will not create a new folder
        version=".",  # will not create a new folder
        log_graph=True,  # for model architecture visualization
        default_hp_metric=False,
    )  # output: save_dir/name/version/hparams.yaml
    return logger


def get_checkpoint(dir_out):
    checkpoint_callback = ModelCheckpoint(
        monitor="val_loss",
        dirpath=dir_out,
        mode="min",
        save_top_k=1,
        verbose=False,
        save_last=False,
        filename="model-{val_loss:.3f}",
    )
    return checkpoint_callback
