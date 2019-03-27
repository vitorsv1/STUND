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

print(listCoordenates)

lista_k = []
material = 0
for incidencia in listIncidences:
    incidencia = incidencia.split(' ')
    ponto1 = incidencia[1] 
    ponto2 = incidencia[2]

    for ponto in listCoordenates:
        ponto = ponto.split(' ')
        if ponto[0] == ponto1:
            coordenada1 = [float(ponto[1]), float(ponto[2])]
        elif ponto[0] == ponto2:
            coordenada2 = [float(ponto[1]), float(ponto[2])]

    distancia = math.sqrt((coordenada2[0] - coordenada1[0])**2 + (coordenada2[1] - coordenada1[1])**2)
    cos = (coordenada1[0] - coordenada2[0]) / distancia   
    sen = (coordenada1[1] - coordenada2[1]) / distancia 

    modulo_elasticidade = float(listMaterials[material].split(' ')[0])
    area = float(listGeoProps[material].split(' ')[0])
    constante = (modulo_elasticidade * area) / distancia

    c = (cos**2) * constante
    cs = (cos*sen) * constante
    s = (sen**2) * constante

    print("\nBarra: " + str(material+1))
    print("c: " + str(c))
    print("cs: " + str(cs))
    print("s: " + str(s))
    lista_ki = [[c, cs, -c, -cs],
                [cs, s, -cs, -s],
                [-c, cs, c, cs],
                [-cs, -s, cs, s]]

    lista_k.append(lista_ki)
    material += 1 

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