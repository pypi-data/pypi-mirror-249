import json
import requests
from typing import Optional, Union
from typing_extensions import Self
from sqlalchemy import create_engine
from .table import Table
import pandas as pd


class DatasetModel:
    def __init__(self) -> None:
        self._tables = []
        self._name = ""

    def __repr__(self) -> str:
        return "Dataset (" + self.name + ")"

    @property
    def name(self) -> str:
        return self._name

    def from_json(self, json_filepath: str) -> Self:
        json_data = json.load(open(json_filepath))
        self._tables = []
        self._name = json_data["nameDatasetSchema"]
        for table in json_data["tableSchemas"]:
            self._tables.append(Table(table))
        return self

    def from_url(
        self,
        dataset_id: Union[int, str],
        api_key: str,
        base_url: str = "https://api-reportnet.europa.eu",
    ) -> Self:
        headers = {"Authorization": api_key}
        endpoint = base_url + r"/dataschema/v1/datasetId/" + str(dataset_id)
        request = requests.get(endpoint, headers=headers)
        if not request.ok:
            raise Exception(
                f"Status Code: {request.status_code}. Could not retrieve schema with GET: {endpoint}."
            )
        json_data = request.json()
        self._tables = []
        self._name = json_data["nameDatasetSchema"]
        for table in json_data["tableSchemas"]:
            self._tables.append(Table(table))
        return self

    def sql_cmd(self, database_name=None, schema_name=None) -> str:
        sql_cmd = ""
        for table in self.tables:
            sql_cmd += "\n"
            tbl_cmd = table.sql_create_cmd
            if database_name is not None:
                tbl_cmd = tbl_cmd.replace("DATABASE_NAME", database_name)
            if schema_name is not None:
                tbl_cmd = tbl_cmd.replace("SCHEMA_NAME", schema_name)
            sql_cmd += str(tbl_cmd)
            sql_cmd += "\n"
        return sql_cmd

    def sqlalchemy_generate_models(self, schema_name=None) -> str:
        sql_cmd = "from sqlalchemy import Column, ForeignKey, Boolean, Date, DateTime, Float, Integer, String\n"
        sql_cmd += "from sqlalchemy.orm import declarative_base, relationship\n"
        sql_cmd += "from sqlalchemy.dialects.mssql import NVARCHAR, TEXT\n"
        sql_cmd += "\nBase = declarative_base()\n"
        sql_cmd += "\n"

        sql_cmd += "class ReportNet3HistoricReleases(Base):\n"
        sql_cmd += "\t__tablename__ = 'ReportNet3HistoricReleases'\n"
        sql_cmd += "\t__table_args__ = {'schema': 'metadata'}\n\n"

        sql_cmd += "\tId = Column(Integer, primary_key=True)\n"
        sql_cmd += "\tcountryCode = Column(NVARCHAR(2), nullable=False)\n"
        sql_cmd += "\tReportNet3DataflowId = Column(Integer, nullable=False)\n"
        sql_cmd += "\tReportNet3EuDatasetId = Column(Integer, nullable=True)\n"
        sql_cmd += "\tdataURL = Column(NVARCHAR(100), nullable=False)\n"
        sql_cmd += "\treleaseDate = Column(DateTime, nullable=False)\n"
        sql_cmd += "\tisLatestRelease = Column(Boolean, nullable=False)\n"
        sql_cmd += "\tfmeJobId = Column(Boolean, nullable=True)\n"
        sql_cmd += "\tfmeJobStartedAt = Column(DateTime, nullable=True)\n"
        sql_cmd += "\tfmeSuccess = Column(Boolean, nullable=True)\n"
        sql_cmd += "\tfmeErrorLog = Column(NVARCHAR(1000), nullable=True)\n"
        sql_cmd += "\n"

        for table in self.tables:
            sql_cmd += "\n"
            tbl_cmd = table.sqlalchemy_class
            if schema_name is not None:
                tbl_cmd = tbl_cmd.replace("SCHEMA_NAME", schema_name)

            sql_cmd += str(tbl_cmd)
            sql_cmd += "\n"
        return sql_cmd

    def sql_codelist_data(
        self, server_name: str, database_name: str, schema_name: str
    ) -> None:
        for table in self.tables:
            for item in table.items:
                if "CODELIST" in item._rn3_type:
                    items = item._code_list_items
                    ids = list(range(1, len(items) + 1))
                    df = pd.DataFrame({"Id": ids, "Value": items})
                    self._write_table(
                        server_name, database_name, schema_name, item.name, df
                    )

    def _write_table(
        self,
        server_name: str,
        database_name: str,
        schema_name: str,
        table_name: str,
        df: pd.DataFrame,
    ):
        engine = create_engine(
            "mssql+pyodbc://@"
            + server_name
            + "/"
            + database_name
            + "?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
        )
        try:
            print(f"writing table: [{schema_name}].[dict_{table_name}]")
            df.to_sql(
                name=f"dict_{table_name}",
                schema=schema_name,
                con=engine,
                if_exists="replace",
                index=False,
            )
        except Exception:
            print(
                "Error. Make sure executing on a computer with the database \
                server and windows authentication provides you 'Owner' \
                privileges."
            )

    @property
    def table_names(self) -> list[str]:
        """Returns a list of table names.

        Returns:
            A list of table names extracted from the input tables.

        """
        return [table.name for table in self._tables]

    @property
    def tables(self) -> list[Table]:
        """Returns a list table objects.

        Returns:
            A list of table objects.
        """
        return self._tables

    def remove_table(self, table_name: str) -> Self:
        table = self.get_table(table_name=table_name)
        if table is None:
            raise ValueError(f"Cannot fine table {table_name} in dataset")
        self._tables.remove(table)
        return self

    def get_table(self, table_name: str) -> Optional[Table]:
        return next((t for t in self._tables if t.name == table_name), None)
