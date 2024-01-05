import pandas as pd
from typing_extensions import Self
from sqlalchemy import create_engine
import warnings


class DatasetReferenceData:
    def __init__(self) -> None:
        self._data: dict[str, pd.DataFrame] = {}

    def from_xlsx(self, xlsx_filepath: str) -> Self:
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            self._data = pd.read_excel(io=xlsx_filepath, sheet_name=None)
            self._clean()

    def to_mssql(self, server_name: str, database_name: str, schema_name: str) -> None:
        engine = create_engine(
            "mssql+pyodbc://@"
            + server_name
            + "/"
            + database_name
            + "?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server"
        )
        try:
            for key, df in self._data.items():
                print(f"writing table: [{schema_name}].[dict_{key}]")
                df.to_sql(
                    name=f"dict_{key}",
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

    def _clean(self) -> None:
        for key, df in self._data.items():
            self._whitespace_remover(self._data[key])

    def _whitespace_remover(self, df: pd.DataFrame) -> None:
        for col in df.columns:
            df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
