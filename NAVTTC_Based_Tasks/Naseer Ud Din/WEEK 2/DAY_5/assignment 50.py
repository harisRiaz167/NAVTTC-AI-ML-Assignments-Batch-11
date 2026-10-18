
import statistics

# Create a list of numbers
data = [10, 20, 30, 40, 50]

print("Data:", data)

# 1. Calculate Mean
mean_value = statistics.mean(data)
print("Mean:", mean_value)

# 2. Calculate Population Standard Deviation
population_sd = statistics.pstdev(data)
print("Population Standard Deviation:", population_sd)

# 3. Calculate Sample Standard Deviation
sample_sd = statistics.stdev(data)
print("Sample Standard Deviation:", sample_sd)
