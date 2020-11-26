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
#####################################################################################################################
##                               Simulación de Método Distribuido: Min Costo UAV/Destino
#####################################################################################################################

np.seterr(divide='ignore', invalid='ignore')
#calculo de radio de Operaciones, consumo y vel óptimos
[radOper,PtOptimum,vOptimum,capJoules]=GRIDFcns.CalcularParametrosEnergeticos()

''' Parámetros generales de simulación'''
[densidadMin,densidadMax]=[6,6] #Rango de densidades a simular
qPerUAV=6 #Proporción de objetivos por UAV
w_Densidad=[] #valores medios y desviación estándar por densidad de consumo
w_Iteracion=[] #valores medios y desviación estándar en consumo por iteración
desv_w_p=0 #max desv de consumo entre UAVs (ideal 0)
divIniciales=3 #divisiones iniciales
simulacionesPorDensidad=100 #n sim por densidad
divMethod="GRID" #tipo de particion del espacio
dt=0.3

video=0 #obtener un video de simulación (1) ejecutar sin video (0)
autom=1 #autom sim(1)/ver todo(0)
changeDiv=0 #cambiar div durante sim(1)/ mantener div(0)
video=True

''' ############################  Inicialización escenario, UAVs, Puntos Recolección y objetivos  ############################ '''
nQ=90 #Numero de Objetivos
nP=round(nQ/qPerUAV) #Numero de UAVs segun densidad deseada
nR=5 #Numero de Puntos Recolección/despliegue

r=np.random.rand(nR,2)*radOper/1000 #(x,y) posiciones [km] de recolectores en AreaOperaciones
q=np.random.rand(nQ,2)*radOper/1000 #(x,y) posiciones [km] de objetivos en AreaOperaciones 
qNodes=np.ones(nQ)*(-1) #(z) nodos en los que se encuentran q
w=np.ones(nP)*capJoules #Registro de consumo por UAV (Energía restante)

p= np.random.rand(nP,2)*radOper/1000   #inicializacion de matriz de UAVs
for pItem in range(nP): #Ubicaciones iniciales en Recolectores aleatorios 
    p[pItem]=r[int(round(np.random.rand()*nR-0.5))] + (np.random.rand(1,2)-0.5)
pNodes=np.ones(nP)*(-1) #nodos en los que se encuentra p
pZero=p

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
TesisFcns.initialScatter(q,r,p,pZero,div,radOper,C,autom,video) #ploteo inicial
####################################################################################################

if video:
    fourcc=cv2.VideoWriter_fourcc(*'MP4V')
    theVideo=cv2.VideoWriter('TesisSimVideo.mp4',fourcc,10,(640,480))

allQMet=np.array([[-1,-1]]) #Objetivos que han sido alcanzados (inicializado con valor dummie)

'''##################################################################################################################
##                                      EJECUCIÓN PRINCIPAL DEL ALGORITMO
#####################################################################################################################'''
for iter in range(6): #Sim hasta:(a) todo P ha llegado, o, (b) Q agotados

    for deltaT in range(130):
        print("///////////////////////////////////////// Iteración simulada: ", iter," /// Delta T simulado: ", deltaT)
        qDone=np.array([]) #lista de indices de objetivos alcanzados para eliminación en ciclo final
        qDoneU=np.array([]) #lista de indices alcanzados para eliminación parcial (ciclo Internodal)
        nodesMet=True #booleano que indica si los objetivos fueron alcanzados en todos los nodos
        indexU=np.array([]) #arreglo de indices de P unassigned

        ######################################################################################################
        ##                      Asignación y Movimiento Intranodal
        ######################################################################################################
        for nodoActual in range(1,div**2+1): #recorrido sobre todos los nodos 
            [pInNode, indexP, qInNode, indexQ, rNode]= TesisFcns.pqrInNode(nodoActual,p,q,r,C,radOper,div,divMethod)
            if not np.array(indexQ).shape[0]==0:
                qNodes[np.array(indexQ).astype(int)]=nodoActual #nodos de Q
            if not np.array(indexP).shape[0]==0:
                pNodes[np.array(indexP).astype(int)]=nodoActual #nodos de Q
            indexUinNode=np.array([]) #indices de U dentro del nodo
            
            print("Nodo: ",nodoActual,", pInNode: ", pInNode.shape, ", qInNode: ", qInNode.shape)
            if not pInNode.shape[0]==0 and qInNode.shape[0]==0: #solo hay U (no hay Q) en Nodo actual
                indexUinNode=np.array(indexP)

            if not pInNode.shape[0]==0 and not qInNode.shape[0]==0:
                Amatrix= np.zeros((qInNode.shape[0],pInNode.shape[0])) #inicialización de matriz de pesos

                #Matriz de distancias P_i a Q_i
                xdeltapq= qInNode[:,0].reshape(qInNode.shape[0],1)-pInNode[:,0].reshape(1,pInNode.shape[0])
                ydeltapq= qInNode[:,1].reshape(qInNode.shape[0],1)-pInNode[:,1].reshape(1,pInNode.shape[0])
                distancepq= np.sqrt(np.add(np.square(xdeltapq),np.square(ydeltapq)))

                #Matriz de distancias Q_i a R_i
                xdeltaqr= np.ones((pInNode.shape[0],1))*rNode[0,0] -qInNode[:,0].reshape(1,qInNode.shape[0])
                ydeltaqr= np.ones((pInNode.shape[0],1))*rNode[0,1] -qInNode[:,1].reshape(1,qInNode.shape[0])
                distanceqr= np.sqrt(np.add(np.square(xdeltaqr),np.square(ydeltaqr))).T

                Amatrix=distancepq*PtOptimum/vOptimum +distanceqr*PtOptimum/vOptimum #matriz de pesos
                wNode=w[indexP]
                asignE=Amatrix<wNode #inicialización de la matriz con arcos que pueden ser recorridos
                asigned=np.zeros((qInNode.shape[0],pInNode.shape[0])) #matriz con p asignados
                Amatrix= Amatrix- distanceqr*PtOptimum/vOptimum #Actualizacion a pesos por recorrido individual
                #print("Amatrix: ", Amatrix)
                #print("asignE inicial: ", asignE)
                
                #eliminacion de arcos no eficientes
                for row in range(Amatrix.shape[0]):
                    infArc=100000.0 #arco con valor infinito (no será considerado para calcular arcos minimos) 
                    if row==Amatrix.shape[1]:
                        break
                    #arcos restantes (sin p asignados, sus arcos y arcos de q respectivos)
                    remainingArcs=Amatrix+(asignE-1)*(-1)*infArc+asigned*infArc
                    #print("remainingArcs: ",remainingArcs)
                    currMin=np.min(remainingArcs) #arco mínimo global por q para todo p

                    #print("arcos minimos", currMin)
                    deleteNonMax=remainingArcs==currMin #matriz booleana actual para eliminar arcos desde q y desde p
                    [rowIndex,colIndex]=np.where(remainingArcs==currMin) #indice de p seleccionado

                    asignE[rowIndex,:]=asignE[rowIndex,:]*deleteNonMax[rowIndex,:] #eliminado de arcos no mínimos desde q
                    asignE[:,colIndex]=asignE[:,colIndex]*deleteNonMax[:,colIndex] #eliminado de arcos no mínimos desde p
                    asigned[rowIndex,colIndex]=True
                    #print("asignE actual: ",asignE)

                pLlegada=distancepq<=dt #matriz con booleanos para llegada
                #deltax y deltay matricial segun distancia restante
                deltax=(pLlegada-1)*(-1)*(np.nan_to_num(xdeltapq/distancepq))*asignE*dt +pLlegada*(xdeltapq)*asignE
                deltay=(pLlegada-1)*(-1)*(np.nan_to_num(ydeltapq/distancepq))*asignE*dt +pLlegada*(ydeltapq)*asignE
                
                #Movimiento segun asignacion (movimiento unitario o movimiento de llegada)
                xmove=np.dot(np.ones(asignE.shape[0]),deltax)
                ymove=np.dot(np.ones(asignE.shape[0]),deltay)
                p[indexP]=pInNode +np.c_[xmove,ymove]

                #Identificacion de objetivos recorridos en celda actual
                inNodeQdone=np.where(distancepq<=0.01)[0]
                if inNodeQdone.shape[0]>=qInNode.shape[0] or inNodeQdone.shape[0]>=pInNode.shape[0]:
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
                currU= (np.dot(np.ones(asignE.shape[0]),asignE).astype(int)-1)*(-1) #vector bool con U en Nodo actual
                indexUinNode=np.where(currU==True)[0]
                indexUinNode=np.array(indexP)[indexUinNode]
                
            indexU=np.concatenate((indexU,np.array(indexUinNode)))
        print("Size de no asignados acumulado: ", indexU.shape)
        
        ######################################################################################################
        ##                      Asignación y Movimiento Internodal
        ######################################################################################################
        if not indexU.shape[0]==0:
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
            Amatrix=distanceuq*PtOptimum/vOptimum +distanceqRperQ*PtOptimum/vOptimum #matriz de pesos

            wU=w[indexU]
            asignE=Amatrix<wU #inicialización de la matriz con arcos que pueden ser recorridos
            asignE=np.multiply(asignE,nodeQnodeU)

            asigned=np.zeros((qleft.shape[0],u.shape[0])) #matriz con p asignados
            Amatrix= Amatrix- distanceqRperQ*PtOptimum/vOptimum #Actualizacion a pesos por recorrido individual
            
            #eliminacion de arcos no eficientes
            for row in range(Amatrix.shape[0]):
                infArc=100000.0 #arco con valor infinito (no será considerado para calcular arcos minimos) 
                if row==Amatrix.shape[1]:
                    break
                #arcos restantes (sin u asignados, sus arcos y arcos de q respectivos)
                remainingArcs=Amatrix+(asignE-1)*(-1)*infArc+asigned*infArc
                #print("remainingArcs: ",remainingArcs)
                currMin=np.min(remainingArcs) #arco mínimo global por q para todo u

                #print("arcos minimos", currMin)
                deleteNonMax=remainingArcs==currMin #matriz booleana actual para eliminar arcos desde q y desde u
                [rowIndex,colIndex]=np.where(remainingArcs==currMin) #indice de u seleccionado

                asignE[rowIndex,:]=asignE[rowIndex,:]*deleteNonMax[rowIndex,:] #eliminado de arcos no mínimos desde q
                asignE[:,colIndex]=asignE[:,colIndex]*deleteNonMax[:,colIndex] #eliminado de arcos no mínimos desde p
                asigned[rowIndex,colIndex]=True
            
            uLlegada=distanceuq<=dt #matriz con booleanos para llegada
            #deltax y deltay matricial segun distancia restante
            deltax=np.nan_to_num((uLlegada-1)*(-1)*(xdeltauq/distanceuq)*asignE*dt +uLlegada*(xdeltauq)*asignE)
            deltay=np.nan_to_num((uLlegada-1)*(-1)*(ydeltauq/distanceuq)*asignE*dt +uLlegada*(ydeltauq)*asignE)
            #Movimiento segun asignacion (movimiento unitario o movimiento de llegada)
            xmove=np.dot(np.ones(asignE.shape[0]),deltax)
            ymove=np.dot(np.ones(asignE.shape[0]),deltay)
            u=u +np.c_[xmove,ymove]
            
            #Actualizacion en P global
            p[indexU]=np.array(u)
            
        if video:
            TesisFcns.initialScatter(q,r,p,pZero,div,radOper,C,autom,video) #ploteo de delta
            #Transformar figura a imagen (no pude implementar FuncAnimation)
            img= np.frombuffer(plt.gcf().canvas.tostring_rgb(), dtype=np.uint8)
            img= img.reshape(plt.gcf().canvas.get_width_height()[::-1] + (3,))
            img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR) #imagen lista para ser agregada a video
            theVideo.write(img)
            
        if nodesMet and indexU.shape[0]==0: #todo q fue alcanzado para los p disponibles y no hay u
            #Transformar figura a imagen (no pude implementar FuncAnimation)
            img= np.frombuffer(plt.gcf().canvas.tostring_rgb(), dtype=np.uint8)
            img= img.reshape(plt.gcf().canvas.get_width_height()[::-1] + (3,))
            img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR) #imagen lista para ser agregada a video
            theVideo.write(img)
            theVideo.write(img)
            theVideo.write(img)
            break
        print("")
    print("deltax:",deltax,"deltay:",deltay)
    if not qDone.shape[0]==0:
        allQMet= np.concatenate((allQMet,q[qDone])) #guardado de q alcanzados
        q=np.delete(q,qDone,0) #eliminación de q alcanzados
        qNodes=np.delete(qNodes,qDone,0) #eliminación asociada a q
        RperQ=np.delete(RperQ,qDone,0) #eliminación de R asignados respectivos
    if q.shape[0]==0:
        break

print("///////////////////////////----FINISHED----/////////////////////////////")
