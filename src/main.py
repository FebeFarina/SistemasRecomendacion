import numpy as np
import heapq
import sys


def del_element(list, index):
  return list[:index] + list[index+1:]
    

filename = "utility-matrix-5-10-1"


with open("data/" + filename + ".txt", "r") as f:
  contents = f.readlines()

min_rate = float(contents[0].strip())
max_rate = float(contents[1].strip())

matrix_data = []

#Los datos se normalizan a valores entre 0 y 1
for line in contents[2:]:
  row = line.strip().split()
  for x in row:
    if x == '-':
      row[row.index(x)] = None
    elif float(x) > max_rate or float(x) < min_rate:
      print("Error: Algún no están dentro del rango: " + x)
      exit()
    else:
      row[row.index(x)] = (float(x) - min_rate)/(max_rate-min_rate)
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
  # Calculamos la similaridad de cada fila con la fila que tiene valores vacíos
  for j,other_rows in enumerate(reviews):
    other_copy = other_rows.copy()
    main_copy = rows_og[0].copy()
    # Caso de filas distintas
    if j != rows_og[2]:
      help_val = 0
      # Eliminamos los valores vacíos de la fila que estamos comparando
      for i,e in enumerate(rows_og[0]):
        if e is None:
          main_copy.remove(e)
          other_copy = del_element(other_copy, i+help_val)
          help_val -= 1
      help_val = 0
      other_copy2 = other_copy.copy()
      # Eliminamos los valores vacíos de la otra fila
      for i,e in enumerate(other_copy2):
        if e is None:
          other_copy.remove(e)
          main_copy = del_element(main_copy, i+help_val)
          help_val -= 1
      # No añadiremos las similitudes de las filas que no tengas valores en la misma columna que el valor a predecir
      if reviews[j][rows_og[1]] is not None:
        similarities.append((np.corrcoef(main_copy, other_copy)[0][1],j))
      mean.append(np.mean(other_copy))
    # Calcular la media de la fila con el valor a predecir
    else:
      other_rows = [x for x in other_rows if x is not None]
      mean.append(np.mean(other_rows))
  # Obtenemos las dos similitudes más altas
  highest = heapq.nlargest(2, similarities)
  result = 0
  div = 0
  # Hacemos la predicción considerando la diferencia con la media
  for sim in highest:
    result += sim[0] * (reviews[sim[1]][rows_og[1]]-mean[sim[1]])
    div += sim[0]
  result =mean[rows_og[2]] + (result/div)
  matrix_result[rows_og[2]][rows_og[1]] = result

# Desnormalizamos los valores y almacenamos en fichero
sys.stdout = open("results/" + filename + "-predicted.txt", "w")
for row in matrix_result:
  for e in row:
    e = e * (max_rate-min_rate) + min_rate
    sys.stdout.write(str(round(e,3)) + " ")
  sys.stdout.write("\n")