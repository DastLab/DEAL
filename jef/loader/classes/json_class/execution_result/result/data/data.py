from loader.classes.json_class.execution_result.result.data.attribute import Attribute


class Data:
    lhs: list[Attribute]
    rhs: Attribute
    cc: (str, None)

    def __init__(self, lhs: list[Attribute], rhs: Attribute, cc: (str, None)):
        self.rhs = rhs
        self.lhs = lhs
        self.cc = cc