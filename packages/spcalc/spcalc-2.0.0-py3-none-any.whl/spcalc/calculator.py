# calculator class


class Calculator:
    def __init__(self, n1, n2, operation):
        self._n1 = n1
        self._n2 = n2
        self._operation = operation

    def execute(self):
        return self._operation.execute(self._n1, self._n2)
