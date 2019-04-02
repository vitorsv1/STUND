# STUND
Software de Treliça Universitário Dinâmico 

Desenvolvido por um grupo de estudantes universitários do Insper/SP, o STUND tem como premissa funcionar como uma API e/ou uma interface gráfica para análise matricial de estruturas baseadas em treliças.

## Como rodar

Tenha Python 3.6-2.7 e Numpy instalado

### Instale o Tkinter

#### No Ubuntu
```
sudo apt-get install python3-tk
```
#### No Windows
Já vem instalado

### Instale o VTK

```
pip3 install vtk
```
### Rode

```
python3 interface.py
```


## API
A STUND API é escrita em Python e serve para fazer todos os cálculos do programa; Nela, é possível inserir um arquivo .fem nos seguintes moldes:

```
*COORDINATES
3
1 0 0
2 0 0.4
3 0.3 0.4
*ELEMENT_GROUPS
3
1 1 BAR
2 1 BAR
3 1 BAR
*INCIDENCES
1 1 2
2 2 3
3 3 1
*MATERIALS
3
210E9 1570E6 1570E6
210E9 1570E6 1570E6
210E9 1570E6 1570E6
*GEOMETRIC_PROPERTIES
3
2E-4
2E-4
2E-4
*BCNODES
3
1 1
2 1
2 2
*LOADS
2
3 1 150
3 2 -100
```

A resposta da API vem na medida de um arquivo .out com:

```
*DISPLACEMENTS
 1 0.0000e+00 -9.5238e-07
 2 0.0000e+00 0.0000e+00
 3 1.6071e-06 -4.0179e-06
*ELEMENT_STRAINS
 1 2.380952e-06
 2 5.357143e-06
 3 -2.976190e-06
```

## Interface Gráfica (GUI)
Essa interface gráfica funciona como um programa de acesso à API de forma rápida e de simples utilização
