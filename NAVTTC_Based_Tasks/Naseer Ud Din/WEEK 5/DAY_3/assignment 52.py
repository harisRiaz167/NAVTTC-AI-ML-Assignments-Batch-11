
# Assignment 52: Logistic Regression

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 1. Prepare the dataset
# X = study hours
# y = result (0 = Fail, 1 = Pass)

X = np.array([
    [1],
    [2],
    [2.5],
    [3],
    [3.5],
    [4],
    [4.5],
    [5],
    [6],
    [7]
])

y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

# 2. Create the Logistic Regression model
model = LogisticRegression()

# 3. Train the model
model.fit(X, y)

# 4. Predict results for the training data
predictions = model.predict(X)

print("Actual Results:")
print(y)

print("\nPredicted Results:")
print(predictions)

# 5. Predict the result for a student who studied 3 hours
new_student = np.array([[3]])
result = model.predict(new_student)

print("\nPrediction for 3 study hours:")
if result[0] == 1:
    print("Pass")
else:
    print("Fail")

# 6. Predict the result for a student who studied 5 hours
new_student = np.array([[5]])
result = model.predict(new_student)

print("\nPrediction for 5 study hours:")
if result[0] == 1:
    print("Pass")
else:
    print("Fail")

# 7. Display predicted probabilities for 5 hours
probabilities = model.predict_proba(np.array([[5]]))

print("\nProbabilities for 5 study hours:")
print("Fail probability:", probabilities[0][0])
print("Pass probability:", probabilities[0][1])

# 8. Calculate model accuracy on training data
accuracy = accuracy_score(y, predictions)

print("\nTraining Accuracy:")
print(accuracy)

# 9. Display confusion matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y, predictions))

# 10. Display classification report
print("\nClassification Report:")
print(classification_report(y, predictions, zero_division=0))
