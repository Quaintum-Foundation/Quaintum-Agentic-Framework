from ml.hybrid_models import ClassicalModel
from agents.base_agent import BaseAgent

class ClassicalAgent(BaseAgent):
    def __init__(self):
        self.model = ClassicalModel()

    def make_decision(self, input_data: list) -> float:
        return self.model.predict(input_data)