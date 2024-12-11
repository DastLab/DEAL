class Statistics:
    attribute_types: dict
    mean: dict
    median: dict
    mode: dict
    min_values: dict
    max_values: dict
    distribution: dict

    def __init__(self, attribute_types: dict, mean: dict, median: dict, mode: dict, min_values: dict, max_values: dict, distribution: dict):
        self.attribute_types = attribute_types
        self.mean = mean
        self.median = median
        self.mode = mode
        self.max_values = max_values
        self.min_values = min_values
        self.distribution = distribution
