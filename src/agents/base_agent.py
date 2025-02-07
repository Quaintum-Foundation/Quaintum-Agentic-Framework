import time
import logging
from typing import Callable, List, Any

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class BaseAgent:
    def __init__(self, name: str):
        """Initialize the agent with a name and any other necessary configuration."""
        self.name = name
        self.state = {}  # Can be extended to store any state or configuration
        logger.info(f"Agent '{self.name}' initialized.")

    def make_decision(self, input_data: List[Any]) -> float:
        """This method should be overridden by subclasses to make decisions."""
        raise NotImplementedError("This method should be overridden by subclasses.")

    def track_performance(self, func: Callable, *args, **kwargs) -> Any:
        """Track the performance of a function."""
        try:
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"Execution time for {func.__name__}: {execution_time:.4f} seconds")
            return result
        except Exception as e:
            logger.error(f"Error occurred while executing {func.__name__}: {str(e)}")
            raise

    def update_state(self, key: str, value: Any) -> None:
        """Update the agent's state."""
        self.state[key] = value
        logger.info(f"State updated: {key} = {value}")

    def get_state(self, key: str) -> Any:
        """Retrieve the agent's state."""
        value = self.state.get(key, None)
        if value:
            logger.info(f"State retrieved: {key} = {value}")
        else:
            logger.warning(f"State not found for key: {key}")
        return value

    def handle_error(self, error: Exception) -> None:
        """Handle errors and log them."""
        logger.error(f"An error occurred: {str(error)}")

    def clean_up(self) -> None:
        """Perform any cleanup tasks before shutting down."""
        logger.info(f"Cleaning up agent '{self.name}'...")
        # Extend with any necessary cleanup code

    def shutdown(self) -> None:
        """Gracefully shut down the agent."""
        logger.info(f"Shutting down agent '{self.name}'...")
        self.clean_up()
        # Any additional shutdown logic can be placed here
        logger.info(f"Agent '{self.name}' has been shut down.")

# Example subclass that uses BaseAgent
class MyAgent(BaseAgent):
    def __init__(self, name: str, strategy: str):
        super().__init__(name)
        self.strategy = strategy

    def make_decision(self, input_data: List[Any]) -> float:
        """Implement a specific decision-making strategy."""
        logger.info(f"Making decision using strategy: {self.strategy}")
        # Dummy decision logic for example purposes
        decision = sum(input_data) / len(input_data) if input_data else 0
        logger.info(f"Decision made: {decision}")
        return decision

# Example Usage
if __name__ == "__main__":
    agent = MyAgent(name="TestAgent", strategy="simple_average")
    
    # Track performance
    input_data = [1, 2, 3, 4, 5]
    agent.track_performance(agent.make_decision, input_data)
    
    # Update and retrieve state
    agent.update_state("last_decision", agent.make_decision(input_data))
    agent.get_state("last_decision")
    
    # Shutdown gracefully
    agent.shutdown()
