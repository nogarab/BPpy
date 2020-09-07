from abc import ABC, abstractmethod


class EventSelectionStrategy(ABC):

    @abstractmethod
    def select(self, b_program, statements):
        pass

    @abstractmethod
    def is_satisfied(self, event, statement):
        pass
