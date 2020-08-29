"""
Métodos para réplica de GRID Target Assgmt.

Funciones:
* InitialPlot gráfica inicial, organización de información y relacion visual de información.
* CurrentCell funcion para obtener id de celda actual.
* UAVandTargetInCell funcion que retorna UAVs y targets en la celda actual.
* MoveUAVtoTarget funcion que mueve UAVs segun tipo de UAV y asignación.

@author: Juan Sebastián González Rojas 201612109
"""
from matplotlib import pyplot
import numpy as np
import math
def CurrentCell(p:list,C:list,radOper:int,div:int)->int:
    #Retorna la celda actual del UAV
    currentColumn=math.ceil((p[1]/(radOper/1000))*div) #columna actual
    currentLine=math.ceil((p[2]/(radOper/1000))*div) #fila actual
    yourCell=C[currentLine][currentColumn] #celda actual
    return yourCell

C=[]
div=3
for i in range(div):
    C=C.append(list(range(i*div+1,i*div)))
print(C)