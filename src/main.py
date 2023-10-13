import numpy as np
import heapq

def del_col(matrix, i):
  for row in matrix:
    del row[i]
  return matrix
    
with open("data/ejemplo1.txt", "r") as f:
  contents = f.readlines()

min_rate = float(contents[0].strip())
max_rate = float(contents[1].strip())

matrix_data = []
for line in contents[2:]:
  row = line.strip().split()
  row = [None if x == '-' else (float(x) - min_rate)/(max_rate-min_rate) for x in row]
  matrix_data.append(row)

reviews = matrix_data

# Llamamos main_rows a las filas que tienen valores vacíos
main_rows = []

for rows in reviews:
  if None in rows:
    main_rows.append(rows)

for rows in main_rows:
  flags = []
  similarities = []
  mean = []
  rows = rows.copy()
  # Si encuentra un valor vacío, lo elimina de la lista y agrega un True a la lista de flags
  for i,e in enumerate(rows):
    if e is None:
      flags.append(True)
      rows.remove(e)
    else:
      flags.append(False)
  for j,other_rows in enumerate(reviews):
    aux_row = rows.copy()
    other_rows = other_rows.copy()
    for i,e in enumerate(flags):
      if e == True:
        del other_rows[i]
    if other_rows != aux_row:
      for i,e in enumerate(other_rows):
        if e is None:
          other_rows.remove(e)
          del aux_row[i]
      similarities.append((np.corrcoef(aux_row, other_rows)[0][1],j))
    mean.append(np.mean(other_rows))
  highest = heapq.nlargest(2, similarities)
  result = 0
  for sim in highest:
    result += sim[0] * (mean[i[sim[1]]])
  
