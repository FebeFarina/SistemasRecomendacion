# Sistemas de recomendacion. Métodos de filtrado colaborativo

## Índice

- [Instrucciones de instalación](#instrucciones-de-instalación)
- [Descripción del código](#descripción-del-código)
  - [Funciones](#funciones)
  - [Lectura de ficheros y parseo de argumentos](#lectura-de-ficheros-y-parseo-de-argumentos)
  - [Extracción de datos](#extracción-de-datos)
  - [Bucle principal](#bucle-principal)
    - [eliminamos los otros Nones](#eliminamos-los-otros-nones)
    - [Calculamos la similitud entre filas](#calculamos-la-similitud-entre-filas)
    - [Calculamos el valor a predecir](#calculamos-el-valor-a-predecir)
  - [Retorno de resultados](#retorno-de-resultados)
- [Ejemplos de uso](#ejemplos-de-uso)

En esta práctica abordaremos el método de filtrado colaborativo basado en el usuario, por el cual realizaremos predicciones sobre una matriz de valoraciones.

## Instrucciones de instalación

Las librerías necesarias para la ejecución del programa son las siguientes:

- numpy
- heapq
- sys
- copy
- argparse

En caso de no contar con alguna de estas librerías, se debe instalar haciendo uso de **pip**

```
pip install <package>
```

## Descripción del código

### Funciones

Lo primero que vemos al analizar el codigo son distinta funciones que usamos varias veces a lo largo del codigo. En nuestro caso y para una mayor ordenacion las hemos separado en 2 ficheros:

```python
# Función que elimina un elemento de una lista
def del_element(list, index):
  return list[:index] + list[index+1:]
# Función que elimina los valores vacíos de una lista y el valor de la misma columna de la otra lista
def remove_none(list_original, list_main, list_other):
    help_val = 0
    for i,e in enumerate(list_original):
        if e is None:
            list_main.remove(e)
            list_other = del_element(list_other, i+help_val)
            help_val -= 1
    return list_othe
```

El primer fichero llamado del_function.py contiene las funciones que usamos para eliminar elementos de una lista y para eliminar los valores None de una lista y el valor de la misma columna de la otra lista.

Debido a que estamos eliminando valores no solo en la columna de la fila que estamos comparando, sino tambien en la columna de la fila con la que estamos comparando, se pueden quedar valores sin analizar al desplazarse las filas, por eso tras cada eliminacion de un valor, retrocedemos en 1 el indice para que no se salte ningún valor.

El segundo fichero llamado pred_functions.py contiene las funciones que usamos para calcular la distancia entre vectores:

```python
import numpy as np

# funcion que calcula la distancia entre dos filas
def calculate_distance(row1, row2, metric):
  if metric == 'pearson':
    if np.std(row1) == 0 or np.std(row2) == 0:
      return 0
    return np.corrcoef(row1, row2)[0][1]
  elif metric == 'cosine':
    if np.linalg.norm(row1) == 0 or np.linalg.norm(row2) == 0:
      return 0
    return np.dot(row1, row2)/(np.linalg.norm(row1)*np.linalg.norm(row2))
  elif metric == 'euclidean':
    return np.linalg.norm(np.array(row1) - np.array(row2))

def predict(neighbors, predict_type, reviews, rows_og, mean):
  result = 0
  div = 0
  for sim in neighbors:
    if predict_type == 'meandif':
      result += sim[0] * reviews[sim[1]][rows_og[1]]-mean[sim[1]]
    elif predict_type == 'simple':
      result += sim[0] * (reviews[sim[1]][rows_og[1]])
    div += abs(sim[0])
  result =(result/div)
  if predict_type == 'meandif':
    result += mean[rows_og[2]]
  return result
```

Como podemos ver, la primera función que tenemos es la que calcula la distancia entre vectores. Esta función recibe como parametros los 2 vectores a comparar y el tipo de métrica que queremos usar (pearson, cosine o euclidean). Dependiendo del tipo de métrica que hayamos elegido, la función calculará la distancia entre vectores de una forma u otra. La segunda función que tenemos es la que calcula el valor a predecir. Esta función recibe como parametros los 2 vectores mas similares, el tipo de predicción que queremos hacer (simple o meandif), la matriz de datos, la fila donde se encuentra el valor a predecir y la lista de promedios de las filas. Dependiendo del tipo de predicción que hayamos elegido, la función calculará el valor a predecir de una forma u otra.

### Lectura de ficheros y parseo de argumentos

Lo siguiente que vemos en el código es como recoje y procesa los datos que entran por linea de comandos. Estos comandos serian el nombre del fichero donde estan los datos a cargar, y el segundo el tipo de métrica que queremos usar para calcular la distancia entre vectores, como deseamos predecir los valores, si de forma simple o usando la media de la fila y el número de vecinos que deseamos para realizar la predicción.

```python
parser = argparse.ArgumentParser(description='Process filename.')
parser.add_argument('-f', '--file', type=str, help='filename', required=True)
parser.add_argument('-m', '--metric', type=str, help='metric', choices=['pearson', 'cosine', 'euclidean'], required=True)
parser.add_argument('-p', '--predict', type=str, help='predict', choices=['simple', 'meandif'], required=True)
parser.add_argument('-n', '--neighbors', type=int, help='neighbors', default=2)

args = parser.parse_args()

filename = args.file
```

### Extracción de datos

Ya una vez con el fichero cargado, lo que hacemos es extraer los datos de este fichero y guardarlos para usarlos:

```python
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

matrix_result = copy.deepcopy(reviews)ç
```

Como podemos apreciar tambien en el código anterior, lo primero que hacemos es leer los valores que seran el minimo valor y el maximo valor posible en la matriz. Tras esto, y mientras leemos la matriz, normalizamos los datos a valores entre 0 y 1 para que no haya problemas a la hora de calcular las distancias entre vectores. En caso de encontrar un guión, lo sustituimos por un None. En caso de que el valor no esté dentro del rango, mostramos un error y salimos del programa.

Tras esto, creamos un diccionario que nos servirá para guardar las similitudes de cada fila con las otras filas y una lista que nos servirá para guardar los vecinos que ha usado el programa para calcular las predicciones. Estas ultimas las usaremos principalmente para mostrar al final del programa los resultados que se nos piden. También, buscamos con la siguiente función las filas en las que hemos encontrado un None, y las guardamos en la lista "main_rows" lista para usarlas más adelante. Esta lista la llamaremos main_rows como se puede ver en el siguiente código.

```python
all_similarities = dict(zip(list(range(len(reviews))), [[] for _ in range(len(reviews))]))
all_neighbors = []
# Llamamos main_rows a las filas que tienen valores vacíos
main_rows = []

# Obtenemos las filas con valores vacíos
for j,rows in enumerate(reviews):
  for i in range(len(rows)):
    if rows[i] is None:
      main_rows.append((rows,i,j))

```



### Bucle principal

```python

# Obtenemos las filas con valores vacíos
for rows_og in main_rows:
  # Flags es un array de booleanos que almacena un true si es un valor vacío y un false si no lo es
  flags = []
  # Similarities un array de tuplas que almacena el numero de la fila dentro de la matriz y su valor de similaridad con la fila en la que estamos calculando el valor
  similarities = []
  # Mean es un array que almacena el promedio de cada fila
  mean = []
  # Calculamos la similaridad de cada fila con la fila que tiene valores vacíos
  for j,other_rows in enumerate(reviews):
    other_copy = other_rows.copy()
    main_copy = rows_og[0].copy()
```

Lo siguiente que hacemos es proceder a resolver y sustituir los valores None por valores calculados por el programa.
Entraremos en un bucle que recorra las filas que tienen valores vacíos. Estos están guardados aparte gracias al fragmento de código anterior.
Lo siguiente que haremos sera crear unas variables que nos ayudarán a calcular los valores que necesitamos. Estas variables son:

- flags: un array de booleanos que almacena un true si es un valor vacío y un false si no lo es
- similarities: un array de tuplas que almacena el número de la fila dentro de la matriz y su valor de similaridad con la fila en la que estamos calculando el valor
- mean: es un array que almacena el promedio de cada fila

Ya entrando en el bucle lo que vamos a hacer es ir comparando entre la fila donde está el el valor a calcular con las otras para saber la similitud de las otras filas con la primera mencionada.

Importante mencionar que para poder movernos libremente por la matriz, vamos a ir haciendo copias de las filas que vamos comparando y así no perder los valores originales ni el tamaño original de estas.

#### eliminamos los otros Nones

Para poder sacar la similitud entre filas, primero debemos eliminar los valores de las columnas donde hay algún None, ya que si no, no podremos calcular la similitud entre filas:

```python
# Caso de filas distintas
    if j != rows_og[2]:
      # Eliminamos los valores vacíos de la fila que estamos comparando
      other_copy = remove_none(rows_og[0], main_copy, other_copy)
      # Eliminamos los valores vacíos de la otra fila
      other_copy2 = other_copy.copy()
      main_copy = remove_none(other_copy2, other_copy, main_copy)
```

Como podemos ver, para eliminar los valores llamamos a la misma función 2 veces cambiando el orden de las filas que comparamos, para asi borrar primero los nones de la fila main, y luego los de la fila other (con sus respectivas columnas)


#### Calculamos la similitud entre filas

Ya una vez eliminados los valores None, procedemos a calcular la similitud entre filas:

```python
 # No añadiremos las similitudes de las filas que no tengas valores en la misma columna que el valor a predecir
if reviews[j][rows_og[1]] is not None:
        similarities.append((calculate_distance(main_copy,other_copy, args.metric),j))
      # Calcular la media de la fila con el valor a predecir
      mean.append(np.mean(other_copy))
```

Lo primero que vemos en el fragmento de código anterior es que si la fila con la que estamos comparando no tiene valor en la misma columna que el valor a predecir, no añadiremos la similitud de esa fila a la lista de similitudes. Esto es debido a que no podremos calcular la similitud entre filas si no tienen valores en las mismas columnas.
Como podemos ver también, si la desviación típica de alguna de las filas es 0, no podremos calcular la similitud entre filas, por lo que en ese caso, añadiremos un 0 a la lista de similitudes.

En un caso normal, entraremos por el else, donde calcularemos la similitud dependiendo del tipo de métrica que hayamos elegido al inicio del programa. Tras esto, añadiremos la similitud a la lista de similitudes y el promedio de la fila a la lista de promedios.

```python
    else:
      other_copy = [x for x in other_copy if x is not None]
      mean.append(np.mean(other_copy))
```

Si estamos comparando una fila consigo misma, tendremos que tener en cuenta su media en el caso de hacer la predicción por diferencia con la media. Para ello, eliminamos todos los valores vacíos de la fila y añadimos su media a la lista de promedios.

Se nos pasa como argumento el número de vecinos que necesitaremos para realizar la predicción, por lo que ordenamos la lista de similitudes y nos quedamos con los N primeros valores. También añadimos a la lista de vecinos la lista de similitudes ordenada y los valores de la fila y columna donde se encuentra el valor a predecir.

```python
highest = heapq.nlargest(args.neighbors, similarities)
all_neighbors.append((highest, rows_og[2], rows_og[1])) 
```

#### Calculamos el valor a predecir

Ya una vez tenemos los 2 valores mas similares, procedemos a calcular el valor a predecir:

```python
 matrix_result[rows_og[2]][rows_og[1]] = predict(highest, args.predict, reviews, rows_og, mean)
```

Haciendo referencia a la función que enseñamos anteriormente, lo primero que hacemos es inicializar las variables que vamos a usar para calcular el valor a predecir. Tras esto, y usando los 2 valores mayores de la lista de similitudes, procedemos a calcular el valor a predecir. Para ello, lo que hacemos es multiplicar la similitud de cada fila con la fila que tiene el valor a predecir por la diferencia entre el valor a predecir y el promedio de la fila con la que estamos comparando. Tras esto, dividimos el resultado entre la suma de los valores absolutos de las similitudes de las filas con la fila que tiene el valor a predecir. Finalmente, sumamos el resultado a la media de la fila con la que estamos trabajando y guardamos el resultado en la matriz de resultados.

Tras hacer todo lo mencionado anteriormente, obtenemos un valor que remplaza al none. Por lo que pasamos al siguiente none y repetimos el proceso hasta que no queden mas valores none en la matriz.

Es importante mencionar que en nuestro caso, a la hora de decidir y hacer el código, no usamos valores que estos mismos generan para obtener otros valores, esto lo hacemos a causa de que son predicciones y no valores reales, por lo que no queremos que un valor que hemos calculado influya en el calculo de otro valor.

Por último, para poder mostrar al final uno de los resultados que se nos desea mostrar, guardamos en "all_similarities" las similitudes de la fila con todas las otras filas. Cabe destacar el condicional previo creado para comprobar que se coloque el caso en el que mas veces se genera similitudes en una fila con otra fila (un caso en el que puede generar menos es cuando en la misma columna que deseamos predecir el valor, tambien hay un none en la fila con la que estamos comparando, para optimizar el programa, no calculamos la similitud en ese caso)

```python
  if len(all_similarities[rows_og[2]]) < len(similarities):
    all_similarities[rows_og[2]] = similarities
```

### Retorno de resultados

Una vez cambiados todos los valores none por valores calculados por el programa, procedemos a preparar el fichero con los resultados y los datos que se nos piden:

```python

# Desnormalizamos los valores y almacenamos en fichero
sys.stdout = open("results/" + filename + "-predicted.txt", "w")
sys.stdout.write("Matriz de utilidad predicha:\n")
for row in matrix_result:
  for e in row:
    e = e * (max_rate-min_rate) + min_rate
    if e > max_rate:
        e = max_rate
    elif e < min_rate:
        e = min_rate
    sys.stdout.write(str(round(e,3)) + " ")
  sys.stdout.write("\n")
sys.stdout.write("\n")
sys.stdout.write("Predicciones:\n")
for i in range(len(all_neighbors)):
  sys.stdout.write("[" + str(all_neighbors[i][1]+1) + "][" + str(all_neighbors[i][2]+1) + "]: " +
   str(round(matrix_result[all_neighbors[i][1]][all_neighbors[i][2]] * (max_rate - min_rate) + min_rate,3)) + "\n")
sys.stdout.write("\n")
sys.stdout.write("Similitudes:\n")
for i in range(len(all_similarities)):
  if len(all_similarities[i]) == 0:
    sys.stdout.write("Fila " + str(i+1) + " sin similitudes (no fue necesario su cálculo)\n")
  else:
    sys.stdout.write("Fila " + str(i+1) + ":\n")
  for j in range(len(all_similarities[i])):
    sys.stdout.write("\tFila " + str(all_similarities[i][j][1]+1) + " con similitud " + str(round(all_similarities[i][j][0],3)) + "\n")
sys.stdout.write("\n")
sys.stdout.write("Vecinos:\n")
for i in range(len(all_neighbors)):
  sys.stdout.write("[" + str(all_neighbors[i][1]+1) + "][" + str(all_neighbors[i][2]+1) + "]:\n") 
  for j in range(len(all_neighbors[i][0])):
    sys.stdout.write("\tFila " + str(all_neighbors[i][0][j][1]+1) + " con similitud " + str(round(all_neighbors[i][0][j][0],3)) + "\n")

```

Lo primero que hacemos aqui es desnormalizar los valores de la matriz de resultados y guardarlos en un fichero. Tras esto, guardamos en el fichero las predicciones que ha hecho el programa ordenandolas por posiciones en la matriz. Luego guardamos en el fichero las similitudes que ha calculado el programa de todas las filas con todas las filas. Finalmente, guardamos en el fichero los vecinos que ha usado el programa para calcular las predicciones.

## Ejemplos de uso

a la hora de ejeuctar el codigo es tan sencillo como poner en la terminal:

```
python3 /SistemasRecomendacion/src/main.py -f <fichero> -m <métrica> -p <predicción>
```

especificando con -f el nombre del fichero que queremos cargar y con -m la metrica que queremos usar para calcular la distancia entre vectores.

Un ejemplo de ejecucion seria:

```
python3 /SistemasRecomendacion/src/main.py -f utility-matrix-5-10-1 -m pearson -p simple
```

dando como resultado un fichero con los valores predecidos por el programa. Este fichero se encontraria en el directorio results con el nombre del fichero de datos y el sufijo -predicted.
