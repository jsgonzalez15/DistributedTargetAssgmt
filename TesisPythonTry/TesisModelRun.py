"""
1. Diseño de control distribuido con asignación de menor costo.

Temas:
* Consumo energético.
* Eficiencia de método iterativo.
* Incidencia en concentración de agentes.
* Efectos de puntos de inicio en el mapa.
* Eficiencia de partición espacial iterativa.

@author: Juan Sebastián González Rojas 201612109
@email: js.gonzalez15@uniandes.edu.co
"""
import GRIDassgmtFunctions as GRIDFcns
import TesisModelFunctions as TesisFcns
from matplotlib import pyplot as plt
import numpy as np
import cv2
import time
import json
import pyglet
#####################################################################################################################
##                               Simulación de Método Distribuido: Min Costo UAV/Destino
#####################################################################################################################
np.seterr(divide='ignore', invalid='ignore')
#calculo de radio de Operaciones, consumo y vel óptimos
[radOper,PtOptimum,vOptimum,capJoules]=GRIDFcns.CalcularParametrosEnergeticos()
''' Parámetros generales de simulación'''
qPerUAV=6 #Proporción de objetivos por UAV
desv_w_p=0 #max desv de consumo entre UAVs (ideal 0)
simPorDensidad=250 #n sim por densidad
divMethod="GRID" #tipo de particion del espacio (GRID,)
dt=0.3

theRange=range(1,5)#1,2)

w_Densidad=np.array([]) #valores medios y desviación estándar por densidad de consumo
w_Div=np.zeros((int(2.1*qPerUAV),len(theRange))) #valores promedio de consumo por UAV por división para 4 divisiones
w_DivTotal=np.zeros((int(2.1*qPerUAV),len(theRange))) #valores totales de consumo por flota por división para 4 divisiones
q_Div=np.zeros((int(2.1*qPerUAV),len(theRange)))
w_DivStandar=np.zeros((int(2.1*qPerUAV),len(theRange)))
w_DivTotalStandar=np.zeros((int(2.1*qPerUAV),len(theRange)))
q_DivStandar=np.zeros((int(2.1*qPerUAV),len(theRange)))

video=False  #obtener un video de simulación (True) ejecutar sin video (False)
simGRID=True #simular asignación y traslado GRID target Assgmt (True)
pureGRID=False #simular algoritmo GRID target Assgmt (True)
autom=1 #autom sim(1)/ver todo(0)
changeDiv=0 #cambiar div durante sim(1)/ mantener div(0)

'''###NO REALIZAR AMBOS FOR CONSECUTIVAMENTE, UNO DE LOS DOS DEBE TENER UNA ÚNICA SIMULACIÓN'''
######################################################################################################
##                      Repeticiones para obtener efecto de número de divisiones
######################################################################################################
for divIniciales in theRange: 

    ######################################################################################################
    ##                      Repeticiones para obtener efecto de número de divisiones
    ######################################################################################################
    for divIniciales2 in range(3,4):
        w_Sim=np.zeros((int(2.1*qPerUAV),simPorDensidad)) #valores medios y desviación estándar en consumo por iteración
        w_SimTotal=np.zeros((int(2.1*qPerUAV),simPorDensidad)) #valores de simulación total de la flota
        q_Sim=np.zeros((int(2.1*qPerUAV),simPorDensidad))

        ######################################################################################################
        ##                      Simulaciones para obtener caso promedio y desviación estándar
        ######################################################################################################
        for simActual in range(simPorDensidad):
            ''' ############################  Inicialización escenario, UAVs, Puntos Recolección y objetivos  ############################ '''
            nQ=30+15*divIniciales2 #Numero de Objetivos
            nP=round(nQ/qPerUAV) #Numero de UAVs segun densidad deseada
            nR=5 #Numero de Puntos Recolección/despliegue

            r=np.random.rand(nR,2)*radOper/1000 #(x,y) posiciones [km] de recolectores en AreaOperaciones
            q=np.random.rand(nQ,2)*radOper/1000 #(x,y) posiciones [km] de objetivos en AreaOperaciones 
            qNodes=np.ones(nQ)*(-1) #(z) nodos en los que se encuentran q
            allQMet=np.array([]) #Objetivos que han sido alcanzados (inicializado con valor dummie)

            w=np.ones(nP)*capJoules #Registro de consumo por UAV (Energía restante)
            winit=np.array(w)
            wIter=np.ones(int(2.1*qPerUAV))
            wIterTotal=np.ones(int(2.1*qPerUAV))
            allQMetIter=np.ones(int(2.1*qPerUAV))

            p= np.random.rand(nP,2)*radOper/1000   #inicializacion de matriz de UAVs
            if not pureGRID:
                for pItem in range(nP): #Ubicaciones iniciales en Recolectores aleatorios 
                    p[pItem]=r[int(round(np.random.rand()*nR-0.5))] + (np.random.rand(1,2)-0.5)

            pNodes=np.ones(nP)*(-1) #nodos en los que se encuentra p
            pReturned=np.zeros((nP,1)) #indicador de retorno a recolector
            pReturning=np.zeros((nP,1)) #p returnando a recolectores
            pZero=np.array(p)

            ''' Asignación de puntos de recolección a objetivos'''
            RperQ=np.array(q) #(x,y) posiciones [km] recolector asignado por q

            #distancias de objetivos a recolectores para obtener asignación Q to R (RperQ)
            xRQ= r[:,0].reshape(r.shape[0],1)-q[:,0].reshape(1,q.shape[0]) #componente en x
            yRQ= r[:,1].reshape(r.shape[0],1)-q[:,1].reshape(1,q.shape[0]) #componente en y
            distRQ= np.sqrt(np.add(np.square(xRQ),np.square(yRQ))) #matriz norma de distancias
            for target in range(q.shape[0]): # Actualizacion de recolectores asignados por vehiculo
                #recolector más cercano a q actual
                RperQ[target,:]=r[np.where(distRQ[:,target]==np.min(distRQ[:,target]))[0]]
                
            ################################ division de espacio en cuadrículas ################################
            if autom:
                div=divIniciales #div default
            else:
                div=input('Ingrese el numero de divisiones') #base y altura de la malla (div personalizado)

            C=np.array([range((div-1)*div+1,div*div+1)]) # Matriz de indices para identificar celdas
            for i in range(div-1,0,-1):
                C=np.append(C,[range((i-1)*div+1,div*i+1)],axis=0)
            TesisFcns.initialScatter(q,r,p,pZero,div,radOper,C,autom,video,allQMet) #ploteo inicial
            ####################################################################################################

            if video:
                fourcc=cv2.VideoWriter_fourcc(*'MP4V')
                theVideo=cv2.VideoWriter('TesisSimVideo.mp4',fourcc,10,(640,480))

            if simGRID:
                deltaMatrix=np.zeros((2*div,div)) #delta Q-P local y propagado en filas por columnas
                deltaRow=np.zeros((1,div)) #delta Q-P fila de intercambio
            '''##################################################################################################################
            ##                                      EJECUCIÓN PRINCIPAL DEL ALGORITMO
            #####################################################################################################################'''
            for iter in range(int(2.1*qPerUAV)): #Sim hasta:(a) todo P ha llegado, o, (b) Q agotados

                wPrev=np.array(w) #registro de anterior energía almacenada
                for deltaT in range(150):
                    print("// Div iniciales: ", divIniciales,"// Simulación actual: ",simActual,"// Iteración simulada: ", iter," /// Delta T simulado: ", deltaT)
                    qDone=np.array([]) #lista de indices de objetivos alcanzados para eliminación en ciclo final
                    qDoneU=np.array([]) #lista de indices alcanzados para eliminación parcial (ciclo Internodal)
                    nodesMet=True #booleano que indica si los objetivos fueron alcanzados en todos los nodos
                    indexU=np.array([]) #arreglo de indices de P unassigned
                    finalReturn=False 
                    ######################################################################################################
                    ##                      Asignación y Movimiento Intranodal
                    ######################################################################################################
                    for nodoActual in range(1,div**2+1): #recorrido sobre todos los nodos 
                        [pInNode, indexP, qInNode, indexQ]= TesisFcns.pqrInNode(nodoActual,p,q,r,C,radOper,div,divMethod)
                        if not np.array(indexQ).shape[0]==0:
                            qNodes[np.array(indexQ).astype(int)]=nodoActual #nodos de Q
                        if not np.array(indexP).shape[0]==0:
                            pNodes[np.array(indexP).astype(int)]=nodoActual #nodos de Q
                        indexUinNode=np.array([]) #indices de U dentro del nodo

                        [currentLine,currentColumn]=np.where(C==nodoActual)
                        if simGRID:
                            deltaMatrix[(div-currentLine-1)*2+1,currentColumn]=qInNode.shape[0]-pInNode.shape[0] #delta local
                            if not currentLine==div-1: #delta propagado
                                deltaMatrix[(div-currentLine-1)*2,currentColumn]=deltaMatrix[((div-currentLine-1)-1)*2+1,currentColumn]+deltaMatrix[((div-currentLine-1)-1)*2,currentColumn]
                            if currentLine==0 and (not currentColumn==div-1):
                                deltaRow[0,currentColumn]=deltaRow[0,currentColumn+1]+deltaMatrix[(div-1)*2+1,currentColumn+1]+deltaMatrix[(div-1)*2,currentColumn+1]

                        if (not pInNode.shape[0]==0) and (qInNode.shape[0]==0): #solo hay U (no hay Q) en Nodo actual
                            indexUinNode=np.array(indexP)

                        if (not pInNode.shape[0]==0) and not (qInNode.shape[0]==0): #hay p y q en Nodo actual 
                            Amatrix= np.zeros((qInNode.shape[0],pInNode.shape[0])) #inicialización de matriz de pesos
                            RperQNode=np.array(RperQ[np.array(indexQ)]) #R^[i]

                            #Matriz de distancias P_i a Q_i
                            xdeltapq= qInNode[:,0].reshape(qInNode.shape[0],1)-pInNode[:,0].reshape(1,pInNode.shape[0])
                            ydeltapq= qInNode[:,1].reshape(qInNode.shape[0],1)-pInNode[:,1].reshape(1,pInNode.shape[0])
                            distancepq= np.sqrt(np.add(np.square(xdeltapq),np.square(ydeltapq)))

                            #Matriz de distancias Q_i a R_i
                            xdeltaqr= np.zeros((pInNode.shape[0],1))+ RperQNode[:,0].reshape(1,qInNode.shape[0]) -qInNode[:,0].reshape(1,qInNode.shape[0])
                            ydeltaqr= np.zeros((pInNode.shape[0],1))+ RperQNode[:,1].reshape(1,qInNode.shape[0]) -qInNode[:,1].reshape(1,qInNode.shape[0])
                            distanceqr= np.sqrt(np.add(np.square(xdeltaqr),np.square(ydeltaqr))).T

                            Amatrix=1000*distancepq*PtOptimum/vOptimum +1000*distanceqr*PtOptimum/vOptimum #matriz de pesos
                            wNode=w[indexP]
                            asignE=Amatrix<wNode #inicialización de la matriz con arcos que pueden ser recorridos
                            #asignE=asignE*(np.zeros((Amatrix.shape))+wMin<wNode)

                            #Matriz de distancias P_i a R
                            xdeltapr= r[:,0].reshape(r.shape[0],1)-pInNode[:,0].reshape(1,pInNode.shape[0])
                            ydeltapr= r[:,1].reshape(r.shape[0],1)-pInNode[:,1].reshape(1,pInNode.shape[0])
                            distancepr= np.sqrt(np.add(np.square(xdeltapr),np.square(ydeltapr)))

                            #Casos de retorno P a R
                            asignPtoR=np.dot(np.ones((1,asignE.shape[0])),asignE)==0
                            #Ignorar casos de retorno actual
                            if not np.sum(pReturning[indexP])==0:
                                asignE[:,np.where(pReturning[indexP]==1)[0]]=False
                            asignPtoR=asignPtoR.reshape(asignPtoR.shape[1],1)
                            if not np.sum(asignPtoR)==0:
                                pReturning[np.array(indexP)[np.where(asignPtoR==1)[0]]]=1

                            if not pureGRID:
                                for rC in range(asignE.shape[1]): #Possible return Column
                                    if asignPtoR[rC]:
                                        rR= np.array(np.where(distancepr[:,rC]==np.min(distancepr[:,rC]))[0])[0] #return Row (distancia a r más cercano)
                                        pLlegadaR=distancepr[rR,rC]<=dt #matriz con booleanos para llegada
                                        #deltax y deltay individual segun distancia restante
                                        prdeltax=(pLlegadaR-1)*(-1)*(np.nan_to_num(xdeltapr[rR,rC]/distancepr[rR,rC]))*dt +pLlegadaR*(xdeltapr[rR,rC])
                                        prdeltay=(pLlegadaR-1)*(-1)*(np.nan_to_num(ydeltapr[rR,rC]/distancepr[rR,rC]))*dt +pLlegadaR*(ydeltapr[rR,rC])
                                        pInNode[rC]=pInNode[rC]+np.c_[prdeltax,prdeltay]
                                        p[indexP[rC]]=pInNode[rC] #actualizacion en posicion global
                                        w[indexP[rC]]=w[indexP[rC]]- 1000*np.sqrt(np.square(prdeltax)+np.square(prdeltay))*PtOptimum/vOptimum
                                        if distancepr[rR,rC]<=dt/2:
                                            pReturned[indexP[rC]]=1 #Retorno a Recolector
                            
                            asigned=np.zeros((qInNode.shape[0],pInNode.shape[0])) #matriz con p asignados
                            Amatrix= Amatrix-1000*distanceqr*PtOptimum/vOptimum #Actualizacion a pesos por recorrido individual
                            
                            #eliminacion de arcos no eficientes
                            for row in range(Amatrix.shape[0]):
                                infArc=100*capJoules #arco con valor infinito (no será considerado para calcular arcos minimos) 
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
                                #print("asignE actual: ",asignE)

                            pLlegada=distancepq<=dt #matriz con booleanos para llegada
                            #deltax y deltay matricial segun distancia restante
                            deltax=(pLlegada-1)*(-1)*(np.nan_to_num(xdeltapq/distancepq))*asigned*dt +pLlegada*(xdeltapq)*asigned
                            deltay=(pLlegada-1)*(-1)*(np.nan_to_num(ydeltapq/distancepq))*asigned*dt +pLlegada*(ydeltapq)*asigned 
                            
                            #Movimiento segun asignacion (movimiento unitario o movimiento de llegada)
                            xmove=np.dot(np.ones(asignE.shape[0]),deltax)
                            ymove=np.dot(np.ones(asignE.shape[0]),deltay)

                            if(not (np.all(deltax<=dt) and np.all(deltay<=dt))) or (not (np.all(xmove<=dt) and np.all(ymove<=dt))):
                                print("/////////////////////////////////////////////////////////////")
                                print("////////////////////////--ALERTA EN P--//////////////////////")
                                print("/////////////////////////////////////////////////////////////")
                                print(not (np.all(deltax<=dt) and np.all(deltay<=dt)))
                                print(not (np.all(xmove<=dt) and np.all(ymove<=dt)))
                                print("deltax: ", deltax,"deltay: ", deltay)
                                time.sleep(10) #alerta al usuario que el algoritmo está fallando

                            p[indexP]=pInNode +np.c_[xmove,ymove]
                            w[indexP]=w[indexP]- 1000*np.sqrt(np.add(np.square(xmove),np.square(ymove)))*PtOptimum/vOptimum

                            #Identificacion de objetivos recorridos en celda actual
                            inNodeQdone=np.where(distancepq<=0.01)[0]
                            if inNodeQdone.shape[0]+np.sum(pReturned[indexP])>=qInNode.shape[0] or inNodeQdone.shape[0]+np.sum(pReturned[indexP])>=pInNode.shape[0]:
                                inNodeQdone=np.array(indexQ)[inNodeQdone] #transformacion a indices en Q global
                                qDoneU=np.concatenate((qDoneU,np.array(inNodeQdone))) #se agregan indices a globales
                                qDoneU=qDoneU.astype(int) #se asegura que sean de tipo int
                                nodesMet=nodesMet and True  #celda actual satisface asignacion
                            else:
                                nodesMet=nodesMet and False #celda actual no satisface asignacion
                                qDone=np.array([]) #reinicio de indices para proxima delta
                            if nodesMet:
                                qDone=np.concatenate((qDone,np.array(inNodeQdone))) #se agregan indices a globales
                                qDone=qDone.astype(int) #se asegura que sean de tipo int

                            #Guardado de indices en U y nodos asociados
                            currU= (np.dot(np.ones(asignE.shape[0]),asigned).astype(int)-1)*(-1) #vector bool con U en Nodo actual
                            indexUinNode=np.where(currU==True)[0]
                            indexUinNode=np.array(indexP)[indexUinNode]
                        
                        indexU=np.concatenate((indexU,np.array(indexUinNode)))
                    print("Size de no asignados acumulado: ", indexU.shape)
                    print("Size de objetivos alcanzados: ", qDone.shape)

                    ######################################################################################################
                    ##                      Asignación y Movimiento Internodal
                    ######################################################################################################
                    if not indexU.shape[0]-np.sum(pReturning)==0:
                        print("/////////////////////////--INTERNODAL--//////////////////////")
                        indexU=indexU.astype(int)
                        u=np.array(p[indexU]) # U en espacio de operaciones
                        uNodes=np.array(pNodes[indexU]) # nodos de U

                        qleft=np.array(q) # Q disponibles internodal
                        qNodesleft=np.array(qNodes) #nodos de Q disponibles internodal
                        RperQleft=np.array(RperQ) # R disponibles internodal
                        if not qDoneU.shape[0]==0:
                            qleft=np.delete(qleft,qDoneU,0) #eliminación de q alcanzados por P en asignaciones intranodales
                            qNodesleft=np.delete(qNodesleft,qDoneU,0)
                            RperQleft=np.delete(RperQleft,qDoneU,0) 
                        Amatrix= np.zeros((qleft.shape[0],u.shape[0])) #inicialización de matriz de pesos

                        #Matriz de distancias U a Q
                        xdeltauq= qleft[:,0].reshape(qleft.shape[0],1)-u[:,0].reshape(1,u.shape[0])
                        ydeltauq= qleft[:,1].reshape(qleft.shape[0],1)-u[:,1].reshape(1,u.shape[0])
                        distanceuq= np.sqrt(np.add(np.square(xdeltauq),np.square(ydeltauq)))

                        #Matriz de distancias Q a R asignado
                        xdeltaqRperQ= np.zeros((u.shape[0],1))-(qleft[:,0].reshape(1,qleft.shape[0])-RperQleft[:,0].reshape(1,qleft.shape[0]))
                        ydeltaqRperQ= np.zeros((u.shape[0],1))-(qleft[:,1].reshape(1,qleft.shape[0])-RperQleft[:,1].reshape(1,qleft.shape[0]))
                        distanceqRperQ= np.sqrt(np.add(np.square(xdeltaqRperQ),np.square(ydeltaqRperQ))).T

                        #Matriz de diferencia de nodos (U_i no se asigna a su N_i)
                        nodeQnodeU=qNodesleft[:].reshape(qNodesleft.shape[0],1)-uNodes[:].reshape(1,uNodes.shape[0])
                        nodeQnodeU=((nodeQnodeU.astype(int)==0)-1)*(-1)
                        Amatrix=1000*distanceuq*PtOptimum/vOptimum +1000*distanceqRperQ*PtOptimum/vOptimum #matriz de pesos

                        wU=w[indexU]
                        asignE=Amatrix<wU #inicialización de la matriz con arcos que pueden ser recorridos
                        asignE=np.multiply(asignE,nodeQnodeU)
                        #asignE=asignE*(np.zeros((Amatrix.shape))+wMin<wU)
                        asignUtoR=np.dot(np.ones((1,asignE.shape[0])),asignE)==0
                        asignUtoR=asignUtoR.reshape(asignUtoR.shape[1],1)
                        pReturning[indexU[np.where(asignUtoR==True)[0]]]=1

                        asigned=np.zeros((qleft.shape[0],u.shape[0])) #matriz con p asignados
                        Amatrix= Amatrix- 1000*distanceqRperQ*PtOptimum/vOptimum #Actualizacion a pesos por recorrido individual
                        
                        #eliminacion de arcos no eficientes
                        for row in range(Amatrix.shape[0]):
                            infArc=100*capJoules #arco con valor infinito (no será considerado para calcular arcos mínimos) 
                            if row==Amatrix.shape[1]:
                                break
                            #arcos restantes (sin u asignados, sus arcos y arcos de q respectivos)
                            remainingArcs=Amatrix+(asignE-1)*(-1)*infArc+asigned*infArc
                            #print("remainingArcs: ",remainingArcs)
                            currMin=np.min(remainingArcs) #arco mínimo global por q para todo u
                            if currMin>=infArc:
                                break
                            #print("arcos minimos", currMin)
                            deleteNonMax=remainingArcs==currMin #matriz booleana actual para eliminar arcos desde q y desde u
                            [rowIndex,colIndex]=np.where(remainingArcs==currMin) #indice de u seleccionado
                            rowIndex=np.array(rowIndex)[0]
                            colIndex=np.array(colIndex)[0]

                            asignE[rowIndex,:]=asignE[rowIndex,:]*False #eliminado de arcos no mínimos desde q
                            asignE[:,colIndex]=asignE[:,colIndex]*False #eliminado de arcos no mínimos desde p
                            asigned[rowIndex,colIndex]=True
                        
                        uLlegada=distanceuq<=dt #matriz con booleanos para llegada
                        #deltax y deltay matricial segun distancia restante
                        deltax=np.nan_to_num((uLlegada-1)*(-1)*(xdeltauq/distanceuq)*asigned*dt +uLlegada*(xdeltauq)*asigned)
                        deltay=np.nan_to_num((uLlegada-1)*(-1)*(ydeltauq/distanceuq)*asigned*dt +uLlegada*(ydeltauq)*asigned)
                        #Movimiento segun asignacion (movimiento unitario o movimiento de llegada)
                        if simGRID:
                            for celda in range(1,div**2+1):
                                asignadosBlw=0 #Conteo de UAV's asignados a celdas inferiores
                                asignadosRght=0 #Conteo de UAV's asignados a celdas superiores
                                uInCeldaIndex=np.where(uNodes==celda)[0]
                                if uInCeldaIndex.shape[0]==0:
                                    continue
                                uInCelda=u[uInCeldaIndex] # U en celda para GRID internodal
                                [currentLine,currentColumn]=np.where(C==celda)

                                for asignando in range(uInCelda.shape[0]):
                                    if pReturning[indexU[uInCeldaIndex[asignando]]]==1 or pReturned[indexU[uInCeldaIndex[asignando]]]==1:
                                        continue
                                    vunit=np.array([0,0]) #quieto
                                    if deltaMatrix[(div-currentLine-1)*2,currentColumn]-asignadosBlw>0 and not(currentLine==div-1): #delta blw
                                        vunit=np.array([0,-1]) #abajo
                                        asignadosBlw=asignadosBlw+1
                                    elif not (currentLine == 0):
                                        vunit=np.array([0,1]) #arriba
                                    elif (currentLine==0):
                                        if(deltaRow[0,currentColumn]-asignadosRght>0) and not currentColumn==div-1: #delta rght
                                            vunit=np.array([1,0]) #derecha
                                            asignadosRght=asignadosRght+1
                                        elif not(currentColumn==0):
                                            vunit=np.array([-1,0]) #izquierda

                                    dx=vunit*dt
                                    uInCelda[asignando,:]+=dx
                                    w[indexU[uInCeldaIndex[asignando]]]-= np.sum(np.abs(dx))*1000*PtOptimum/vOptimum
                                u[uInCeldaIndex]=uInCelda
                                #input("confirme: ")
                        else:
                            xmove=np.dot(np.ones(asignE.shape[0]),deltax)
                            ymove=np.dot(np.ones(asignE.shape[0]),deltay)
                            u=u +np.c_[xmove,ymove]
                        
                        if(not (np.all(deltax<=dt) and np.all(deltay<=dt))) or (not (np.all(xmove<=dt) and np.all(ymove<=dt))):
                            print("/////////////////////////////////////////////////////////////")
                            print("////////////////////////--ALERTA EN U--//////////////////////")
                            print("/////////////////////////////////////////////////////////////")
                            print(not (np.all(deltax<=dt) and np.all(deltay<=dt)))
                            print(not (np.all(xmove<=dt) and np.all(ymove<=dt)))
                            print("deltax: ", deltax,"deltay: ", deltay)
                            time.sleep(10) #alerta al usuario que el algoritmo está fallando
                        #Actualizacion en P global
                        p[indexU]=np.array(u)
                        if not simGRID:
                            w[indexU]=w[indexU]- 1000*np.sqrt(np.add(np.square(xmove),np.square(ymove)))*PtOptimum/vOptimum

                    ######################################################################################################
                    ##                      Retorno de U a R
                    ######################################################################################################
                    if not np.sum(pReturning)-np.sum(pReturned)==0 and not pureGRID:
                        print("/////////////////////////--REGRESOUAR--//////////////////////")
                        indexU=np.where(pReturning==1)[0]
                        returnU=np.array(p[indexU])
                        
                        #Matriz de distancias U_i a R
                        xdeltaur= r[:,0].reshape(r.shape[0],1)-returnU[:,0].reshape(1,returnU.shape[0])
                        ydeltaur= r[:,1].reshape(r.shape[0],1)-returnU[:,1].reshape(1,returnU.shape[0])
                        distanceur= np.sqrt(np.add(np.square(xdeltaur),np.square(ydeltaur)))

                        finalReturn=True
                        UinR=True
                        for rC in range(returnU.shape[0]): #Possible return Column
                            rR= np.array(np.where(distanceur[:,rC]==np.min(distanceur[:,rC]))[0])[0] #return Row (distancia a r más cercano)
                            uLlegadaR=distanceur<=dt #matriz con booleanos para llegada
                            
                            #deltax y deltay individual segun distancia restante
                            urdeltax=(uLlegadaR[rR,rC]-1)*(-1)*(np.nan_to_num(xdeltaur[rR,rC]/distanceur[rR,rC]))*dt +uLlegadaR[rR,rC]*(xdeltaur[rR,rC])
                            urdeltay=(uLlegadaR[rR,rC]-1)*(-1)*(np.nan_to_num(ydeltaur[rR,rC]/distanceur[rR,rC]))*dt +uLlegadaR[rR,rC]*(ydeltaur[rR,rC])
                            p[indexU[rC]]=p[indexU[rC]]+np.c_[urdeltax,urdeltay]
                            w[indexU[rC]]=w[indexU[rC]]- 1000*np.sqrt(np.square(urdeltax)+np.square(urdeltay))*PtOptimum/vOptimum
                            if distanceur[rR,rC]<=dt/2:
                                pReturned[indexU[rC]]=1
                                UinR=UinR and True
                            else:
                                UinR=UinR and False
                    
                    ######################################################################################################
                    ##                      Estado de ejecución, video y salto a siguiente iteración
                    ######################################################################################################
                    if video:
                        TesisFcns.initialScatter(q,r,p,pZero,div,radOper,C,autom,video,allQMet) #ploteo de delta
                        #Transformar figura a imagen (no pude implementar FuncAnimation)
                        img= np.frombuffer(plt.gcf().canvas.tostring_rgb(), dtype=np.uint8)
                        img= img.reshape(plt.gcf().canvas.get_width_height()[::-1] + (3,))
                        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR) #imagen lista para ser agregada a video
                        theVideo.write(img)

                    if (not np.sum(pReturned) ==0) and np.sum(pReturned)+qDone.shape[0]==p.shape[0]:
                        print("salto llegada y retorno para actualizar Q")
                        break    

                    if (nodesMet and indexU.shape[0]==0) and video: #todo q fue alcanzado para los p disponibles y no hay u
                        #Transformar figura a imagen (no pude implementar FuncAnimation)
                        img= np.frombuffer(plt.gcf().canvas.tostring_rgb(), dtype=np.uint8)
                        img= img.reshape(plt.gcf().canvas.get_width_height()[::-1] + (3,))
                        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR) #imagen lista para ser agregada a video
                        theVideo.write(img)
                        theVideo.write(img)
                        theVideo.write(img)
                        if q.shape[0]>p.shape[0]:
                            break
                    print("")
                    if qDone.shape[0]==p.shape[0]:
                        break
                    if pureGRID and q.shape[0]==0:
                        break

                if not qDone.shape[0]==0:
                    wIter[iter]=(np.sum(wPrev)-np.sum(w))/qDone.shape[0] #Registro de consumo promedio por UAV para iteración actual
                    if allQMet.shape[0]==0:
                        allQMet=np.array(q[qDone])
                    else:
                        allQMet= np.concatenate((allQMet,q[qDone])) #guardado de q alcanzados
                    q=np.delete(q,qDone,0) #eliminación de q alcanzados
                    qNodes=np.delete(qNodes,qDone,0) #eliminación asociada a q
                    RperQ=np.delete(RperQ,qDone,0) #eliminación de R asignados respectivos
                    print("Q actualizado")
                
                wIterTotal[iter]=(np.sum(winit)-np.sum(w))/allQMet.shape[0] #Registro de consumo total por UAV para iteración actual
                allQMetIter[iter]=allQMet.shape[0] #Registro acumulativo de objetivos alcanzados

                if np.sum(pReturned)==p.shape[0]:
                    img= np.frombuffer(plt.gcf().canvas.tostring_rgb(), dtype=np.uint8)
                    img= img.reshape(plt.gcf().canvas.get_width_height()[::-1] + (3,))
                    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR) #imagen lista para ser agregada a video
                    print("Todo P ha regresado")
                    if video:
                        theVideo.write(img)
                        theVideo.write(img)
                        theVideo.write(img)
                    break
                if pureGRID and q.shape[0]==0:
                    break

            w_Sim[:,simActual]=wIter/3600 #Conversión de Joules a Wh
            w_SimTotal[:,simActual]=wIterTotal/3600 #Conversión a Wh
            q_Sim[:,simActual]=allQMetIter
        w_Div[:,divIniciales-1]=np.mean(w_Sim,axis=1)
        print(w_SimTotal.shape)
        w_DivTotal[:,divIniciales-1]=np.mean(w_SimTotal,axis=1)
        print(q_Sim.shape)
        q_Div[:,divIniciales-1]=np.mean(q_Sim,axis=1)
        w_DivStandar[:,divIniciales-1]=np.std(w_Sim,axis=1)
        w_DivTotalStandar[:,divIniciales-1]=np.std(w_SimTotal,axis=1)
        q_DivStandar[:,divIniciales-1]=np.std(q_Sim,axis=1)

#print("initial energy",winit)
#print("remaining energy",w)
#print("returned:",pReturned, "Bool statement:",np.sum(pReturned)==p.shape[0], "returning:",pReturning)
#print("qShape:", q.shape[0])
dataForJson={} #Data a ser guardada en formato json
dataForJson["dataP"]=w_Div.tolist()
dataForJson["dataPTotal"]=w_DivTotal.tolist()
dataForJson["desvP"]=w_DivStandar.tolist()
dataForJson["desvPTotal"]=w_DivTotalStandar.tolist()
dataForJson["qData"]=q_Div.tolist()
dataForJson["qDesv"]=q_DivStandar.tolist()
dataForJson["info"]="Resultado promedio con desviación estándar para simulaciones de múltiples particiones de AO."
dataForJson["nQ"]=str(nQ)
dataForJson["qPerUAV"]=str(qPerUAV)
fileToWrite= open("dataStored.json","w",encoding="utf-8")
json.dump(dataForJson,fileToWrite,ensure_ascii=False)

print("q:")
print(q.shape)
print("allQMet:")
print(allQMet.shape)
print("w:")
print(w)
print("C:")
print(C)

music = pyglet.resource.media('sound.mp3')
music.play()
time.sleep(8)
print("///////////////////////////----FINISHED----/////////////////////////////")