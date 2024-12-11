from typing import Final

from loader.classes.abstract_class.algorithm_loader import AlgorithmLoader
from loader.classes.abstract_class.dataset_loader import DatasetLoader
from loader.classes.abstract_class.execution_result_loader import ExecutionResultLoader
from loader.classes.abstract_class.extra_data_loader import ExtraDataLoader
from loader.classes.abstract_class.final_operation import FinalOperation
from loader.classes.abstract_class.run_info_loader import RunInfoLoader
from loader.classes.json_class.discovery_info import DiscoveryInfo


class Loader:
    dataset_loader:(DatasetLoader, None)
    algorithm_loader:(AlgorithmLoader, None)
    run_info_loader:(RunInfoLoader, None)
    execution_result_loader:(ExecutionResultLoader, None)
    extra_data_loader:(ExtraDataLoader, None)
    final_operation:(FinalOperation,None)

    def __init__(self, dataset_loader:DatasetLoader = None,
                 algorithm_loader:AlgorithmLoader = None,
                 run_info_loader:RunInfoLoader = None,
                 execution_result_loader:ExecutionResultLoader = None,
                 extra_data_loader:ExtraDataLoader = None,
                 final_operation:FinalOperation=None):
        self.dataset_loader = dataset_loader
        self.algorithm_loader = algorithm_loader
        self.run_info_loader = run_info_loader
        self.execution_result_loader = execution_result_loader
        self.extra_data_loader = extra_data_loader
        self.final_operation = final_operation

    def load(self) -> DiscoveryInfo:
        dataset = self.dataset_loader.load_info() if self.dataset_loader else None
        algorithm = self.algorithm_loader.load_info() if self.algorithm_loader else None
        run_info = self.run_info_loader.load_info() if self.run_info_loader else None
        extra_data = self.extra_data_loader.load_info() if self.extra_data_loader else None
        execution_result = self.execution_result_loader.load_info() if self.execution_result_loader else None
        discovery_info = DiscoveryInfo(dataset, algorithm, execution_result, run_info, extra_data)
        if self.final_operation:
            discovery_info=self.final_operation.edit(discovery_info)
        return discovery_info






