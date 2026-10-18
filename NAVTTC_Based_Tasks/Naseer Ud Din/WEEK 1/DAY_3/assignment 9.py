
# Solve the quadratic equation ax² + bx + c = 0 using the cmath module (the example uses a=1, b=5, c=6).
# 

import cmath

a = 1
b = 5
c = 6

# Calculate the discriminant
d = (b**2) - (4*a*c)

# Calculate the two roots
root1 = (-b + cmath.sqrt(d)) / (2*a)
root2 = (-b - cmath.sqrt(d)) / (2*a)

print("The roots are:")
print("Root 1 =", root1)
print("Root 2 =", root2)
