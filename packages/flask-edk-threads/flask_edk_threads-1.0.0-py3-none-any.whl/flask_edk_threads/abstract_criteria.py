import abc


class AbstractCriteria(abc.ABC):
    def __init__(self, *args, **kwargs): ...

    @abc.abstractmethod
    def true(self, criteria_desc): ...
