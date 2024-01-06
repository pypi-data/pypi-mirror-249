import numpy as np

from pathlib import Path
from zipfile import ZipFile

from ecgdatasets.datasets.physionet.dataset import PhysioNetDataset

class LUDB(PhysioNetDataset):
    """LUDB. Read more in https://physionet.org/content/ludb/
    """
    default_version = '1.0.1'

    allowed_versions = [
        '1.0.1',
    ]

    hashs = {
        '1.0.1': '83dbe47af910488f05759b3e368babc1',
    }

    _raw_channel_order = [
        'i', 'ii', 'iii', 'avr', 'avl', 'avf', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6'
    ]

    def __init__(
        self,
        root,
        version=default_version,
        download=False,
        mapper=None,
        ):
        """
            :args:
                root (string): root directory of dataset.
                version (string): version of dataset for usage.
                download (bool):  If true, downloads the dataset from the internet and
                    puts it in root directory. If dataset is already downloaded, it is
                    not downloaded again.
                mapper(callable or None):   function to transform targets. If None, it
                    is used default mapper.
        """
        version = version if version in self.allowed_versions else self.default_version
        super().__init__(root, version, download, mapper)

    @property
    def frequency(self):
        return 500

    def __getitem__(self, idx):
        key = [*self.data.keys()][idx]

        return self.data[key]

    def __len__(self):
        return len(self.data)

    def extra_repr(self):
        return ''

    @property
    def _name(self):
        return 'ludb'

    @property
    def _fullname(self):
        return 'lobachevsky-university-electrocardiography-database'

    @property
    def _hash(self):
        return self.hashs[self.version]

    def _load_data(self):
        data = dict()

        with ZipFile(self._zippath, 'r') as zf:
            for path in zf.namelist():
                path = Path(path)

                if path.suffix == '.dat':
                    datpath = path
                    heapath = path.with_suffix('.hea')

                    ecg = zf.read(str(datpath))
                    ecg = np.frombuffer(ecg, np.int16)
                    ecg.shape = (5000, 12)

                    header = zf.read(str(heapath))

                    gains, baselines = [], []

                    for s in header.decode().split('\n')[1:13]:
                        s = s.split(' ')[2]
                        s = s.split('/')[0]
                        s = s.split(')')[0]

                        gain, baseline = s.split('(')

                        gains.append(int(gain))
                        baselines.append(int(baseline))

                    gains = np.array(gains)
                    baselines = np.array(baselines)

                    data[int(path.stem)] = (ecg - baselines) / gains

        return data
