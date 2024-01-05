import json
import os
import pandas as pd
import pytest
from rn3 import Xlsx
from rn3 import DatasetModel


@pytest.fixture
def nitrate_dataset():
    ds = DatasetModel()
    return ds.from_json(json_filepath="tests/data/nitrate_schema.json")


@pytest.fixture
def filename_xlsx():
    return "tests/data/fake_italy_reporting_tiny.xlsx"


@pytest.fixture
def zip_file(tmpdir_factory, filename_xlsx):
    outfile = tmpdir_factory.mktemp("data").join("xlsx.zip")
    xlsx = Xlsx()
    xlsx.from_xlsx(filename=filename_xlsx)
    xlsx.to_csv_zip(outfile)
    return outfile


def test_read_xlsx_without_schema(filename_xlsx):
    xlsx = Xlsx()
    xlsx.from_xlsx(filename=filename_xlsx)
    assert xlsx is not None


def test_read_pandas(filename_xlsx):
    df = pd.read_excel(filename_xlsx)
    xlsx = Xlsx()
    xlsx.from_pandas(dataset=df)
    assert xlsx is not None


def test_read_xlsx_with_schema(nitrate_dataset, filename_xlsx):
    xlsx = Xlsx()
    xlsx.from_xlsx(filename=filename_xlsx, datamodel=nitrate_dataset)
    assert xlsx is not None


def test_write_xlsx_to_zip(zip_file):
    assert os.path.isfile(zip_file)
