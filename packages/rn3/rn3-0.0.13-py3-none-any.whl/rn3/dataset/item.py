import json
import numpy as np


class Item:
    def __init__(self, item_json: json) -> None:
        """Create a new Item class

        Args:
            item_json (json): json object of the item.

        """
        self._json_data = item_json
        self._id = item_json.get("id")
        name = item_json.get("name")
        if name.lower() == "id":
            name = name + "_field"
        self._name = name
        self._rn3_type = item_json.get("type")
        self._required = item_json.get("required")
        self._pk = item_json.get("pk")
        self._id_record = item_json.get("idRecord")
        self._code_list_items = item_json.get("codelistItems")
        self._multiple_values = item_json.get("pkHasMultipleValues")

        referenced_field = item_json.get("referencedField")
        if referenced_field is not None:
            self._read_referenced_field(item_json=item_json)

    def _read_referenced_field(self, item_json: json):
        self._referenced_field = item_json.get("referencedField")

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

    @property
    def sql_create_cmd(self) -> str:
        sql_type = ""
        if self._rn3_type in [
            "LINK",
            "CODELIST",
            "NUMBER_INTEGER",
            "URL",
        ]:
            sql_type = "[int]"
        elif self._rn3_type == "NUMBER_DECIMAL":
            sql_type = "[float]"
        elif self._rn3_type == "TEXT":
            sql_type = "[nvarchar](500)"
        elif self._rn3_type == "TEXTAREA":
            sql_type = "[text]"
        elif self._rn3_type in ["URL", "MULTISELECT_CODELIST", "EMAIL"]:
            sql_type = "[nvarchar](500)"
        elif self._rn3_type == "ATTACHMENT":
            sql_type = "[varbinary](MAX)"
        elif self._rn3_type == "DATE":
            sql_type = "[date]"
        else:
            raise Warning(
                f"In item '{self.name}' has unsuported type '{self._rn3_type}'"
            )

        sql_cmd = f"[{self._name}] {sql_type}"

        if self._required:
            sql_cmd += " NOT NULL,"
        else:
            sql_cmd += " NULL,"
        return sql_cmd

    @property
    def sqlalchemy_column(self) -> str:
        sql_type = ""
        if self._rn3_type in [
            "LINK",
            "CODELIST",
            "NUMBER_INTEGER",
            "URL",
        ]:
            sql_type = "Integer"
        elif self._rn3_type == "NUMBER_DECIMAL":
            sql_type = "Float"
        elif self._rn3_type == "TEXT":
            sql_type = "NVARCHAR(500)"
        elif self._rn3_type == "TEXTAREA":
            sql_type = "TEXT"
        elif self._rn3_type in ["URL", "MULTISELECT_CODELIST", "EMAIL"]:
            sql_type = "NVARCHAR(500)"
        elif self._rn3_type == "ATTACHMENT":
            sql_type = "LargeBinary"
        elif self._rn3_type == "DATE":
            sql_type = "Date"
        else:
            raise Warning(
                f"In item '{self.name}' has unsuported type '{self._rn3_type}'"
            )

        s = f"{self.name} = Column({sql_type}"
        if self._pk:
            s += ", primary_key=True"
        if self._required:
            s += ", nullable=True"
        else:
            s += ", nullable=False"
        s += ")"
        return s

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
