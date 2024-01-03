import torch as torch
import torch.nn.functional as nnf
import os.path as path
import pandas as pd


class GenderClassifier(torch.nn.Module):
    def __init__(self, input_size, output_size, fast=False):
        super(GenderClassifier, self).__init__()
        self.fast = fast
        if self.fast:
            self.linear = torch.nn.Linear(input_size, output_size)
            self.softmax = torch.nn.Softmax(dim=1)
        else:
            num_hidden = (input_size + output_size) // 2
            self.linear = torch.nn.Linear(input_size, num_hidden)
            self.linear2 = torch.nn.Linear(num_hidden, output_size)
            self.dropout = torch.nn.Dropout(p=0.5)
            self.softmax = torch.nn.Softmax(dim=1)

    def forward(self, x):
        x = self.linear(x)
        if not self.fast:
            x = nnf.relu(x)
            x = self.dropout(x)
            x = self.linear2(x)
            x = nnf.sigmoid(x)
        probabilities = self.softmax(x)
        return x, probabilities


def retrieve_data(name, csv_path="data.csv") -> tuple:
    df_path = path.join(path.dirname(__file__), csv_path)
    try:
        df = pd.read_csv(df_path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Gender data is missing, place the {csv_path} in {df_path}."
        )

    names = df["Name"].tolist()
    genders = df["Gender"].map({"M": 0, "F": 1}).tolist()
    if name and name in names:
        gender = genders[names.index(name)]
        return names, genders, gender


def load_model(vectorizer, model_path):
    input_size = len(vectorizer.get_feature_names_out())
    output_size = 2
    if len(model_path) >= 18 and model_path[-18:] == "accurate_model.pth":
        model = GenderClassifier(input_size, output_size)
    else:
        model = GenderClassifier(input_size, output_size, True)
    model.load_state_dict(torch.load(model_path))
    return model


def get_path(fast_model):
    data_path = "accurate_model.pth"
    if fast_model:
        data_path = "fast_model.pth"
    return data_path


def predict_gender_model(user_input: str, model: GenderClassifier, vectorizer):
    """
    Predicts gender based on name

    Args:
        user_input (str): First name.
        model (class GenderClassifier): Model to use for prediction.
        vectorizer (CountVectorizer): Vectorizer used in training the model.

    Returns:
        tuple: Containing 2 values of (numpy.ndarray, str)
    """
    input_tensor = torch.tensor(
        vectorizer.transform([user_input]).toarray(), dtype=torch.float32
    )
    model.eval()
    with torch.no_grad():
        output, probabilities = model(input_tensor)
        _, predicted_class = torch.max(output, 1)
        predicted_gender = "M" if predicted_class.item() == 0 else "F"
    return probabilities.numpy(), predicted_gender
