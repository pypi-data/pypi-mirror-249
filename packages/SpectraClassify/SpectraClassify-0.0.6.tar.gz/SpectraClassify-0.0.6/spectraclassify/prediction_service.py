"""
This file is responsible for the prediction service of the latest trained model define by the user.
"""

import os
import numpy as np
from tensorflow.keras.models import load_model
from spectraclassify.utility.data_manager import preprocess_input_image


class PrecictionService:
    def __init__(self, model_path: str, classes: dict[str, int]):
        self.model = load_model(model_path)
        self.classes = classes

    def predict(self,
                image_path: str = "",
                do_preprocess: bool = True,
                target_size: tuple = (224, 224, 3),
                x: np.ndarray = None):
        try:
            if do_preprocess and target_size:
                y = preprocess_input_image(image_path, target_size)
                prediction = self.model.predict(y)
            else:
                prediction = self.model.predict(x)
            prediction = np.argmax(prediction, axis=1)
            return self.classes[prediction[0]]
        except Exception as e:
            print(f"Error in prediction: {e}")
            return None
