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

for i,rows in enumerate(reviews):
  for e in range(len(rows)):
    if rows[e] is None:
      main_rows.append((rows,e,i))
      break
# Rows_og contiene la fila con valores vacíos y los índices de fila y columna
for rows_og in main_rows:
  # Flags es un array de booleanos que almacena si hay un valor vacío en la fila
  flags = []
  # Similarities es un array de tuplas que almacena la fila con su similaridad
  similarities = []
  # Mean es un array que almacena el promedio de cada fila
  mean = []
  # Rows es una copia de la fila con valores vacíos para poder eliminarlos sin perder la fila original
  rows = rows_og[0].copy()
  # Si encuentra un valor vacío, lo elimina de la lista y agrega un True a la lista de flags

  for i,e in enumerate(rows.copy()):
    #busca los valores vacíos
    if e is None:
      #subimos la bandera para no tener en cunenta la columna con el valor vacio
      flags.append(True)
      #eliminamos el valor vacio de la lista
      rows.remove(e)
    else:
      #mantenemos la bandera baja
      flags.append(False)
  for j,other_rows in enumerate(reviews):
    #aux_row es una copia de la fila para no perder la fila original
    aux_row = rows.copy()
    #other_rows son las filas con las que se comparará la fila con valores vacíos
    other_rows = other_rows.copy()
    
    #eliminamos la columna con el valor vacio si la bandera esta en True
    for i,e in enumerate(flags):
      if e == True:
        del other_rows[i]

    #borra los valores de las otras columnas con valores vacios a la hora de comparar 2 columnas con valores vacios
    if other_rows != aux_row:
      for i,e in enumerate(other_rows):
        if e is None:
          other_rows.remove(e)
          del aux_row[i]
      similarities.append((np.corrcoef(aux_row, other_rows)[0][1],j))
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

  
