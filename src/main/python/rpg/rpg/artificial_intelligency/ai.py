from abc import abstractmethod

class ArtificialIntelligence:
    @abstractmethod
    def predict(self, input_data: object) -> object:
        raise NotImplementedError()