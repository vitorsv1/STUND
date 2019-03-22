

# Implementar uma função para solução numérica do sistema de equações obtido na análise estrutural de treliças
# planas. (Met.Jacobi e Gauss-Seidel)
# Função retorna 
# U: vetor solução do sistema de equações.
# Erro: Erro associado.

def column(m, c):
  return [m[i][c] for i in range(len(m))]
 
def row(m, r):
  return m[r][:]
  
def height(m):
  return len(m)
  
def width(m):
  return len(m[0])

def jacobi(A,b,N=25,x=None):
    """Solves the equation Ax=b via the Jacobi iterative method."""
    # Create an initial guess if needed                                                                                                                                                            
    if x is None:
        x = zeros(len(A[0]))

    # Create a vector of the diagonal elements of A                                                                                                                                                
    # and subtract them from A                                                                                                                                                                     
    D = diag(A)
    R = A - diagflat(D)

    # Iterate for N times                                                                                                                                                                          
    for i in range(N):
        x = (b - dot(R,x)) / D
    return x

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
