class Attribute:
    column: str
    comparison_relaxation: str

    def __init__(self, column, comparison_relaxation):
        self.column = column
        self.comparison_relaxation = comparison_relaxation