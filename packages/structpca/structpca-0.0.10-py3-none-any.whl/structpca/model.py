from abc import ABC


class BaseModel(ABC):
    """Implements all the features that can be shared across models."""

    def __init__(self, func):
        """
        Init the model.
        """

        self.func = func

    def transform(self):
        """
        Transforms data.
        """
        return None

    def fit(self):
        "Fits the data"
        print("Fitting")
