import numpy as np
import heapq
import sys
import copy
import argparse
from del_function import remove_none, del_element
from pred_function import calculate_distance, predict

    
parser = argparse.ArgumentParser(description='Process filename.')
parser.add_argument('-f', '--file', type=str, help='filename', required=True)
parser.add_argument('-m', '--metric', type=str, help='metric', choices=['pearson', 'cosine', 'euclidean'], required=True)
parser.add_argument('-p', '--predict', type=str, help='predict', choices=['simple', 'meandif'], required=True)

args = parser.parse_args()

filename = args.file


with open("data/" + filename + ".txt", "r") as f:
  contents = f.readlines()

min_rate = float(contents[0].strip())
max_rate = float(contents[1].strip())

reviews = []

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
  reviews.append(row)

matrix_result = copy.deepcopy(reviews)

# Llamamos main_rows a las filas que tienen valores vacíos
main_rows = []

# Obtenemos las filas con valores vacíos
for j,rows in enumerate(reviews):
  for i in range(len(rows)):
    if rows[i] is None:
      main_rows.append((rows,i,j))

# Rows_og contiene la fila con valores vacíos y los índices de fila y columna. El siguiente bucle recorre cada fila en la que hay valores vacíos
for rows_og in main_rows:
  # Flags es un array de booleanos que almacena un true si es un valor vacío y un false si no lo es
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
      # Eliminamos los valores vacíos de la fila que estamos comparando
      other_copy = remove_none(rows_og[0], main_copy, other_copy)
      # Eliminamos los valores vacíos de la otra fila
      other_copy2 = other_copy.copy()
      main_copy = remove_none(other_copy2, other_copy, main_copy)
      # No añadiremos las similitudes de las filas que no tengas valores en la misma columna que el valor a predecir
      if reviews[j][rows_og[1]] is not None:
        similarities.append((calculate_distance(main_copy,other_copy, args.metric),j))
      # Calcular la media de la fila con el valor a predecir
      mean.append(np.mean(other_copy))
    # Caso de filas iguales
    else:
      other_copy = [x for x in other_copy if x is not None]
      mean.append(np.mean(other_copy))
  # Obtenemos las dos similitudes más altas
  highest = heapq.nlargest(2, similarities) 
  matrix_result[rows_og[2]][rows_og[1]] = predict(highest, args.predict, reviews, rows_og, mean)

# Desnormalizamos los valores y almacenamos en fichero
sys.stdout = open("results/" + filename + "-predicted.txt", "w")
for row in matrix_result:
  for e in row:
    e = e * (max_rate-min_rate) + min_rate
    if e > max_rate:
        e = max_rate
    elif e < min_rate:
        e = min_rate
    sys.stdout.write(str(round(e,3)) + " ")
  sys.stdout.write("\n")