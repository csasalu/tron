from abc import abstractmethod, ABCMeta


class SimpleRequestHandler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def process_request(self, request: str) -> str:
        pass
