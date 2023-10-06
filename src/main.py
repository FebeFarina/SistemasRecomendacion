with open("data/ejemplo1.txt", "r") as f:
  contents = f.readlines()

min_rate = float(contents[0].strip())
max_rate = float(contents[1].strip())

matrix_data = []
for line in contents[2:]:
  row = line.strip().split()
  row = [-1 if x == '-' else (float(x) - min_rate)/(max_rate-min_rate) for x in row]
  matrix_data.append(row)

reviews = matrix_data

print(min_rate)
print(max_rate)
print(reviews)