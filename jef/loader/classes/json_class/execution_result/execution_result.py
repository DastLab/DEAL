from loader.classes.json_class.execution_result.result.result import Result


class ExecutionResult:
    metadata_type: str
    scenario: str
    result: Result

    def __init__(self, metadata_type:str, scenario:str, result:Result):
        self.metadata_type = metadata_type
        self.scenario = scenario
        self.result = result