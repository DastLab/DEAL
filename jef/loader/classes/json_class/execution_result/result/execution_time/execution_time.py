class ExecutionTime:
    unit: (str, None)
    dataset_loading: (str, None)
    preprocessing: (str, None)
    discovery: (str, None)
    total: (str, None)
    others: (dict, None)

    def __init__(self, unit: (str, None), dataset_loading: (str, None), preprocessing: (str, None), discovery: (str, None), total: (str, None), others: (dict, None)):
        self.unit = unit
        self.dataset_loading = dataset_loading
        self.preprocessing = preprocessing
        self.discovery = discovery
        self.total = total
        self.others = others
