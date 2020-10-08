"""
Métodos para réplica de GRID Target Assgmt.

Funciones:
* CurrentCell funcion para obtener id de celda actual.
* UAVandTargetInCell funcion que retorna UAVs y targets en la celda actual.
* initialScatter gráfica inicial, organización de información y relacion visual de información.
* anima función para animar escenario y movimiento de UAVs.
* CalcularParametrosEnergeticos calcula el radio de operación de despliegue, el consumo y la velocidad optimos según parámetros del UAV.

@author: Juan Sebastián González Rojas 201612109
@email: js.gonzalez15@uniandes.edu.co
"""
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import math
from scipy import constants

def CurrentCell(p:list,C:list,radOper:int,div:int)->int:
    #Retorna la celda actual del UAV
    currentColumn=math.ceil((p[0]/(radOper/1000))*div) #columna actual
    currentLine=div-math.ceil((p[1]/(radOper/1000))*div) #fila actual
    print("CurrentCell says:" +str(currentLine)+str(currentColumn))
    yourCell=C[currentLine][currentColumn] #celda actual
    return yourCell

def uavAndTargetInCell(cellOfIter,initialUAVs,places,C,radOper,div)->list:
    #Retorna posiciones de UAVs y Objetivos dentro de la celda especificada
    #Retorna la cantidad de UAVs dentro de la celda
    #Retorna los indices en initialUAVs para posterior actualizacion
    
    CurrentCellInfo=[] #Matriz con ubicaciones (UAVs primero Targets despues)
    indicesUAVinCell=[] #Vector con indices de UAVs encontrados en initialUAVs
    indicesTargetInCell=[] #Vector con indices de Targets encontrados en places
    for j in range(len(initialUAVs)): #filas equivalentes a # de UAVs
        if CurrentCell(initialUAVs[j,:],C,radOper,div)==cellOfIter:
            CurrentCellInfo.append(initialUAVs[j,:])
            indicesUAVinCell.append(j)
    nUAVsInCell=(np.array(CurrentCellInfo)).shape[0]
    for k in range(len(places)):
        if CurrentCell(places[k,:],C,radOper,div)==cellOfIter:
            CurrentCellInfo.append(places[k,:])
            indicesTargetInCell.append(k)
    return [CurrentCellInfo,nUAVsInCell,indicesUAVinCell,indicesTargetInCell]

def initialScatter (places,initialUAVs,div,radOper,C,autom,video):
    # Generacion visual de GRID utilizando meshgrid
    print(int(round(radOper/1000)))
    gridNodes=np.array(range(0,int(round(radOper/1000))+1,int(round(radOper/(1000*div)))))
    
    [Xb,Yb]=np.meshgrid(gridNodes,gridNodes) 
    plt.cla() #Se borra información anterior al ploteo actual
    plt.scatter(places[:,0],places[:,1],marker='o',c='None', edgecolor='red',lineWidth=0.7,label='Objetivos')
    plt.scatter(initialUAVs[:,0],initialUAVs[:,1], marker='x',color='b',lineWidth=0.7,label='UAVs')
    plt.plot(Xb,Yb,'k--',lineWidth=1)
    plt.plot(Yb,Xb,'k--',lineWidth=1)
    plt.xlabel('x (km)')
    plt.ylabel('y (km)')
    plt.title('Evolución de envios distribuidos')
    plt.legend(frameon=False,bbox_to_anchor=(1.001, 1), loc='upper left')
    plt.show()

def anima():
	objeto=animation.FuncAnimation(plt.figure(1),initialScatter,10000) #plt.gcf get currently figure Animar las figuras por parámetro de manera iterativa
	plt.show()

def CalcularParametrosEnergeticos()->list:
    w=21 #Peso [kg] 
    b=0.860 #Ancho frontal [m]
    A=0.530*0.480 #Area frontal [m**2]#
    varSigma=0.430*0.480 #Area superior [m**2]

    g=constants.value('standard acceleration of gravity')#[m/(s**2)]
    T=w*g #Empuje (Peso) [N]
    v=18 #Velocidad (UAV-aire) [m/s]
    Cd=0.45 # Coeficiente aerodinamico de arrastre
 
    Temperature=[8,32] #Temperatura [°C]
    Humidity=[0.65,0.95] #Densidad de H2O
    Pressure=[600,1200] #Presion [hPa] (Valores esperados)
    
    #Densidad del aire minima y maxima esperada en kg/m**3
    Dmin=(0.34848*Pressure[0]-0.009*Humidity[1]*np.exp(0.061*Temperature[1]))/(273.15+Temperature[1])
    Dmax=(0.34848*Pressure[1]-0.009*Humidity[0]*np.exp(0.061*Temperature[0]))/(273.15+Temperature[0])
    
    #Consumo estatico min y max
    [pmin,pmax]=[(T**1.5)/((2*Dmax*varSigma)**0.5),(T**1.5)/((2*Dmin*varSigma)**0.5)]
    p=pmax
    #Consumo velocidad maxima min y max
    [Ptmin,Ptmax]=[0.5*Cd*A*Dmin*(v**3)+(w**2)/(Dmin*v*b**2),0.5*Cd*A*Dmax*(v**3)+(w**2)/(Dmax*v*b**2)]
    Pt=Ptmax #consumo velocidad maxima
    #Velocidad con menor consumo min y max
    [vOptimum,vOptimum2]=[((2*w**2)/(Cd*A*(b*Dmax)**2))**0.25,((2*w**2)/(Cd*A*(b*Dmin)**2))**0.25]
    #Consumo optimo
    [PtOptimum,PtOptimum2]=[0.5*Cd*A*Dmax*(vOptimum**3)+(w**2)/(Dmax*vOptimum*b**2),0.5*Cd*A*Dmin*(vOptimum2**3)+(w**2)/(Dmin*vOptimum2*b**2)]
    
    capBattery=266 #Cap. bateria [Wh]
    timeHovering=11*60 #duracion vuelo estatico (21kg)
    capJoules=capBattery*3600 #cap. estimada [J]
    pHovering=capJoules/timeHovering #consumo en W de vuelo estatico con 21kg
 
    maxDistance=(capJoules/Pt)*v # Distancia velocidad maxima
    maxDistanceOpt=(capJoules/PtOptimum)*vOptimum# Distancia velocidad optima 1
    maxDistanceOpt2=(capJoules/PtOptimum2)*vOptimum2# Distancia velocidad optima 2
    # Radio de operaciones en m para densidades
    radOper=maxDistanceOpt*0.95/2
    radOper2=maxDistanceOpt2*0.95/2#
    return [radOper,PtOptimum,vOptimum]