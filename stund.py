# Insper - Transferencia de Calor e Mecanica dos Sólidos - 2019.2
# ---------------------------------------------------------------------------------------------------
# STUND
# Software para calcular as forças de tração e compressão em Treliças 
# 
# Membros:
# - Arthur Olga
# - Guilherme Moraes
# - Iago Mendes
# - Vitor Satyro
# ---------------------------------------------------------------------------------------------------

from functions import *
import math
import numpy as np
#Pegando input do arquivo e salvando numa lista ja separado por espaço
txtInput = open("input.txt", "r").read()
listInput = txtInput.split("\n")

#Listas que serão salvas no dicionário
listIncidences = []
listCoordenates = []
listElements = []
listMaterials = []
listGeoProps = []
listBCNodes = []
listLoads = []

#Dicionário que irá conter todas as informações do Input do arquivo
dictInput = {}

for i in range(len(listInput)-1):
    #Analisa se a palavra começa com *
    if (listInput[i][0]=='*'):
        
        #Ve se logo apos o * a palavra começa com a letra comparada
        if (listInput[i][1] == 'C'):
            #Salvo o numero total de coordenadas
            numCoordenates = int(listInput[i+1])
            #Salva na lista de coordenadas os valores
            for j in range(1,numCoordenates+1):
                listCoordenates.append(listInput[i+j+1])
            #Salva no dicionário com a chave sendo a letra respectiva e o valor a lista
            dictInput["Coordinates"] = listCoordenates
        
        #O método se repete para todas as letras iniciais        
        elif (listInput[i][1] == 'E'):
            numElements = int(listInput[i+1])
            for j in range(1,numElements+1):
                listElements.append(listInput[i+j+1])
            dictInput["Elements"] = listElements

        elif (listInput[i][1] == 'I'):
            for j in range(1,numElements+1):
                listIncidences.append(listInput[i+j])
            dictInput["Incidences"] = listIncidences #quais nós são ligados pela barra
        
        elif (listInput[i][1] == 'M'):
            numMaterials = int(listInput[i+1])
            for j in range(1,numMaterials+1):
                listMaterials.append(listInput[i+j+1])
            dictInput["Material"] = listMaterials
        
        elif (listInput[i][1] == 'G'):
            numGeoProps = int(listInput[i+1])
            for j in range(1,numGeoProps+1):
                listGeoProps.append(listInput[i+j+1])
            dictInput["Geometric Properties"] = listGeoProps
        
        elif (listInput[i][1] == 'B'):
            numBCNodes = int(listInput[i+1])
            for j in range(1,numBCNodes+1):
                listBCNodes.append(listInput[i+j+1])
            dictInput["Restrictions"] = listBCNodes
        
        elif (listInput[i][1] == 'L'):
            numLoads = int(listInput[i+1])
            for j in range(1,numLoads+1):
                listLoads.append(listInput[i+j+1])
            dictInput["Loads"] = listLoads
#print(dictInput)
            
##############################################################################################################

# Passo 1: Pegar os dois pontos da incidencia, uma incidencia é igual a um K
# Passo 2: Com as Coord do ponto, calcular sen e cos e distancia
# Passo 3: Montar a matriz de cada K e preencher numa lista_K
# Passo 4: Montar o K Global (Numero de pontos * 2)
# Passo 5: Cortar as restrições na matriz K Global

# Montar matriz cheia de zeros
dimensao = len(listCoordenates) * 2
k_global = np.zeros((dimensao, dimensao))
k_global = k_global.tolist()

material = 0
for incidencia in listIncidences:
    incidencia = incidencia.split(' ')
    ponto1 = incidencia[1] 
    ponto2 = incidencia[2]

    for ponto in listCoordenates:
        ponto = ponto.split(' ')
        if ponto[0] == ponto1:
            coordenada1 = [float(ponto[1]), float(ponto[2])]
            incidencia1 = (int(ponto[0]) - 1)*2 + 1
            incidencia2 = (int(ponto[0]) - 1)*2 + 2

        elif ponto[0] == ponto2:
            coordenada2 = [float(ponto[1]), float(ponto[2])]
            incidencia3 = (int(ponto[0]) - 1)*2 + 1
            incidencia4 = (int(ponto[0]) - 1)*2 + 2

    incidencias = [incidencia1,incidencia2,incidencia3,incidencia4]
    distancia = math.sqrt((coordenada2[0] - coordenada1[0])**2 + (coordenada2[1] - coordenada1[1])**2)
    cos = (coordenada1[0] - coordenada2[0]) / distancia   
    sen = (coordenada1[1] - coordenada2[1]) / distancia 

    modulo_elasticidade = float(listMaterials[material].split(' ')[0])
    area = float(listGeoProps[material].split(' ')[0])
    constante = (modulo_elasticidade * area) / distancia

    c = (cos**2) * constante
    cs = (cos*sen) * constante
    s = (sen**2) * constante

    lista_ki = [[  c, cs, -c,-cs],
                [ cs,  s,-cs, -s],
                [ -c, cs,  c, cs],
                [-cs, -s, cs,  s]]

    linha = 0
    for i in incidencias:
        coluna = 0
        for j in incidencias:
            k_global[i-1][j-1] += lista_ki[linha][coluna]
            coluna +=1
        linha += 1
    material += 1 

k_global = np.matrix(k_global)
restricao = []
for delete in listBCNodes:
    restricao.append((int(delete[0])-1)*2 + int(delete[2])-1)

restricao = np.flip(np.sort(restricao), 0)

k_global = np.delete(k_global, (restricao), axis=0) #deleta linha
k_global = np.delete(k_global, (restricao), axis=1) #deleta coluna
k_global = k_global.tolist()

F = np.zeros((dimensao, 1))

for forca in listLoads:
    forca = forca.split(' ')

    for ponto in listCoordenates:
        ponto = ponto.split(' ')
        if ponto[0] == forca[0]:
            coordenada = [float(ponto[1]), float(ponto[2])]
            if forca[1] == '2':
                incidencia = (int(ponto[0]) - 1)*2 + 2
            elif forca[1] == '1':
                incidencia = (int(ponto[0]) - 1)*2 + 1
    
    F[incidencia-1] = forca[2]

F = np.delete(F, (restricao), axis=0) #deleta linha
F2 = []
for i in range(len(F)):
    F2.append(F[i][0])

r1, r2 = gauss_seidel(50, 0.000001, k_global, F2)

print(r1)

##############################################################################################################  
#Escrevendo arquivo de saída

output_file = open("output.txt", "w")

output_file.write("*DISPLACEMENTS\n")
output_file.write("resultados lalala\n\n")
output_file.write("*ELEMENT_STRAINS\n")
output_file.write("resultados lalala\n\n")
output_file.write("*ELEMENT_STRESSES\n")
output_file.write("resultados lalala\n\n")
output_file.write("*REACTION_FORCES\n")
output_file.write("resultados lalala\n\n")


output_file.close()