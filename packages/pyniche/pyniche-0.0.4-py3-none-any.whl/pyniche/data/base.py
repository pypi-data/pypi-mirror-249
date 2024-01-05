import lightning as L

from torch.utils.data import random_split, DataLoader
from datasets import concatenate_datasets, load_dataset


class BaseDataModule(L.LightningDataModule):
    """
    parameters
    ---
    dataname and configname: str
        local config file or repository name on the huggingface hub
    batch: int (default: 32, optional)
        batch size
    split_trainval: any (default: None, optional)
        two-element list
        if None, keep the default splits for train/val/test
        if a list of floats, e.g., [0.8, 0.2], then split the train/val with the given ratio
        if a list of ints, e.g., [100, 20], then split the train/val with the given number of samples

    """

    def __init__(
        self,
        dataname: str,
        configname: str = None,
        batch: int = 32,
        split_trainval: any = None,
    ):
        super().__init__()
        # input parameters
        self.dataname = dataname
        self.configname = configname
        self.batch = batch
        self.split_trainval = split_trainval
        # datasets
        self.dataset = {
            "train": None,
            "val": None,
            "test": None,
        }

    def prepare_data(self):
        # download
        pass

    def setup(self, stage: str):
        # Assign train/val datasets for use in dataloaders
        if stage == "fit":
            # load and re-distribute train/val
            data_train = load_dataset(self.dataname, self.configname, split="train")
            data_val = load_dataset(self.dataname, self.configname, split="validation")
            data_train, data_val = self.re_distribute(
                data_train,
                data_val,
                self.split_trainval,
            )
            # assign and set transforms
            self.dataset["train"] = data_train
            self.dataset["val"] = data_val
        if stage == "test":
            data_test = load_dataset(self.dataname, self.configname, split="test")
            self.dataset["test"] = data_test

    # loaders
    def train_dataloader(self):
        return DataLoader(
            self.dataset["train"].with_transform(self._transform_train),
            batch_size=self.batch,
            shuffle=True,
            pin_memory=True,
            collate_fn=self._collate_fn_train,
        )

    def val_dataloader(self):
        return DataLoader(
            self.dataset["val"].with_transform(self._transform_val),
            batch_size=self.batch,
            shuffle=False,
            pin_memory=True,
            collate_fn=self._collate_fn_val,
        )

    def test_dataloader(self):
        return DataLoader(
            self.dataset["test"].with_transform(self._transform_test),
            batch_size=self.batch,
            shuffle=False,
            pin_memory=True,
            collate_fn=self._collate_fn_test,
        )

    # additional methods
    def re_distribute(self, data_train, data_val, split_trainval):
        """
        split_trainval: list, [n_train, n_val]
        """
        if split_trainval is not None:
            # concatenate to get the full dataset
            data_full = concatenate_datasets([data_train, data_val])
            n = len(data_full)

            # check int (count) or float (ratio)
            if isinstance(split_trainval[0], float):
                n_train = int(split_trainval[0] * n)
                n_val = n - n_train
            else:
                n_train, n_val = split_trainval
            # if n_val is not proivded
            if n_val == -1:
                n_val = n - n_train

            # split
            if n_train + n_val == n:
                data_train, data_val = random_split(data_full, split_trainval)
            elif n_train + n_val < n:
                data_train, data_val = random_split(data_full, [n - n_val, n_val])
                data_train, _ = random_split(data_train, [n_train, n - n_train - n_val])
            elif n_train + n_val > n:
                print("The sum of train/val samples is larger than the total samples.")
                raise ValueError

        # return
        return data_train, data_val

    # need to be implemented
    def _collate_fn(self, batch):
        raise NotImplementedError

    def _collate_fn_train(self, batch):
        batch = self._collate_fn(batch)
        return batch

    def _collate_fn_val(self, batch):
        batch = self._collate_fn(batch)
        return batch

    def _collate_fn_test(self, batch):
        batch = self._collate_fn(batch)
        return batch

    def _transform_train(examples):
        return examples

    def _transform_val(examples):
        return examples

    def _transform_test(examples):
        return examples
