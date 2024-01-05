"""The simulation module"""
import pandas as pd
from ..dataset.dataset_model import DatasetModel
from typing import Dict
from typing_extensions import Self
from zipfile import ZipFile


class Xlsx:
    def from_xlsx(
        self, filename: str, strict=False, datamodel: DatasetModel = None
    ) -> None:
        """Create a new Import XLSX class

        Parameters
        ----------
        filename: str
            name of simulation
        datamodel: DatasetModel, optional
            database model

        Examples
        --------
        >>> xls = Xlsx(filename="data/excel_file.xlsx", datamodel=data_model_from_json)
        """
        self._filename = filename
        self._datamodel = datamodel
        self._data = {}
        self._read(strict=strict)

    def from_pandas(self, dataset: Dict[str, pd.DataFrame]) -> None:
        """Create a new Import XLSX class with the dataset

        Parameters
        ----------
        dataset: Dict[str, pd.DataFrame]
            dictionary of panda dataframes

        Examples
        --------
        >>> xls = Xlsx(dataset=dicts_of_pd_dataframes)
        """
        self._data = dataset

    def _read(self, strict=False) -> Self:
        """read the xlsx file

        Parameters
        ----------
        strict: bool (optional)
            The required fields defined in datamodel are included. Requires datasetmodel
        Returns
        -------
        dictionary of panda dataframes
        """
        if self._datamodel is None:
            self._data = pd.read_excel(io=self._filename, sheet_name=None)
            return self
        else:
            self._data = {}
            for table_name in self._datamodel.table_names:
                try:
                    table = self._datamodel.get_table(table_name)
                    if not table:
                        raise ValueError(
                            f"Error. Could not find table {table_name} in excel file."
                        )
                    self._data[table_name] = pd.read_excel(
                        io=self._filename,
                        parse_dates=table.date_columns,
                        dtype=table.non_date_fields,
                        sheet_name=table_name,
                    )
                except ValueError:
                    print(
                        f"Error reading excel file in sheet '{table_name}'. Check value type and names are consistent."
                    )

                if strict:
                    if not set(table.required).issubset(self._data[table_name].columns):
                        raise ValueError(f"Missing columns in table: '{table_name}'")

                    for var in table.required:
                        if any(self._data[table_name][var].isnull()):
                            raise ValueError(
                                f"In table: '{table_name}', the column: {var} is required but contains empty or NA values."
                            )

            return self

    @property
    def dataset(self) -> Dict[str, pd.DataFrame]:
        return self._data

    def to_csv_zip(self, zip_filepath: str) -> None:
        """
        Writes DataFrame objects to an zip file of csv.

        Parameters:
            - zip_filepath (str): The name of the zip file to write.

        Returns:
            None
        """
        with ZipFile(zip_filepath, "x") as zip_file:
            for k in self.dataset.keys():
                df: pd.DataFrame = self.dataset[k]
                csv_data = df.to_csv(index=False)
                zip_file.writestr(k + ".csv", csv_data)
