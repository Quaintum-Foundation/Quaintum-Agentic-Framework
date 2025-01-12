from ml.hybrid_models import ClassicalModel

class ClassicalAgent:
    def __init__(self):
        """
        Initializes a ClassicalAgent.
        """
        self.model = ClassicalModel()

    def make_decision(self, input_data: list) -> float:
        """
        Makes a decision based on classical machine learning.
        :param input_data: Input data for the classical model.
        :return: The decision made by the classical agent.
        """
        return self.model.predict(input_data)
