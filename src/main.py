import numpy as np
import heapq

def del_element(list, index):
  return list[:index] + list[index+1:]
    
with open("data/ejemplo1.txt", "r") as f:
  contents = f.readlines()

min_rate = float(contents[0].strip())
max_rate = float(contents[1].strip())

matrix_data = []

#Los datos se normalizan a valores entre 0 y 1
for line in contents[2:]:
  row = line.strip().split()
  row = [None if x == '-' else (float(x) - min_rate)/(max_rate-min_rate) for x in row]
  matrix_data.append(row)

# Reviews es la matriz de datos
reviews = matrix_data
matrix_result = reviews.copy()

# Llamamos main_rows a las filas que tienen valores vacíos
main_rows = []

for j,rows in enumerate(reviews):
  for i in range(len(rows)):
    if rows[i] is None:
      main_rows.append((rows,i,j))

# Rows_og contiene la fila con valores vacíos y los índices de fila y columna
for rows_og in main_rows:
  # Flags es un array de booleanos que almacena si hay un valor vacío en la fila
  flags = []
  # Similarities es un array de tuplas que almacena la fila con su similaridad
  similarities = []
  # Mean es un array que almacena el promedio de cada fila
  mean = []
  # Rows es una copia de la fila con valores vacíos para poder eliminarlos sin perder la fila original
  #main_rows = rows_og[0].copy()
  # Si encuentra un valor vacío, lo elimina de la lista y agrega un True a la lista de flags

  for j,other_rows in enumerate(reviews):
    main_rows = rows_og[0].copy()
    if other_rows != rows_og[0]:
      for i,e in enumerate(main_rows):
        if e is None:
          main_rows.remove(e)
          other_rows = del_element(other_rows, i)
      for i,e in enumerate(other_rows):
        if e is None:
          other_rows.remove(e)
          main_rows = del_element(main_rows, i)
      similarities.append((np.corrcoef(main_rows, other_rows)[0][1],j))
      mean.append(np.mean(other_rows))
    else:
      other_rows = [x for x in other_rows if x is not None]
      mean.append(np.mean(other_rows))
  highest = heapq.nlargest(2, similarities)
  result = 0
  div = 0
  for sim in highest:
    result += sim[0] * (reviews[sim[1]][rows_og[1]]-mean[sim[1]])
    div += sim[0]
  # Se deshace la normalización del resultado
  result =mean[rows_og[2]] + (result/div)
  #result = result * (max_rate-min_rate) + min_rate
  matrix_result[rows_og[2]][rows_og[1]] = result



for row in matrix_result:
  for e in row:
    e = e * (max_rate-min_rate) + min_rate
    print(round(e, 3), end=" ")
  print()
      