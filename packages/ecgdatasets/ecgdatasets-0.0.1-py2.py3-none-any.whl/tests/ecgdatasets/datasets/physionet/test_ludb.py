import pytest

import os
import wfdb
import numpy as np

from pathlib import Path
from zipfile import ZipFile

from ecgdatasets.datasets.physionet.ludb import LUDB

@pytest.mark.ludb
@pytest.mark.physionet
def test_LUDB_CASE_create_AND_no_exist():
    msg = 'Dataset not found. You can use download=True to download it.'

    with pytest.raises(RuntimeError, match=msg):
        LUDB('', '1.0.1', download=False, mapper=None)

@pytest.mark.ludb
@pytest.mark.physionet
@pytest.mark.skipif(os.getenv('EDSLOAD', None) is None, reason='Set EDSLOAD to run tests.')
def test_LUDB_CASE_create_version_1_0_1():
    datadir = Path(__file__).parent.parent.parent.parent / 'files'

    dataset = LUDB(datadir, '1.0.1', download=True, mapper=None)

    assert len(dataset) == 200

    with ZipFile(dataset._zippath, 'r') as zf:
        for path in zf.namelist():
            path = Path(path)

            if path.suffix == '.dat':
                datpath = path
                heapath = path.with_suffix('.hea')

                ecg = zf.read(str(datpath))
                header = zf.read(str(heapath))

                name = int(path.stem)

                with open(datadir / datpath.name, 'wb') as f:
                    f.write(ecg)

                with open(datadir / heapath.name, 'wb') as f:
                    f.write(header)

                wfdbdatum = wfdb.rdsamp(datadir / datpath.stem)[0]

                (datadir / datpath.name).unlink()
                (datadir / heapath.name).unlink()

                datum = dataset.data[name]

                assert datum.shape == wfdbdatum.shape
                assert np.allclose(datum, wfdbdatum)
