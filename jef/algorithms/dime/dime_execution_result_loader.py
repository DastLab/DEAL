from abc import ABC
import json
from loader.classes.abstract_class.execution_result_loader import ExecutionResultLoader
from loader.classes.json_class.execution_result.execution_result import ExecutionResult
from loader.classes.json_class.execution_result.result.additional_info.additional_info import AdditionalInfo
from loader.classes.json_class.execution_result.result.data.attribute import Attribute
from loader.classes.json_class.execution_result.result.data.data import Data
from loader.classes.json_class.execution_result.result.error.error import Error
from loader.classes.json_class.execution_result.result.execution_time.execution_time import ExecutionTime
from loader.classes.json_class.execution_result.result.ram_usage.ram_usage import RamUsage
from loader.classes.json_class.execution_result.result.result import Result
import re


def _cast_time_to_ms(time_string):
    time_string=time_string.replace("...", "").replace("in", "").replace("(too slow!)", "").strip()
    value=""
    if time_string.endswith("ms"):
        value=time_string.replace("ms","").replace(",",".").strip()
    elif time_string.endswith("s"):
        value=float(time_string.replace("s","").replace(",",".").strip())*1000
    elif time_string.endswith("min") or time_string.endswith("m"):
        value=float(time_string.replace("min","").replace("m","").replace(",",".").strip())*60000
    return str(value)


def _find_index(lines, search, start_with=True):
    i = 0
    found = False
    for line in lines:
        line = line.strip()
        if start_with:
            found = line.startswith(search)
        else:
            found = line==search
        if found:
            break
        i+=1
    return i if found else None


def _find_value(lines, search, start_with=True):
    i = _find_index(lines, search, start_with)
    if i:
        return lines[i].replace(search, "").strip()

    else:
        return None


def _load_execution_time(lines) -> ExecutionTime:
    load_string = "#load(...):"
    run_string = "#run(...):"
    main_string = "#main(...):"
    construct_string = "#construct(...):"
    load  = _find_value(lines, load_string)
    run   = _find_value(lines, run_string)
    main  = _find_value(lines, main_string)
    construct  = _find_value(lines, construct_string)
    if load:
        load = _cast_time_to_ms(load)
    if run:
        run = _cast_time_to_ms(run)
    if main:
        main = _cast_time_to_ms(main)
    if construct:
        construct = _cast_time_to_ms(construct)
    return ExecutionTime(unit = "ms", preprocessing = construct, discovery = run, total = main, dataset_loading=load, others={})


def _load_ram_usage(lines) -> RamUsage:
    mem="Memory consumption:"
    line= _find_value(lines, mem)
    q = line[:-2]
    u = line[len(line)-2:]
    return RamUsage(unit=u,max_ram_used=q)


def _load_error(lines) -> Error:
    time_string = "Time limit:"
    memory_string = "Out of memory:"
    time = _find_value(lines, time_string)
    memory = _find_value(lines, memory_string)
    return Error(time_limit = time, memory_limit = memory, general_error = "")


def _load_additional_info(lines) -> AdditionalInfo:
    comparison_string = "Comparison:"
    extent_string = "Extent:"
    approx_string = "ApproximateG3Error:"
    impute_string = "ImputeColumnType:"
    low_string = "ImputeColumnType:"
    upper_string = "ImputeColumnType:"
    exact_string = "Exact solved:"
    return AdditionalInfo(extent_relaxation = _find_value(lines, extent_string), similarity_function = ["abs","lev"], comparison_operator = ["<="],
                          others = {
                              "comparison_values":_find_value(lines, comparison_string),
                              "approximate_g3_error": _find_value(lines, approx_string),
                              "impute_col_type": _find_value(lines, impute_string),
                              "lower_bound_used": _find_value(lines, low_string),
                              "upper_bound_used": _find_value(lines, upper_string),
                              "exact_mvc_solved": _find_value(lines, exact_string),
                          })


def _cast_attribute(attribute_string) -> Attribute:
    attr, thr = attribute_string.split("@")
    return Attribute(attr, thr)


def _cast_dependency(line) -> Data:
    lhs_string, rhs_string = line.split("->")
    rhs_string=rhs_string.strip()
    lhs_string=lhs_string.strip()
    rhs = _cast_attribute(rhs_string)
    lhs = []
    if lhs_string=='':
        lhs.append(Attribute("*", "*"))
    else:
        lhs_attrs=lhs_string.split("\t")
        for attribute_string in lhs_attrs:
            lhs.append(_cast_attribute(attribute_string))
    return Data(lhs, rhs,None)


def _load_dependencies(lines) -> list[Data]:
    result=[]
    i = _find_index(lines,"RFDs:",False)+1
    while i < len(lines):
        line = lines[i].strip()
        if line =="": break
        result.append(_cast_dependency(line))
        i+=1
    return result


class DimeExecutionResultLoader(ExecutionResultLoader, ABC):
    file_path_key='log_file'
    def __init__(self, parameters_string: str):
        super().__init__(parameters_string)

    def load_info(self):
        execution = ExecutionResult(
            metadata_type="RFD",
            scenario="static",
            result = Result(
                execution_time= ExecutionTime(unit = "", dataset_loading = "", preprocessing = "", discovery = "", total = "", others = {}),
                ram_usage = RamUsage(unit = "", max_ram_used = ""),
                error = Error(time_limit = "", memory_limit = "", general_error = ""),
                additional_info = AdditionalInfo(extent_relaxation = 0, similarity_function = ["abs","lev"], comparison_operator = ["<="], others = {}),
                data = []
            )
        )
        with open(self.parameters[self.file_path_key], 'r') as file:
            lines=file.readlines()
        execution.result.data = _load_dependencies(lines)
        execution.result.execution_time = _load_execution_time(lines)
        execution.result.ram_usage = _load_ram_usage(lines)
        execution.result.error = _load_error(lines)
        execution.result.additional_info = _load_additional_info(lines)
        return execution
