import numpy as np

# funcion que calcula la distancia entre dos filas
def calculate_distance(row1, row2, metric):
  if metric == 'pearson':
    if np.std(row1) == 0 or np.std(row2) == 0:
      return 0
    num = (np.array(row1) - np.mean(row1)).dot(np.array(row2) - np.mean(row2))
    den = (np.linalg.norm(np.array(row1) - np.mean(row1))*np.linalg.norm(np.array(row2) - np.mean(row2)))
    return num/den
  elif metric == 'cosine':
    if np.linalg.norm(row1) == 0 or np.linalg.norm(row2) == 0:
      return 0
    return np.dot(row1, row2)/(np.linalg.norm(row1)*np.linalg.norm(row2))
  elif metric == 'euclidean':
    return 1 / (1 + (np.linalg.norm(np.array(row1) - np.array(row2))))

def predict(neighbors, predict_type, reviews, rows_og, mean):
  result = 0
  div = 0
  for sim in neighbors:
    if predict_type == 'meandif':
      result += sim[0] * (reviews[sim[1]][rows_og[1]]-mean[sim[1]])
    elif predict_type == 'simple':
      result += sim[0] * (reviews[sim[1]][rows_og[1]])
    div += abs(sim[0])
  result =(result/div)
  if predict_type == 'meandif':
    result += mean[rows_og[2]]
  return result