import pytest
import os
import json
from rn3 import DatasetModel, DatasetReferenceData, Table


@pytest.fixture
def nitrate_json_file_path():
    return "tests/data/nitrate_schema.json"


@pytest.fixture
def pam_json_file_path():
    return "tests/data/pam_schema.json"


@pytest.fixture
def nitrate_dataset(nitrate_json_file_path):
    ds = DatasetModel()
    return ds.from_json(json_filepath=nitrate_json_file_path)


def test_read_json_ok(nitrate_json_file_path):
    ds = DatasetModel()
    ds.from_json(json_filepath=nitrate_json_file_path)
    assert ds is not None
    assert isinstance(ds.table_names, list)


def test_create_table_sql_cmd_ok(pam_json_file_path):
    ds = DatasetModel()
    ds.from_json(json_filepath=pam_json_file_path)
    sql_cmd = ds.sql_cmd(database_name="EnergyCommunity", schema_name="annex_XXIV")
    assert sql_cmd is not ""


@pytest.mark.skip(reason="Github has not sandbox access")
def test_read_url_ok():
    ds = DatasetModel()
    ds.from_url(
        dataset_id=20822,
        api_key="ApiKey d79237c1-8942-44b9-b6df-2ef20fca66a4",
        base_url=r"https://sandbox-api.reportnet.europa.eu",
    )
    assert ds is not None
    assert isinstance(ds.table_names, list)


@pytest.mark.skip(reason="MSSQL Server uses Windows Authentication")
def test_create_sql_table_ok():
    dsrd = DatasetReferenceData()
    dsrd.from_xlsx(xlsx_filepath="tests/data/Reference Dataset - Reference data.xlsx")
    dsrd.to_mssql("osprey", "EnergyCommunity", "annex_XXIV")


@pytest.mark.skip(reason="MSSQL Server uses Windows Authentication")
def test_create_sql_codelist_data_ok():
    dsrd = DatasetReferenceData()
    dsrd.from_xlsx(xlsx_filepath="tests/data/Reference Dataset - Reference data.xlsx")
    dsrd.to_mssql("osprey", "EnergyCommunity", "annex_XXIV")


def test_get_table_found(nitrate_dataset):
    table = nitrate_dataset.get_table("NiD_GW_Conc")
    assert table is not None


def test_get_table_not_found(nitrate_dataset):
    table = nitrate_dataset.get_table("Does not exist")
    assert table is None


def test_remove_table(nitrate_dataset):
    nitrate_dataset.remove_table("NiD_GW_Conc")
    table = nitrate_dataset.get_table("NiD_GW_Conc")
    assert table is None
