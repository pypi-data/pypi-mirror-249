import os.path as _path
from joblib import load as _jlload
import logging
from .utils import gender_utils as _utils

__version__ = "0.0.1"


class PredictedGender:
    def __init__(self):
        self._gender = None
        self._probability = None

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        if not isinstance(value, str):
            raise TypeError("The 'gender' attribute must be a string.")
        if value not in ("M", "F"):
            raise ValueError("Invalid gender")
        self._gender = value

    @property
    def probability(self):
        return self._probability

    @probability.setter
    def probability(self, value):
        if not isinstance(value, list):
            raise TypeError("The 'probabilities' attribute must be a list.")
        if len(value) != 2:
            raise ValueError("The 'probabilities' list must contain 2 elements only.")
        if not isinstance(value[0], int) or not isinstance(value[1], int):
            raise TypeError("Both elements of the 'probabilities' list must be ints.")
        self._probability = value


def init_vectorizer():
    """
    Returns vectorizer if found

    Raises:
        FileNotFoundError: If vectorizer isnt found.
    """
    vectorizer_path = _path.join(_path.dirname(__file__), "vectorizer.joblib")
    try:
        vectorizer = _jlload(vectorizer_path)
        return vectorizer
    except FileNotFoundError:
        raise FileNotFoundError(
            f"vectorizer.joblib is missing, place vectorizer in {vectorizer_path}."
        )


def init_model(vectorizer, model_path="accurate_model.pth") -> _utils.GenderClassifier:
    """
    Returns model based on path if found

    Raises:
        FileNotFoundError: If model isnt found.
    """
    if model_path != "fast_model.pth" and not _path.exists(
        _path.join(_path.dirname(__file__), model_path)
    ):
        logging.warning(f"predict_gender_ml: missing {model_path}, falling back to fast_model.pth")
        model_path = "fast_model.pth"
    model_path = _path.join(_path.dirname(__file__), model_path)
    try:
        return _utils.load_model(vectorizer, model_path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Gender model is missing, place model in {model_path}."
        )


def predict(name: str, check_csv=False, fast_model=False, model=None, vectorizer=None):
    """
    Predicts gender based on name

    Args:
        name (str): First name.
        check_csv (bool, optional): Sets whether to use CSV data lookup for more accurate results.
        fast_model (bool, optional): Sets whether to use the faster but less accurate model.
        model (class GenderClassifier): Model to use for prediction.
        vectorizer (CountVectorizer): Vectorizer used in training the model.

    Returns:
        <class PredictedGender>
    """
    if check_csv:
        _, _, gender = _utils.retrieve_data(name)
        if gender != None:
            gender = "M" if gender == 0 else "F"
            return gender
    if not vectorizer:
        vectorizer = init_vectorizer()
    if not model:
        model = init_model(vectorizer, _utils.get_path(fast_model))
    probabilitys, predicted_gender = _utils.predict_gender_model(
        name, model, vectorizer
    )
    gender = PredictedGender()
    gender.gender = predicted_gender
    gender.probability = [round(p * 100) for p in probabilitys[0].tolist()]
    return gender
