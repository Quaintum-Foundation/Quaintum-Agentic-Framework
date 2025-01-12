class BaseAgent:
    def make_decision(self, input_data: list) -> float:
        raise NotImplementedError("This method should be overridden by subclasses.")
