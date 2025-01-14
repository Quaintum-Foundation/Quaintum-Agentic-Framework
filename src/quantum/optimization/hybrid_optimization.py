from quantum.optimization import QuantumOptimizer
from optimization.classical_optimization import ClassicalOptimizer

class HybridOptimizer:
    def __init__(self):
        self.quantum_optimizer = QuantumOptimizer()
        self.classical_optimizer = ClassicalOptimizer()

    def optimize(self, problem: dict, initial_guess: list):
        """
        Hybrid optimization combining QAOA and gradient descent.
        :param problem: Optimization problem.
        :param initial_guess: Initial parameters for classical refinement.
        :return: Final optimized parameters and value.
        """
        quantum_result = self.quantum_optimizer.optimize_qaoa(problem)
        initial_params = quantum_result.optimal_parameters
        refined_result = self.classical_optimizer.gradient_descent(
            func=problem['objective'],
            grad_func=problem['gradient'],
            initial_guess=initial_params,
        )
        return refined_result
