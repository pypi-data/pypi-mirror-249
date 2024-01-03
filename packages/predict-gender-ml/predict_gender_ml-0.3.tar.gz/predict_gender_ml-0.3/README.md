# Predict Gender ML

Predict Gender ML is a tool to predict a person's gender based on their name using ML Models.

## Usage
```python
import predict_gender_ml


prediction = predict_gender_ml.predict("John")
gender = prediction.gender
probabilities = prediction.probability
print(f"John is {gender} with a confidence of {max(probabilities)}%")
> John is M with a confidence of 73%
```

## ML Models
### Data
Data used to train models: https://archive.ics.uci.edu/dataset/591/gender+by+name
### Accuracy on trained data
Fast Model: 80%

Accurate Model: 87%

