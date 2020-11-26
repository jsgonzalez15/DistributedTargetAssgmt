"""
Métodos para propuesta de modelo distribuido para Flota de UAV's.

Funciones:
* initialScatter gráfica inicial, organización de información y relacion visual de información.

@author: Juan Sebastián González Rojas 201612109
@email: js.gonzalez15@uniandes.edu.co
"""
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import math

def initialScatter (q,r,p,pZero,div,radOper,C,autom,video):
    # Generacion visual de GRID utilizando meshgrid
    gridNodes=np.array(range(0,int(round(radOper/1000))+1,int(round(radOper/(1000*div)))))
    
    ''' CONVERTIR PLOT DE DIVISIONES EN UNA FUNCION'''
    ##--------------------------------------PLOTEO PARA CUADRÍCULAS----------------------------------------##
    [Xb,Yb]=np.meshgrid(gridNodes,gridNodes) 
    plt.cla() #Se borra información anterior al ploteo actual
    plt.plot(Xb,Yb,'k--',linewidth=1)
    plt.plot(Yb,Xb,'k--',linewidth=1)
    ##------------------------------------------------------------------------------------------------------##

    for j in range(p.shape[0]):
        plt.plot([pZero[0,0],p[0,0]],[pZero[0,1],p[0,1]],'b--',linewidth=0.5)
    
    plt.scatter(q[:,0],q[:,1],marker='o',c='None', edgecolor='red',linewidth=0.7,label='Objetivos')
    plt.scatter(p[:,0],p[:,1], marker='x',color='b',linewidth=0.7,label='UAVs')
    plt.scatter(r[:,0],r[:,1], c='None', marker='h',edgecolor='g',linewidth=0.7,label='Recolectores')

    plt.plot([pZero[0,0],p[0,0]],[pZero[0,1],p[0,1]],'b--',linewidth=0.5)
    plt.xlabel('x (km)')
    plt.ylabel('y (km)')
    ''' CONDICIONAR TITLE SEGUN PARTICION'''
    plt.title('Evolución de envios distribuidos')
    plt.legend()
    plt.gcf().canvas.draw()
    #plt.show()
    #if not video:
        #print("InitialScatter says: not Showing for now")
        #plt.show()

def pqrInNode(theNode:int,p:list,q:list,r:list,C:list,radOper:int,div:int,divMethod:str)->list:
    #Retorna posiciones de UAVs, UAVs no Asignados, Objetivos y Recolector asignados al nodo recibido
    #Retorna los indices en matrices p y q para posterior actualizacion
    
    pInNode=[] #Matriz con ubicaciones de UAVs en nodo
    pInNodeUnassigned=[] #Matriz con ubicaiones de UAVs en nodo (IMPLEMENTAR)
    qInNode=[] #Matriz con ubicaciones de objetivos en nodo
    indexP=[] #Vector con indices de UAVs encontrados en matriz p
    indexQ=[] #Vector con indices de Objetivos encontrados en matriz q
    theCenter=np.array([0,0]) #Punto central del nodo

    for j in range(len(p)): #filas equivalentes a # de UAVs
        [yourNode,center]=currentNode(p[j,:],C,radOper,div,divMethod)
        if yourNode==theNode:
            pInNode.append(p[j,:])
            indexP.append(j)
            theCenter=np.array(center)
    for k in range(len(q)): #filas equivalentes a # de Objetivos
        if currentNode(q[k,:],C,radOper,div,divMethod)[0]==theNode:
            qInNode.append(q[k,:])
            indexQ.append(k)
    #print("Centro actual ", theCenter)
    centerToR=np.array(r)-theCenter
    #print("Distancia del centro a los r ",centerToR)
    minDistances=np.sqrt(np.sum(np.multiply(centerToR,centerToR))) #obtiene la distancia al recolector más cercano
    rNode=r[np.where(np.min(minDistances)==minDistances)[0]] #obtiene el nodo asociado a esta distancia mínima
    #print("Distancia minima actual ", np.min(minDistances))
    #print("Nodo recolector seleccionado ", rNode)

    return [np.array(pInNode), indexP, np.array(qInNode), indexQ, np.array(rNode)]

def currentNode(p:list,C:list,radOper:int,div:int, divMethod:str)->list:
    #Retorna el numero del nodo y las coordenadas de su centro para el p recibido

    if divMethod=="GRID": #Particion de nodo en cuadriculas
        currentColumn=math.ceil((p[0]/(radOper/1000))*div)-1 #columna actual
        currentLine=div-math.ceil((p[1]/(radOper/1000))*div) #fila actual
        #centro de nodo en división del método GRID
        center=[((currentColumn+0.5)*radOper/1000)/div,((currentLine+0.5)*radOper/1000)/div]

        #condicionales para casos excepcionales
        if currentColumn<0:
            currentColumn=0
        if currentLine<0:
            currentLine=0
        if currentLine>=div:
            currentLine=div-1
        if currentColumn>=div:
            currentColumn=div-1
        yourNode=C[currentLine][currentColumn] #celda actual
        return [yourNode,center]