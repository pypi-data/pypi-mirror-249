from pathlib import Path
from torch.utils.data import Dataset

class EcgDataset(Dataset):
    """Base class for making datasets which are compatible with ecgdatasets.
       It is necessary to override the ``__getitem__`` and ``__len__`` method.
    """

    _repr_indent = 4

    _default_channel_order = [
        'i', 'ii', 'iii', 'avr', 'avl', 'avf', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6'
    ]

    def __init__(
        self,
        root,
        download=False,
        mapper=None,
        ):
        """
            :args:
                root (string): root directory of dataset.
                download (bool):  If true, downloads the dataset from the internet and
                    puts it in root directory. If dataset is already downloaded, it is
                    not downloaded again.
                mapper(callable or None):   function to transform targets. If None, it
                    is used default mapper.
        """
        self.root = Path(root).expanduser()
        self.mapper = mapper

    @property
    def frequency(self):
        """
            :return:
                the original frequency of the dataset
        """
        raise NotImplementedError

    def __getitem__(self, idx):
        """
            :args:
                idx (int): index of an accessed dataset item

            :return:
                ...
        """
        raise NotImplementedError

    def __len__(self):
        """
            :return:
                the length of the dataset
        """
        raise NotImplementedError

    def __repr__(self):
        """
            :return:
                the string representation of the dataset
        """
        head = 'Dataset ' + self.__class__.__name__
        body = [f'Number of datapoints: {self.__len__()}']

        if self.root is not None:
            body.append(f'Root location: {self.root}')

        body += self.extra_repr().splitlines()

        lines = [head] + [' ' * self._repr_indent + line for line in body]
        return '\n'.join(lines)

    def extra_repr(self):
        return ''
