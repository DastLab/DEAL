import argparse
import importlib
import sys
import json
import re
from loader.classes.json_class.json_encoder import CustomJSONEncoder
from loader.loader import Loader


def load_class(loader_class_name):
    module_name, class_name = loader_class_name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    loader_class = getattr(module, class_name)
    return loader_class

def load_class_and_parameters(parameter):
    match = re.match(r"^(.*?)(?:\[(.*)\])$", parameter)
    loader_class_name=match.group(1)
    loader_parameter=match.group(2)

    loader_class = load_class(loader_class_name)
    return loader_class, loader_parameter


def save_results_to_json(data, save_path):
    with open(save_path, "w") as json_file:
        json.dump(data, json_file, indent=4, cls=CustomJSONEncoder)
    print("JSON file saved successfully.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='jsonifydiscovery.py',
        description='Standardize dependencies discovery result.'
    )
    parser.add_argument('-o', '--output', help="Output JSON file.", type=str, default="result.json")
    parser.add_argument('-d', '--dataset_loader', help="DatasetLoader class.", type=str, required=True)
    parser.add_argument('-a', '--algorithm_loader', help="AlgorithmLoader class.", type=str, required=True)
    parser.add_argument('-r', '--run_info_loader', help="RunInfoLoader class.", type=str, required=True)
    parser.add_argument('-e', '--execution_result_loader', help="ExecutionResultLoader class.", type=str, required=True)
    parser.add_argument('-extra', '--extra_data_loader', help="ExtraDataLoader class.", type=str)
    parser.add_argument('-fo', '--final_operation', help="FinalOperation class.", type=str)

    args = parser.parse_args()
    try:
        dataset_loader, dataset_loader_parameters=load_class_and_parameters(args.dataset_loader)
        algorithm_loader, algorithm_loader_parameters=load_class_and_parameters(args.algorithm_loader)
        run_info_loader, run_info_loader_parameters=load_class_and_parameters(args.run_info_loader)
        execution_result_loader, execution_result_loader_parameters=load_class_and_parameters(args.execution_result_loader)
        if(args.extra_data_loader):
            extra_data_loader, extra_data_loader_parameters=load_class_and_parameters(args.extra_data_loader)
        else:
            extra_data_loader=None
            extra_data_loader_parameters=None

        if (args.final_operation):
            final_operation = load_class(args.final_operation)
        else:
            final_operation = None

        loader=Loader(
            dataset_loader(dataset_loader_parameters),
            algorithm_loader(algorithm_loader_parameters),
            run_info_loader(run_info_loader_parameters),
            execution_result_loader(execution_result_loader_parameters),
            extra_data_loader(extra_data_loader_parameters) if extra_data_loader else None,
            final_operation() if final_operation else None
        )
    except (ImportError, AttributeError) as e:
        print(f"Error loading class: {e}")
        sys.exit(1)

    discovery_info = loader.load()
    save_results_to_json(discovery_info, args.output)