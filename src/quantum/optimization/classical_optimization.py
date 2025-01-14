import numpy as np

class ClassicalOptimizer:
    def gradient_descent(self, func, grad_func, initial_guess, learning_rate=0.01, max_iter=100):
        """
        Performs gradient descent optimization.
        :param func: Objective function.
        :param grad_func: Gradient of the function.
        :param initial_guess: Initial point.
        :param learning_rate: Step size.
        :param max_iter: Maximum number of iterations.
        :return: Optimal point and value.
        """
        x = initial_guess
        for _ in range(max_iter):
            grad = grad_func(x)
            x -= learning_rate * grad
        return x, func(x)

    def simulated_annealing(self, func, bounds, max_iter=1000, temp=1000):
        """
        Performs simulated annealing optimization.
        :param func: Objective function.
        :param bounds: Bounds for variables.
        :param max_iter: Maximum number of iterations.
        :param temp: Initial temperature.
        :return: Optimal point and value.
        """
        x = np.random.uniform(bounds[:, 0], bounds[:, 1])
        best_x = x
        best_val = func(x)
        for _ in range(max_iter):
            new_x = x + np.random.uniform(-1, 1, size=x.shape)
            new_x = np.clip(new_x, bounds[:, 0], bounds[:, 1])
            delta = func(new_x) - func(x)
            if delta < 0 or np.exp(-delta / temp) > np.random.rand():
                x = new_x
                if func(x) < best_val:
                    best_x, best_val = x, func(x)
            temp *= 0.99  # Cooling
        return best_x, best_val
