

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


def gauss_seidel(m, x0=None, eps=1e-5, max_iteration=100):
  """
  Parameters
  ----------
  m  : list of list of floats : coefficient matrix
  x0 : list of floats : initial guess
  eps: float : error tolerance
  max_iteration: int
  
  Returns
  -------  
  list of floats
      solution to the system of linear equation
  
  Raises
  ------
  ValueError
      Solution does not converge
  """
  n  = height(m)
  x0 = [0] * n if x0 == None else x0
  x1 = x0[:]

  for __ in range(max_iteration):
    for i in range(n):
      s = sum(-m[i][j] * x1[j] for j in range(n) if i != j) 
      x1[i] = (m[i][n] + s) / m[i][i]
    if all(abs(x1[i]-x0[i]) < eps for i in range(n)):
      return x1 
    x0 = x1[:]    
  raise ValueError('Solution does not converge')    
