import pytest

import os
import wfdb
import numpy as np

from pathlib import Path
from zipfile import ZipFile

from ecgdatasets.datasets.physionet.ptbxl import PTBXL

@pytest.mark.ptbxl
@pytest.mark.physionet
def test_PTBXL_CASE_create_AND_no_exist():
    msg = 'Dataset not found. You can use download=True to download it.'

    with pytest.raises(RuntimeError, match=msg):
        PTBXL('', '1.0.3', download=False, mapper=None)

@pytest.mark.ptbxl
@pytest.mark.physionet
@pytest.mark.skipif(os.getenv('EDSLOAD', None) is None, reason='Set EDSLOAD to run tests.')
def test_PTBXL_CASE_create_version_1_0_3():
    datadir = Path(__file__).parent.parent.parent.parent / 'files'

    dataset = PTBXL(datadir, '1.0.3', download=True, mapper=None)

    assert len(dataset) == 21799

    with ZipFile(dataset._zippath, 'r') as zf:
        for path in zf.namelist():
            if 'records500' in path:
                path = Path(path)

                if path.suffix == '.dat':
                    datpath = path
                    heapath = path.with_suffix('.hea')

                    ecg = zf.read(str(datpath))
                    header = zf.read(str(heapath))

                    name = int(path.stem[:-3])

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
