from loader.classes.json_class.algorithm.algorithm import Algorithm
from loader.classes.json_class.dataset.dataset import Dataset
from loader.classes.json_class.execution_result.execution_result import ExecutionResult
from loader.classes.json_class.run_info.run_info import RunInfo


class DiscoveryInfo:
    dataset: (Dataset, None)
    algorithm: (Algorithm, None)
    execution_result: (ExecutionResult, None)
    run_info: (RunInfo, None)
    extra_data: (dict, None)

    def __init__(self, dataset: Dataset, algorithm: Algorithm, execution_result: ExecutionResult, run_info: RunInfo, extra_data: dict):
        self.dataset = dataset
        self.algorithm = algorithm
        self.execution_result = execution_result
        self.run_info = run_info
        self.extra_data = extra_data
        