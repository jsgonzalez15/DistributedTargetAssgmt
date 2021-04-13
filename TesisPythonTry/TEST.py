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

kpiFleet=np.array([33.683540299170986,30.30852352550388, 28.44059206353354, 29.864682358704176])
print("fleet",np.mean(kpiFleet), np.std(kpiFleet))
kpiDiv=np.array([27.321822666448412, 30.645665006211054, 30.938761468283566, 30.31597776423304])
print("div",np.mean(kpiDiv), np.std(kpiDiv))

GRIDkpiFleet=np.array([40.67266478917134, 38.09069102438195, 35.64525498029396, 37.809084534931436])
print("fleetGRID",np.mean(GRIDkpiFleet), np.std(GRIDkpiFleet))
GRIDkpiDiv=np.array([27.297148625465045, 32.88229813232855, 36.68073664169082, 38.5140722451969])
print("divGRID",np.mean(GRIDkpiDiv), np.std(GRIDkpiDiv))