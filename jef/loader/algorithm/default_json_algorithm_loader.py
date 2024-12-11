from abc import ABC
import json
from loader.classes.abstract_class.algorithm_loader import AlgorithmLoader
from loader.classes.json_class.algorithm.algorithm import Algorithm


class DefaultJSONAlgorithmLoader(AlgorithmLoader, ABC):
    file_path_key='file_path'
    def __init__(self, parameters_string: str):
        super().__init__(parameters_string)

    def load_info(self):
        with open(self.parameters[self.file_path_key], 'r') as file:
            data = json.load(file)
            return Algorithm(**data)