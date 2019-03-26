# Insper - Transferencia de Calor e Mecanica dos Sólidos - 2019.2
# ---------------------------------------------------------------------------------------------------
# STUND
# Software para calcular as forças de tração e compressão em Treliças 
# 
# Membros:
# - Vitor Satyro
# - Arthur Olga
# - Guilherme Moraes
# - Iago Mendes
# ---------------------------------------------------------------------------------------------------

from functions import *

#Criando objeto para teste - Mudar o nome do input da variavel
truss = Truss("input.txt",{})


#Função que cria o dicionario a partir de uma leitura de arquivo
def createDict (truss):

    #Pegando input do arquivo e salvando numa lista ja separado por espaço
    txtInput = open(truss.fileName, "r").read()
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
    dictInput = truss.dict

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
                dictInput["Incidences"] = listIncidences
            
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
    
            
##############################################################################################################

if __name__ == '__main__':
    m = [[1.59, -0.4, -0.54], [-0.4, 1.7, 0.4], [-0.54, 0.4, 0.54]]
    m = [[i * 1e8 for i in j] for j in m]

    F = [0, 150, -100]

    r1, r2 = jacobi(50, 0.0001, m, F)

    print(f'\nResultado: {r1}\nIterações: {r2}')

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