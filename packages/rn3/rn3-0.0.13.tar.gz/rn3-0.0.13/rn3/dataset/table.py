import json
import numpy as np
from .item import Item
from typing import List


class Table:
    def __init__(self, table_json: json) -> None:
        """Create a new Table class

        Args:
            table_json (json): json object of the table.

        """
        self._schema = table_json["recordSchema"]["fieldSchema"]
        self._name = table_json["nameTableSchema"]
        self._column_names_and_type = self._get_column_names_and_type()
        self._items = self._read_items(
            table_json=table_json["recordSchema"]["fieldSchema"]
        )

    def __repr__(self) -> str:
        return "Table (" + self.name + ")"

    @property
    def name(self) -> str:
        return self._name

    @property
    def column_names_and_type(self) -> dict[str, object]:
        return self._column_names_and_type

    @property
    def columns(self) -> list[str]:
        return list(self._column_names_and_type.keys())

    @property
    def items(self) -> list[Item]:
        return self._items

    @property
    def required(self) -> list[str]:
        return [s["name"] for s in self._schema if s["required"]]

    @property
    def date_columns(self) -> list[str]:
        return [
            k
            for k in self.column_names_and_type.keys()
            if self.column_names_and_type[k] == "DATE"
        ]

    @property
    def non_date_fields(self) -> dict[str, object]:
        return dict(
            filter(lambda kv: kv[1] != "DATE", self.column_names_and_type.items())
        )

    def _get_column_names_and_type(self) -> dict[str, object]:
        names_and_type = {}
        for s in self._schema:
            name = s.get("name")
            v = s.get("type")
            if v == "LINK" or v == "TEXT" or v == "CODELIST":
                v = str
            elif v == "NUMBER_DECIMAL":
                v = np.float64
            elif v == "NUMBER_INTEGER":
                v = "Int64"
            # elif v == "DATE":
            #    v = datetime
            names_and_type[name] = v
        return names_and_type

    def _read_items(self, table_json: json) -> List[Item]:
        items = []
        for item in table_json:
            items.append(Item(item_json=item))
        return items

    @property
    def sql_create_cmd(self) -> str:
        sql_cmd = "USE [DATABASE_NAME]\n"
        sql_cmd += "GO\n"
        sql_cmd += "SET ANSI_NULLS ON\n"
        sql_cmd += "GO\n"
        sql_cmd += "SET QUOTED_IDENTIFIER ON\n"
        sql_cmd += "GO\n"
        sql_cmd += f"CREATE TABLE [SCHEMA_NAME].[{self.name}](\n"

        # if any(i.name == "Id" for i in self.items):
        sql_cmd += "\t[Id] [int] IDENTITY(1,1) NOT NULL,\n"
        for item in self.items:
            if not item.name == "Id":
                sql_cmd += "\t" + item.sql_create_cmd + "\n"

        sql_cmd += "\t[ReportNet3HistoricReleaseId] [int] NOT NULL,\n"

        sql_cmd += f"CONSTRAINT [PK_{self.name}_1] PRIMARY KEY CLUSTERED\n"
        sql_cmd += "(\n"

        sql_cmd += "\t[Id] ASC\n"
        sql_cmd += ")WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]\n"
        sql_cmd += ") ON [PRIMARY]\n"
        sql_cmd += "GO\n"

        sql_cmd += f"ALTER TABLE [SCHEMA_NAME].[{self.name}]  WITH NOCHECK ADD  CONSTRAINT [FK_{self.name}_ReportNet3HistoricReleases] FOREIGN KEY([ReportNet3HistoricReleaseId])\n"
        sql_cmd += "REFERENCES [metadata].[ReportNet3HistoricReleases] ([Id])\n"
        sql_cmd += "ON DELETE CASCADE\n"
        sql_cmd += "GO\n"

        sql_cmd += f"ALTER TABLE [SCHEMA_NAME].[{self.name}] CHECK CONSTRAINT [FK_{self.name}_ReportNet3HistoricReleases]\n"
        sql_cmd += "GO\n"

        return sql_cmd

    @property
    def sqlalchemy_class(self) -> str:
        sql_cmd = f"class {self.name}(Base):\n"
        sql_cmd += f"\t__tablename__ = '{self.name.lower()}'\n"
        sql_cmd += "\t__table_args__ = {'schema': 'SCHEMA_NAME'}\n"
        sql_cmd += "\t\n"
        sql_cmd += "\tId = Column(Integer, primary_key=True)\n"
        for item in self.items:
            if not item.name == "Id":
                sql_cmd += f"\t{item.sqlalchemy_column}\n"
        sql_cmd += "\tReportNet3HistoricReleaseId = Column(Integer, ForeignKey('metadata.ReportNet3HistoricReleases.Id'))\n"
        sql_cmd += "\tReportNet3HistoricReleases = relationship('ReportNet3HistoricReleases')\n"
        return sql_cmd
