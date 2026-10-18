
a = 5
b = 6
c = 7

# Calculate semi-perimeter
s = (a + b + c) / 2

# Calculate area using Heron's formula
area = (s * (s - a) * (s - b) * (s - c)) ** 0.5

print("Area of the triangle =", area)
