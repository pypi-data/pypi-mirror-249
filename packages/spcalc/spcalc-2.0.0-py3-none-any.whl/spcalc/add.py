from spcalc.operation import Operation


class Add(Operation):
    def execute(self, n1, n2):
        return n1 + n2
