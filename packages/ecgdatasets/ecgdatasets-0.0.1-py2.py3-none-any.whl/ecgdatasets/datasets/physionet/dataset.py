import hashlib

from tqdm import tqdm
from requests import get

import ecgdatasets.datasets.misc as M

from ecgdatasets.core import EcgDataset

class PhysioNetDataset(EcgDataset):
    """Base class for making datasets from PhysioNet source.
    """
    _template_url = 'https://www.physionet.org/static/published-projects/{}/{}-{}.zip'

    def __init__(
        self,
        root,
        version,
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
        super().__init__(root, download, mapper)
        self.version = version

        if download:
            self.download()

        if not self._check_integrity():
            raise RuntimeError('Dataset not found. You can use download=True to download it.')

        self.data = self._load_data()

    @property
    def _name(self):
        """
            :return:
                shortname of the dataset
        """
        raise NotImplementedError

    @property
    def _fullname(self):
        """
            :return:
                dataset name according to physionet
        """
        raise NotImplementedError

    @property
    def _zippath(self):
        return self.root / ( self._name + '-' + self.version + '.zip' )

    @property
    def _hash(self):
        raise NotImplementedError

    @property
    def _url(self):
        return self._template_url.format(self._name, self._fullname, self.version)

    def _check_integrity(self):
        return M._check_integrity(self._zippath, self._hash, M._calculate_md5)

    def download(self):
        if self._check_integrity():
            return

        req = get(self._url, stream=True)

        if req.status_code == 200:
            if not self._zippath.parent.is_dir():
                self._zippath.parent.mkdir(parents=True, exist_ok=True)

            length = (int(req.headers['Content-Length']) + 127) // 128

            with open(self._zippath, 'wb') as f:
                for chunk in tqdm(req, total=length):
                    f.write(chunk)
        else:
            raise RuntimeError('Remote resourse {} is not avialable.'.format(self._url))

    def _load_data(self):
        """
            :return:
                data that loaded from physionet archive
        """
        raise NotImplementedError
