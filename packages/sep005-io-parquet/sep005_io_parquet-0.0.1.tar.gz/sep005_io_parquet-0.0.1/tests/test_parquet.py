import os
import sys

import pytest
from sdypy_sep005.sep005 import assert_sep005

import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sep005_io_parquet.parquet import read_parquet

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'static')
GOOD_FILES = os.listdir(os.path.join(static_dir, 'good'))


@pytest.mark.parametrize("filename", GOOD_FILES)
def test_compliance_sep005(filename):
    """
    Test the compliance with the SEP005 guidelines
    """
    file_path = os.path.join(static_dir, 'good', filename)
    signals = read_parquet(file_path)  # should already not crash here

    assert len(signals) != 0  # Not an empty response
    assert_sep005(signals)


