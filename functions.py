

# Implementar uma função para solução numérica do sistema de equações obtido na análise estrutural de treliças
# planas. (Met.Jacobi e Gauss-Seidel)
# Função retorna 
# U: vetor solução do sistema de equações.
# Erro: Erro associado.

def jacobi_gauss(ite, tol, K, F):
    