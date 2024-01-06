import pytest

import ecgdatasets.datasets.misc as M

def test__check_integrity_CASE_no_file():
    output = M._check_integrity('no_file', 'hash', M._calculate_md5)
    expected = False

    assert output == expected
