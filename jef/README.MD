# FD\RFD discovery results formatter
The aim of this python tool is to allow you to translate your dependency discovery results into a standard JSON format so that they are usable by the DEAL web tool.

We assume that an anaconda environment has already been set up, named deal with python version=3.11 and pandas=2.2.2.


In order to implement your result translator, you need to implement (or take advantage of already provided implementations of) the classes:

1. loader/classes/abstract_class/dataset_loader/DatasetLoader
2. loader/classes/abstract_class/algorithm_loader/AlgorithmLoader
3. loader/classes/abstract_class/run_info_loader/RunInfoLoader
3. loader/classes/abstract_class/execution_result_loader/ExecutionResultLoader
5. loader/classes/abstract_class/extra_data_loader/ExtraDataLoader (not mandatory)
6. loader/classes/abstract_class/final_operation/FinalOperation (not mandatory)

Implementing the load_info method and returning as output of the method the correct class (Dataset, Algorithm, etc.).

Each loader is used to build a parts of the DiscoveryInfo object which represents the JSON to load in DEAL tool. 

The FinalOperation class is used to edit the DiscoveryInfo object before the final save on a file.

Some basic loader classes are already defined:
1. loader/algorithm/default_json_algorithm_loader/DefaultJSONAlgorithmLoader is used to load Algorithm object from JSON
2. loader/dataset/csv_dataset_loader/CSVDatasetLoader is used to extract information from a given CSV dataset 
3. ...

Each loader will receive its respective parameters as dict, passed on the command line before jsonifydiscovery.py is executed.

Example of implemented loaders and finaloperation can be found in algorithms folder.









