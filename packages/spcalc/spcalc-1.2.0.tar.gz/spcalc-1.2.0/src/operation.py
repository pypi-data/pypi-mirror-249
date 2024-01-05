# Operation interface
from abc import ABC, abstractmethod


class Operation(ABC):
    @abstractmethod
    def execute(self, n1, n2):
        pass
