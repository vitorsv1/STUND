# Implementar uma função para solução numérica do sistema de equações obtido na análise estrutural de treliças
# planas. (Met.Jacobi e Gauss-Seidel)
# Função retorna 
# U: vetor solução do sistema de equações.
# Erro: Erro associado.

class Truss:
  def __init__(self, fileName, dictio={}):
    self.fileName = fileName
    self.dict = dictio

def column(m, c):
  return [m[i][c] for i in range(len(m))]
 
def row(m, r):
  return m[r][:]
  
def height(m):
  return len(m)
  
def width(m):
  return len(m[0])

def erro(x, i, Tol):
    counter = 0
    for n in range(len(x[i])):
        if (x[i][n]==0): return False
        erro = (x[i][n] - x[i-1][n]) / x[i][n]
        if (abs(erro) < Tol):
            counter += 1
    if (counter == len(x[i])):
        print('\nTolerância atingida')
        return True
    return False

def jacobi(Ite,Tol,K,F):
    numIte = 0
    x = [[0]*len(K[0])]
    for i in range(1, Ite):
        x_step = [0]*len(K[0])
        for n in range(len(K[0])):
            x_step[n] = F[n]
            for n_step in range(len(K[0])):
                x_step[n] -= K[n][n_step] * x[i-1][n_step]
            x_step[n] += K[n][n]*x[i-1][n]
            x_step[n] /= K[n][n]
        print(x_step)
        x.append(x_step)
        numIte = i
        if erro(x, i, Tol): break
    return x[-1], numIte + 1

def gauss_seidel(Ite,Tol,K,F):
  numIte = 0
  current_X = [0]*len(K[0])
  x = [current_X]
  for i in range(1, Ite):
      x_step = [0]*len(K[0])
      for n in range(len(K[0])):
          x_step[n] = F[n]
          for n_step in range(len(K[0])):
              x_step[n] -= K[n][n_step] * current_X[n_step]
          x_step[n] += K[n][n] * current_X[n]
          x_step[n] /= K[n][n]
          current_X[n] = x_step[n]
      print(x_step)
      x.append(x_step)
      numIte = i
      if erro(x, i, Tol): break
  return x[-1], numIte + 1