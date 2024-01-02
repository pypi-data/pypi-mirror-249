import warnings
from collections.abc import Generator

from torch.utils.data import DataLoader, Dataset


class DummyDataset(Dataset):
    def __getitem__(self, index: int) -> Generator[None, None, None]:
        yield None

    def __len__(self) -> int:
        return 1


class DummyLoader(DataLoader):
    def __init__(self):
        warnings.filterwarnings("ignore", message=".*does not have many workers.*")
        super().__init__(DummyDataset(), collate_fn=lambda x: x)
