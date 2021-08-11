"""
Réplica del Auction Algorithm y su adaptación al problema de asignación UAV a objetivos

@author: Juan Sebastián González Rojas 201612109
@email: js.gonzalez15@uniandes.edu.co
"""
import numpy as np
from numpy import doc
import GRIDassgmtFunctions as GRIDFcns
from matplotlib import pyplot as plt
import cv2
from mpl_toolkits import mplot3d
import time
import json

## Asymmetric implementation: n_v < n_t

nv=12
nt=4
Amatrix=np.random.rand(nv,nt)*100 #matrix of benefits
Pvector=np.zeros((1,nt))+0.000001 #initial vector of bidding cost
Passignments=np.zeros((1,nt))-1 #initial pairs of assignment
unassignedIndex=np.array(range(nv)) #vector of unassigned vehicle indexes
assignedIndex=np.delete(np.array(range(nv)),unassignedIndex)

AmatrixIter=np.array(Amatrix) #matrix of unassigned vehicle benefits
epsilon=2

while(not unassignedIndex.shape[0]==0):
    
    ##------------------------------- Bidding Fase
    if not assignedIndex.shape[0]==0:
        AmatrixIter=np.delete(Amatrix,assignedIndex,0)
        unassignedIndex=np.delete(np.array(range(nv)),assignedIndex,0)
    else:
        AmatrixIter=np.array(Amatrix)
    BmatrixIter=np.zeros((AmatrixIter.shape[0],nt)) #zero bidding matrix init
    AmatrixIter=AmatrixIter-(Pvector+np.zeros((AmatrixIter.shape[0],1))) #absolute benefit of each target

    vW=np.partition(AmatrixIter,-2) #first and second most valuable targets for selection
    vWdeltas= vW[:,-1]-vW[:,-2] #delta first-second for each vehicle
    AmatrixIterMax=np.max(AmatrixIter,axis=1)
    for i in range(nv-assignedIndex.shape[0]): #filling the Bmatrix
        colIndex=int(np.where(AmatrixIter[i,:]==AmatrixIterMax[i])[0]) #index of current bet
        bid=vWdeltas[i]+Pvector[0,colIndex]+epsilon
        BmatrixIter[i,colIndex]=bid
    ##------------------------------- Assignment Fase
    BmaxIter=np.max(BmatrixIter,axis=0) #bets in current iteration
    Pupdate=Pvector<BmaxIter #boolean vector of higher bid update
    Pvector=Pvector*(Pupdate-1)*(-1)+BmaxIter.reshape(1,BmaxIter.shape[0])*Pupdate #update of bidding
    Vupdate=unassignedIndex[np.where((BmaxIter==BmatrixIter)&(BmaxIter>0))[0]] #V-T pairs
    Passignments[np.where(Pupdate==True)]=Vupdate #V-T pair update
    assignedIndex=Passignments[np.where(Passignments!=-1)]

