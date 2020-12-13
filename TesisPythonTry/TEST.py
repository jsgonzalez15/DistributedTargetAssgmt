import numpy as np
from numpy import doc
import GRIDassgmtFunctions as GRIDFcns
from matplotlib import pyplot as plt
import cv2
from mpl_toolkits import mplot3d
import time
import json
[radOper,PtOptimum,vOptimum,capJoules]=GRIDFcns.CalcularParametrosEnergeticos()
print(radOper)
print(PtOptimum)
print(vOptimum)

w=np.ones(10)
wIter=np.c_[w,w*2,w,w]
w[0]=5
Amatrix=np.random.rand(10,6)*100
asignE= Amatrix<200
asigned=np.zeros((Amatrix.shape[0],Amatrix.shape[1]))
asignPtoR=np.dot(np.ones((1,asignE.shape[0])),asignE)==0
'''
print("asignE: ",asignE)
for row in range(Amatrix.shape[0]):
    infArc=100000.0 #arco con valor infinito (no será considerado para calcular arcos minimos) 
    asignEdeleted=np.dot(np.ones((1,asignE.shape[0])),asignE)==0
    if row==Amatrix.shape[1]:
        break
    #arcos restantes (sin p asignados, sus arcos y arcos de q respectivos)
    remainingArcs=Amatrix+(asignE-1)*(-1)*infArc+asigned*infArc
    #print("remainingArcs: ",remainingArcs)
    currMin=np.min(remainingArcs) #arco mínimo global por q para todo p
    if currMin>=infArc:
        break
    #print("arcos minimos", currMin)
    deleteNonMax=remainingArcs==currMin #matriz booleana actual para eliminar arcos desde q y desde p
    [rowIndex,colIndex]=np.where(remainingArcs==currMin) #indice de p seleccionado
    rowIndex=np.array(rowIndex)[0]
    colIndex=np.array(colIndex)[0]

    asignE[rowIndex,:]=asignE[rowIndex,:]*False #eliminado de arcos no mínimos desde q
    asignE[:,colIndex]=asignE[:,colIndex]*False #eliminado de arcos no mínimos desde p
    asigned[rowIndex,colIndex]=True
    print("asigned: ")
    print(asigned)
print("Amatrix:")
print(Amatrix)'''

ey=np.array([[7,8,9,4,5,6,1,2,3]])
currentLine=np.where(ey==6)
print(len(range(4)))

