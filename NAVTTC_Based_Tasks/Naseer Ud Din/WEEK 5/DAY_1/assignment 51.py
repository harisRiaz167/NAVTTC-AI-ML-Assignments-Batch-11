
# Assignment 51: Linear Regression

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# 1. Prepare the data
# X = study hours
# y = marks obtained

X = np.array([[1], [2], [3], [4], [5], [6]])
y = np.array([20, 30, 40, 50, 60, 70])

print("Study Hours:")
print(X)

print("\nMarks:")
print(y)

# 2. Create the Linear Regression model
model = LinearRegression()

# 3. Train the model
model.fit(X, y)

# 4. Display the model's equation parameters
print("\nSlope:")
print(model.coef_[0])

print("\nIntercept:")
print(model.intercept_)

# 5. Predict marks for 7 study hours
new_hours = np.array([[7]])
predicted_marks = model.predict(new_hours)

print("\nPredicted marks for 7 study hours:")
print(predicted_marks[0])

# 6. Predict marks for all training examples
predictions = model.predict(X)

print("\nPredicted marks for training data:")
print(predictions)

# 7. Evaluate the model
print("\nMean Absolute Error:")
print(mean_absolute_error(y, predictions))

print("\nR-squared score:")
print(r2_score(y, predictions))
