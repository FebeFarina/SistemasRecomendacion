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
    return list_other