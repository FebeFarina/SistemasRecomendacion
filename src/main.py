import numpy as np

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

print(min_rate)
print(max_rate)
print(reviews)


# bucle que va a recorrer la matriz de reviews por filas
for i in range(len(reviews)):
  for j in range(len(reviews)):
    if i != j and j > i:
    #creamos un array para guadar las banderas
      flags = []
      # bucle que va a recorrer la matriz de reviews por columnas
      for k,l in zip(range(len(reviews[i])), range(len(reviews[j]))):
        # si el valor de la celda es None, subimos la bandera
        if (reviews[i][k] is None) or (reviews[j][l] is None):
          flags.append(True)
        else:
          flags.append(False)
      #la operacion va a este nivel

  print (flags)