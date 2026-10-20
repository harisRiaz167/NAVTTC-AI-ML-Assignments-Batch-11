import numpy as np

L = np.array([-1, 0, 1, -2, 0, 2])

print("Dataset:", L)

X = L.reshape(-1, 1)

print("Reshaped dataset:")
print(X)