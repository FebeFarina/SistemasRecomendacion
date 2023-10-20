import numpy as np
import heapq
import sys
import copy
import argparse

# funcion que elimina un elemento de una lista
def del_element(list, index):
  return list[:index] + list[index+1:]

# funcion que calcula la distancia entre dos filas
def calculate_distance(row1, row2, metric):
  if metric == 'pearson':
    return np.corrcoef(row1, row2)[0][1]
  elif metric == 'cosine':
    return 1 - np.dot(row1, row2)/(np.linalg.norm(row1)*np.linalg.norm(row2))
  elif metric == 'euclidean':
    return np.linalg.norm(row1-row2)
    
parser = argparse.ArgumentParser(description='Process filename.')
parser.add_argument('-f', '--file', type=str, help='filename', required=True)
parser.add_argument('-m', '--metric', type=str, help='metric', choices=['pearson', 'cosine', 'euclidean'], required=True)

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
          if np.std(main_copy) == 0 or np.std(other_copy) == 0:
            similarities.append((0,j))
          else: 
            similarities.append((calculate_distance(main_copy,other_copy, args.metric),j))
      # Calcular la media de la fila con el valor a predecir
      mean.append(np.mean(other_copy))
    # Caso de filas iguales
    else:
      other_copy = [x for x in other_copy if x is not None]
      mean.append(np.mean(other_copy))
  # Obtenemos las dos similitudes más altas
  highest = heapq.nlargest(2, similarities)
  result = 0
  div = 0
  # Hacemos la predicción considerando la diferencia con la media
  for sim in highest:
    result += sim[0] * (reviews[sim[1]][rows_og[1]]-mean[sim[1]])
    div += abs(sim[0])
  result =mean[rows_og[2]] + (result/div)
  matrix_result[rows_og[2]][rows_og[1]] = result

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