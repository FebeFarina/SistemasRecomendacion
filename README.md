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

lo primero que vemos al analizar el codigo son distinta funciones que usamos varias veces a lo largo del codigo, como son:

```python
def del_element(list, index):
  return list[:index] + list[index+1:]

def calculate_distance(row1, row2, metric):
  if metric == 'pearson':
    return np.corrcoef(row1, row2)[0][1]
  elif metric == 'cosine':
    return 1 - np.dot(row1, row2)/(np.linalg.norm(row1)*np.linalg.norm(row2))
  elif metric == 'euclidean':
    return np.linalg.norm(row1-row2)

def predict(neighbors, predict_type):
  result = 0
  div = 0
  for sim in highest:
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

La primera función se encarga de eliminar elementos en concreto de una lista dado un índice.
La segunda función la usamos a la hora de elegir la métrica de distancia, ya que dependiendo de la métrica que elijamos, la función que usaremos para calcular la distancia entre dos vectores será una u otra.

### Lectura de ficheros y parseo de argumentos

Lo siguiente que vemos en el código es como recoje y procesa los datos que entran por linea de comandos. Estos comandos serian el nombre del fichero donde estan los datos a cargar, y el segundo el tipo de métrica que queremos usar para calcular la distancia entre vectores y el último como deseamos predecir los valores, si de forma simple o usando la media de la fila.

```python
parser = argparse.ArgumentParser(description='Process filename.')
parser.add_argument('-f', '--file', type=str, help='filename', required=True)
parser.add_argument('-m', '--metric', type=str, help='metric', choices=['pearson', 'cosine', 'euclidean'], required=True)
parser.add_argument('-p', '--predict', type=str, help='predict', choices=['simple', 'meandif'], required=True)

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

como podemos apreciar tambien en el código anterior, lo primero que hacemos es leer los valores que seran el minimo valor y el maximo valor posible en la matriz. Tras esto, y miesntras leemos la matriz, normalizamos los datos a valores entre 0 y 1, para que no haya problemas a la hora de calcular las distancias entre vectores. En caso de encontrar un guion, lo sustituimos por un None, y en caso de que el valor no este dentro del rango, mostramos un error y salimos del programa.

Tras esto, buscamos con la siguiente funcion las filas en las que hemos encontrado un None, y las guardamos en una lista para usarlas mas adelante:

```python
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
# Llamamos main_rows a las filas que tienen valores vacíos
main_rows = []

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
Entraremos en un bucle que recorra las filas que tenienen valores vacios. Estos estan guardados aparte gracias al fragmento de codigo anterior.
Lo siguiente que haremos sera crear unas variables que nos ayudaran a calcular los valores que necesitamos. Estas variables son:

- flags: un array de booleanos que almacena un true si es un valor vacío y un false si no lo es
- similarities: un array de tuplas que almacena el numero de la fila dentro de la matriz y su valor de similaridad con la fila en la que estamos calculando el valor
- mean: es un array que almacena el promedio de cada fila

Ya entrando en el bucle lo que vamos a hacer es ir comparando entre la fila donde está el el valor a calcular con las otras para saber la similitud de las otras filas con la primera mencionada.

Importante mencionar que para poder movernos libremente por la matriz, vamos a ir haciendo copias de las filas que vamos comparando y así no perder los valores originales ni el tamaño original de estas.

#### eliminamos los otros Nones

Para poder sacar la similitud entre filas, primero debemos eliminar los valores de las columnas donde hay algún None, ya que si no, no podremos calcular la similitud entre filas:

```python
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
```

Debido a que estamos eliminando valores no solo en la columna de la fila que estamos comparando, sino tambien en la columna de la fila con la que estamos comparando, se pueden quedar valores sin analizar al desplazarse las filas, por eso tras cada eliminacion de un valor, retrocedemos en 1 el indice para que no se salte ningún valor.

#### Calculamos la similitud entre filas

Ya una vez eliminados los valores None, procedemos a calcular la similitud entre filas:

```python
 # No añadiremos las similitudes de las filas que no tengas valores en la misma columna que el valor a predecir
      if reviews[j][rows_og[1]] is not None:
          if np.std(main_copy) == 0 or np.std(other_copy) == 0:
            similarities.append((0,j))
          else:
            similarities.append((calculate_distance(main_copy,other_copy, args.metric),j))
      mean.append(np.mean(other_copy))
```

Lo primero que vemos en el fragmento de código anterior es que si la fila con la que estamos comparando no tiene valor en la misma columna que el valor a predecir, no añadiremos la similitud de esa fila a la lista de similitudes. Esto es debido a que no podremos calcular la similitud entre filas si no tienen valores en las mismas columnas.
Como podemos ver también, si la desviacion tipica de alguna de las filas es 0, no podremos calcular la similitud entre filas, por lo que en ese caso, añadiremos un 0 a la lista de similitudes.

En un caso normal, entraremos por el else, donde calcularemos la similitud dependiendo del tipo de métrica que hayamos elegido al inicio del programa. Tras esto, añadiremos la similitud a la lista de similitudes y el promedio de la fila a la lista de promedios.

Lo siguiente que hacemos es elegir de las similitudes los 2 valores mayores, ya que solo necesitamos 2 valores para calcular el valor a predecir:

```python
highest = heapq.nlargest(2, similarities)
```

#### Calculamos el valor a predecir

Ya una vez tenemos los 2 valores mas similares, procedemos a calcular el valor a predecir:

```python
result = 0
  div = 0
  # Hacemos la predicción considerando la diferencia con la media
  for sim in highest:
    result += sim[0] * (reviews[sim[1]][rows_og[1]]-mean[sim[1]])
    div += abs(sim[0])
  result =mean[rows_og[2]] + (result/div)
  matrix_result[rows_og[2]][rows_og[1]] = result
```

Lo primero que hacemos es inicializar las variables que vamos a usar para calcular el valor a predecir. Tras esto, y usando los 2 valores mayores de la lista de similitudes, procedemos a calcular el valor a predecir. Para ello, lo que hacemos es multiplicar la similitud de cada fila con la fila que tiene el valor a predecir por la diferencia entre el valor a predecir y el promedio de la fila con la que estamos comparando. Tras esto, dividimos el resultado entre la suma de los valores absolutos de las similitudes de las filas con la fila que tiene el valor a predecir. Finalmente, sumamos el resultado a la media de la fila con la que estamos trabajando y guardamos el resultado en la matriz de resultados.

Tras hacer todo lo mencionado anteriormente, obtenemos un valor que remplaza al none. Por lo que pasamos al siguiente none y repetimos el proceso hasta que no queden mas valores none en la matriz.

Es importante mencionar que en nuestro caso, a la hora de decidir y hacer el código, no usamos valores que estos mismos generan para obtener otros valores, esto lo hacemos a causa de que son predicciones y no valores reales, por lo que no queremos que un valor que hemos calculado influya en el calculo de otro valor.

### Retorno de resultados

Una vez cambiados todos los valores none por valores calculados por el programa, procedemos primero a desnormalizar los valores de la matriz de resultados:

```python

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

```

Tras esto, guardamos los resultados en un fichero de texto.
Importante mencionar que si el valor calculado es mayor que el valor maximo de la matriz, lo igualamos al valor maximo, y si es menor que el valor minimo, lo igualamos al valor minimo. Esto es un caso poco comun, pero puede darse debido a que solo exista un valor de similitud positivo, dando como resultado valores o demasiado altos o demasiado bajos.

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
