from abc import ABC
from loader.classes.abstract_class.dataset_loader import DatasetLoader
import math
import numpy as np
import pandas as pd
import os
import csv
from loader.classes.json_class.dataset.dataset import Dataset
from loader.classes.json_class.dataset.statistics.statistics import Statistics


def _convert_np(obj):
    if isinstance(obj, np.generic):
        return obj.item()
    return obj


def _format_size(size_in_bytes):
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_in_bytes, 1024))) if size_in_bytes > 0 else 0
    p = math.pow(1024, i)
    s = round(size_in_bytes / p, 2) if size_in_bytes > 0 else 0
    return f"{s} {size_name[i]}"


class CSVDatasetLoader(DatasetLoader, ABC):
    file_path_key='file_path'
    def __init__(self, parameters_string: str):
        super().__init__(parameters_string)

    def load_info(self):
        file_path=self.parameters[self.file_path_key]
        try:
            file_name = os.path.basename(file_path)

            with open(file_path, 'r', newline='') as csvfile:
                sample = csvfile.read(1024)
                try:
                    dialect = csv.Sniffer().sniff(sample)
                    delimiter = dialect.delimiter
                except csv.Error:
                    delimiter = ';'

            df = pd.read_csv(file_path, sep=delimiter, keep_default_na=False, header='infer')
            has_header = not df.columns.equals(pd.RangeIndex(start=0, stop=len(df.columns), step=1))
            column_names = list(df.columns) if has_header else list(range(len(df.columns)))

            null_chars = [char for char in ['', '?'] if df.isin([char]).any().any()]

            statistics = {
                "type": {},
                "mean": {},
                "median": {},
                "mode": {},
                "min": {},
                "max": {},
                "distribution": {}
            }

            for col in df.columns:
                if df[col].dtype == object:
                    lengths = df[col].str.len()
                    statistics["mean"][col] = round(lengths.mean(), 2)
                    statistics["median"][col] = round(lengths.median(), 2)
                    mode_values = lengths.mode()
                    statistics["mode"][col] = round(mode_values.iloc[0], 2) if not mode_values.empty else None
                    statistics["type"][col] = "string"
                    statistics["min"][col] = lengths.min()
                    statistics["max"][col] = lengths.max()
                else:
                    statistics["mean"][col] = round(float(df[col].mean()), 2)
                    statistics["median"][col] = round(float(df[col].median()), 2)
                    statistics["mode"][col] = round(df[col].mode().iloc[0], 2) if not df[col].mode().empty else None
                    statistics["type"][col] = df[col].dtype.name
                    statistics["min"][col] = df[col].min()
                    statistics["max"][col] = df[col].max()

                distribution = df[col].value_counts().to_dict()
                combined_distribution = {str(k): v for k, v in distribution.items()}
                statistics["distribution"][col] = combined_distribution

            statistics = {k: {key: _convert_np(value) for key, value in v.items()} if isinstance(v, dict) else v for k, v in statistics.items()}

            dataset = Dataset(
                name=file_name,
                size=_format_size(os.path.getsize(file_path)),
                file_format="CSV",
                header=column_names,
                col_number=len(df.columns),
                row_number=len(df),
                separator=delimiter,
                blank_char=", ".join(null_chars) if null_chars else None,
                statistics=Statistics(statistics["type"],
                                      statistics["mean"],
                                      statistics["median"],
                                      statistics["mode"],
                                      statistics["min"],
                                      statistics["max"],
                                      statistics["distribution"])
            )

            return dataset
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

