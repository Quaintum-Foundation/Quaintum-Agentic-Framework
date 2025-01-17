import time

class BaseAgent:
    def make_decision(self, input_data: list) -> float:
        raise NotImplementedError("This method should be overridden by subclasses.")

    def track_performance(self, func, *args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        logger.info(f"Execution time: {execution_time:.4f} seconds")
        return result