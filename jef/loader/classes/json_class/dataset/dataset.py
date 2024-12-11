from loader.classes.json_class.dataset.statistics.statistics import Statistics


class Dataset:
    name: str
    header: list[str]
    size: str
    file_format: str
    col_number: int
    row_number: int
    separator: str
    blank_char: str
    statistics: Statistics

    def __init__(self, name: str, header: list[str], size: str, file_format: str, col_number: int, row_number: int, separator: str, blank_char: str, statistics: Statistics):
        self.name = name
        self.header = header
        self.size = size
        self.file_format = file_format
        self.col_number = col_number
        self.row_number = row_number
        self.separator = separator
        self.blank_char = blank_char
        self.statistics = statistics
