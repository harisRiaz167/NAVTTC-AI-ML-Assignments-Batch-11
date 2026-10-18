
import statistics

# Create a list of numbers
data = [10, 20, 20, 30, 40, 50, 60]

print("Data:", data)

# 1. Calculate Mean
mean_value = statistics.mean(data)
print("Mean:", mean_value)

# 2. Calculate Median
median_value = statistics.median(data)
print("Median:", median_value)

# 3. Calculate Mode
mode_value = statistics.mode(data)
print("Mode:", mode_value)
