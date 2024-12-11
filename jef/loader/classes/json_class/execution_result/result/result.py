from loader.classes.json_class.execution_result.result.additional_info.additional_info import AdditionalInfo
from loader.classes.json_class.execution_result.result.data.data import Data
from loader.classes.json_class.execution_result.result.error.error import Error
from loader.classes.json_class.execution_result.result.execution_time.execution_time import ExecutionTime
from loader.classes.json_class.execution_result.result.ram_usage.ram_usage import RamUsage


class Result:
    execution_time: ExecutionTime
    ram_usage: RamUsage
    error: Error
    additional_info: AdditionalInfo
    data: list[Data]

    def __init__(self, execution_time: ExecutionTime, ram_usage: RamUsage, error: Error, additional_info: AdditionalInfo,
                 data: list[Data]):
        self.execution_time = execution_time
        self.ram_usage = ram_usage
        self.error = error
        self.additional_info = additional_info
        self.data = data