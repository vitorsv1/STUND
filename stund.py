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
# Pegando input do arquivo e salvando numa lista ja separado por espaço


def read(file):
    txtInput = open(file, "r").read()
    listInput = txtInput.split("\n")

    # Listas que serão salvas no dicionário
    listIncidences = []
    listCoordenates = []
    listElements = []
    listMaterials = []
    listGeoProps = []
    listBCNodes = []
    listLoads = []

    # Dicionário que irá conter todas as informações do Input do arquivo
    dictInput = {}

    for i in range(len(listInput)-1):
        # Analisa se a palavra começa com *
        if (listInput[i][0] == '*'):

            # Ve se logo apos o * a palavra começa com a letra comparada
            if (listInput[i][1] == 'C'):
                # Salvo o numero total de coordenadas
                numCoordenates = int(listInput[i+1])
                # Salva na lista de coordenadas os valores
                for j in range(1, numCoordenates+1):
                    listCoordenates.append(listInput[i+j+1])
                # Salva no dicionário com a chave sendo a letra respectiva e o valor a lista
                dictInput["Coordinates"] = listCoordenates

            # O método se repete para todas as letras iniciais
            elif (listInput[i][1] == 'E'):
                numElements = int(listInput[i+1])
                for j in range(1, numElements+1):
                    listElements.append(listInput[i+j+1])
                dictInput["Elements"] = listElements

            elif (listInput[i][1] == 'I'):
                for j in range(1, numElements+1):
                    listIncidences.append(listInput[i+j])
                # quais nós são ligados pela barra
                dictInput["Incidences"] = listIncidences

            elif (listInput[i][1] == 'M'):
                numMaterials = int(listInput[i+1])
                for j in range(1, numMaterials+1):
                    listMaterials.append(listInput[i+j+1])
                dictInput["Material"] = listMaterials

            elif (listInput[i][1] == 'G'):
                numGeoProps = int(listInput[i+1])
                for j in range(1, numGeoProps+1):
                    listGeoProps.append(listInput[i+j+1])
                dictInput["Geometric Properties"] = listGeoProps

            elif (listInput[i][1] == 'B'):
                numBCNodes = int(listInput[i+1])
                for j in range(1, numBCNodes+1):
                    listBCNodes.append(listInput[i+j+1])
                dictInput["Restrictions"] = listBCNodes

            elif (listInput[i][1] == 'L'):
                numLoads = int(listInput[i+1])
                for j in range(1, numLoads+1):
                    listLoads.append(listInput[i+j+1])
                dictInput["Loads"] = listLoads
    return dictInput
# print(dictInput)

##############################################################################################################
# Passo 1: Pegar os dois pontos da incidencia, uma incidencia é igual a um K
# Passo 2: Com as Coord do ponto, calcular sen e cos e distancia
# Passo 3: Montar a matriz de cada K e preencher numa lista_K
# Passo 4: Montar o K Global (Numero de pontos * 2)
# Passo 5: Cortar as restrições na matriz K Global


def main(file="arquivodeentrada.fem", funcType=1, ite=80):
    print("\n")
    diction = read(file)
    listCoordenates = diction["Coordinates"]
    listLoads = diction["Loads"]
    listIncidences = diction["Incidences"]
    listMaterials = diction["Material"]
    listGeoProps = diction["Geometric Properties"]
    listBCNodes = diction["Restrictions"]

    # Montar matriz cheia de zeros
    dimensao = len(listCoordenates) * 2
    k_global = np.zeros((dimensao, dimensao))
    k_global = k_global.tolist()

    # Faz o vetor de forças
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

    barra = {}

    # Faz a matriz global
    material = 0
    listBars = []
    for incidencia in listIncidences:
        incidencia = incidencia.split(' ')
        ponto1 = incidencia[1]
        ponto2 = incidencia[2]
        listBars.append([int(ponto1), int(ponto2)])

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

        incidencias = [incidencia1, incidencia2, incidencia3, incidencia4]
        distancia = math.sqrt(
            (coordenada2[0] - coordenada1[0])**2 + (coordenada2[1] - coordenada1[1])**2)
        cos = (coordenada1[0] - coordenada2[0]) / distancia
        sen = (coordenada1[1] - coordenada2[1]) / distancia

        modulo_elasticidade = float(listMaterials[material].split(' ')[0])
        area = float(listGeoProps[material].split(' ')[0])
        constante = (modulo_elasticidade * area) / distancia
        barra[int(incidencia[0])] = [distancia, cos,
                                     sen, modulo_elasticidade, incidencias]

        c = (cos**2) * constante
        cs = (cos*sen) * constante
        s = (sen**2) * constante

        lista_ki = [[c, cs, -c, -cs],
                    [cs,  s, -cs, -s],
                    [-c, cs,  c, cs],
                    [-cs, -s, cs,  s]]

        linha = 0
        for i in incidencias:
            coluna = 0
            for j in incidencias:
                k_global[i-1][j-1] += lista_ki[linha][coluna]
                coluna += 1
            linha += 1
        material += 1
    k_global = np.matrix(k_global)

    # Monta a lista com restrições
    restricao = []
    listNodes = []
    for delete in listBCNodes:
        listNodes.append([int(delete[0]), int(delete[2])])

        restricao.append((int(delete[0])-1)*2 + int(delete[2])-1)
    restricao = np.flip(np.sort(restricao), 0)

    # Faz as restrições na matriz global e salva em k_restrito
    k_restrito = np.delete(k_global, (restricao), axis=0)  # deleta linha
    k_restrito = np.delete(k_restrito, (restricao), axis=1)  # deleta coluna
    k_restrito = k_restrito.tolist()

    # Restrições na matriz força
    F = np.delete(F, (restricao), axis=0)  # deleta linha
    F2 = []
    for i in range(len(F)):
        F2.append(F[i][0])
    if funcType == 1:
        print("Tipo utilizado: Gauss")
        u_restrito, r2 = gauss_seidel(ite, 0.000001, k_restrito, F2)
    else:
        print("Tipo utilizado: Jacobi")
        u_restrito, r2 = jacobi(ite, 0.000001, k_restrito, F2)
    u_final = np.zeros((dimensao, 1))
    u_final = u_final.tolist()
    i = 0
    nao_restricao = []
    for r in range(len(u_final)):
        if r not in restricao:
            u_final[r] = (u_restrito[i])
            i += 1
            nao_restricao.append(r)
        if r in restricao:
            u_final[r] = 0

    deformacoes = []
    tensao = []
    for i in barra:
        cos, sen = barra[i][1], barra[i][2]
        # print(cos, sen)
        indices = barra[i][4]
        # print(indices)
        x = np.array([u_final[indices[0]-1], u_final[indices[1]-1],
                      u_final[indices[2]-1], u_final[indices[3]-1]])
        matriz = np.array([-cos, -sen, cos, sen])
        # print(x)
        # print(matriz)
        deformacao = (1/barra[i][0])*np.dot(matriz, x)

        deformacoes.append(deformacao)
        tensao.append(deformacao * barra[i][3])

    # k global sem restrições * u completo = forças
    forcas = np.dot(u_final, k_global)
    forcas = forcas.tolist()
    # forcas = np.delete(forcas, (nao_restricao), axis=1).round(3)
    forcas_format = forcas[0]
    for i in range(len(forcas_format)):
        if i not in restricao:
            forcas_format[i] = 0

    ##############################################################################################################
    # Escrevendo arquivo de saída
    output_file = open("arquivoSaida.out", "w")
    listPoints = []
    listDisplaced = []
    output_file.write("*DISPLACEMENTS\n")
    for ponto in listCoordenates:
        ponto = ponto.split(' ')
        incidencia1 = (int(ponto[0]) - 1)*2 + 1
        incidencia2 = (int(ponto[0]) - 1)*2 + 2
        listPoints.append([float(ponto[1]), float(ponto[2])])

        listDisplaced.append(
            [float(ponto[1])+float(u_final[incidencia1-1])*1000, float(ponto[2])+float(u_final[incidencia2-1])*1000])

        output_file.write(str(ponto[0]) + ' ' + str(u_final[incidencia1-1]
                                                    ) + ' ' + str(u_final[incidencia2-1]) + '\n')

    output_file.write("*ELEMENT_STRAINS\n")
    for i in range(len(deformacoes)):
        output_file.write(str(i+1) + ' ' + str(deformacoes[i]*(-1)) + '\n')

    output_file.write("*ELEMENT_STRESSES\n")

    for i in range(len(deformacoes)):
        output_file.write(str(i+1) + ' ' + str(tensao[i]*(-1)) + '\n')

    output_file.write("*REACTION_FORCES\n")
    for i in range(len(forcas_format)):
        if int(forcas_format[i]) != 0:
            if i % 2 == 0:
                if i == 0:
                    output_file.write(str(1) + ' FX = ' +
                                      str(forcas_format[i]) + '\n')
                else:
                    ponto = math.ceil(((i-1)/2)+1)
                    output_file.write(str(ponto) + ' FX = ' +
                                      str(forcas_format[i]) + '\n')
            else:
                if i == 1:
                    output_file.write(str(1) + ' FY = ' +
                                      str(forcas_format[i]) + '\n')
                else:
                    ponto = math.ceil(((i-2)/2)+1)
                    output_file.write(str(ponto) + ' FY = ' +
                                      str(forcas_format[i]) + '\n')

    output_file.close()
    plotDict = {}

    plotDict["Pontos"] = listPoints
    plotDict["Barras"] = listBars
    plotDict["Deformacoes"] = tensao
    plotDict["Deformados"] = listDisplaced
    plotDict["Iteracoes"] = r2

    print("Numero de iteracoes:"+str(r2))
    print("Resultados salvos em: arquivoSaida.out")
    print("Fim de execução\n\n")
    return plotDict


if __name__ == "__main__":
    main()
