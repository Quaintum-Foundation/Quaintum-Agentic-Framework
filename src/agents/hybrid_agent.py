import numpy as np
from sklearn.neural_network import MLPClassifier

class ClassicalModel:
    def __init__(self):
        """
        Initializes a classical machine learning model (MLPClassifier).
        """
        self.model = MLPClassifier(hidden_layer_sizes=(10,), max_iter=1000)

    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """
        Trains the model on input data.
        :param X_train: Features for training.
        :param y_train: Labels for training.
        """
        self.model.fit(X_train, y_train)

    def predict(self, input_data: list) -> float:
        """
        Makes a prediction using the trained model.
        :param input_data: Input data for prediction.
        :return: The predicted value.
        """
        return self.model.predict([input_data])[0]
