"""
Réplica método distribuido GRID target Assignment y extensión a asignación de tareas no monotónicas.

Temas:
* Consumo energético.
* Eficiencia de método iterativo.
* Incidencia en concentración de agentes y división iterativa.
* Efectos de puntos de inicio en el mapa.

@author: Juan Sebastián González Rojas 201612109
"""
import functionsGRIDassgmt as myFcns
from matplotlib import pyplot
import numpy as np
######################################################################################################
##                          Simulación Metodos Distribuidos: GRID Assignment
######################################################################################################
 
#calculo de radio de Operaciones, consumo y vel óptimos
[radOper,PtOptimum,vOptimum]=myFcns.CalcularParametrosEnergeticos()

[densidadMin,densidadMax]=[6,6]
video=0 #obtener un video de simulación (1) ejecutar sin video (0)
dt=0.3
consumoDensidad=[] #valores medios y desviacion estandar por densidad
consumoIteracion=[] #valores medios y desviacion estandar en consumo por iteracion
desviacionConsumoUAVs=0 #max desv de consumo entre UAVs (ideal 0)
divIniciales=3 #divisiones iniciales

autom=1 #autom sim(1)/ver todo(0)
changeDiv=1 #cambiar div durante sim(1)/ mantener div(0)
simulacionesPorDensidad=100 #n sim por densidad
placesPerUAV=6
video=True
######################################################################################################
##                          Simulacion para diferentes densidades por celda
######################################################################################################
for densidadActualSim in range(densidadMin,densidadMax+1,2): #Densidad (#targets/celda)
    consumoTotal=[] #Consumo en toda la sim
    consumoAcumulado=[] 
    ''' ############################  Inicializacion escenario, UAVs y objetivos  ############################ '''
    actualizaciones=0
    if autom:
        div=divIniciales
    else:
        div=input('Ingrese el numero de divisiones') #base y altura de la malla

    nPlaces=densidadActualSim*div**2
    nUAVs=round(nPlaces/placesPerUAV) #Numero de UAVs segun densidad deseada
    places=np.random.rand(nPlaces,2)*radOper/1000 #(x,y) posiciones [km] en AreaOperaciones 
    consumoUAVs= np.zeros(nUAVs) #Registro de consumo por UAV

    initialUAVs= np.random.rand(nUAVs,2)*radOper/1000 #Ubicaciones iniciales UAVs aleatorias   
    #initialUAVs= [radOper/1000,radOper/1000]-(rand(nUAVs,2)*radOper/1000)/10 #UAVs iniciales en ultima celda
    #initialUAVs= (rand(nUAVs,2)*radOper/1000)/10 #UAVs iniciales en celda inicial

    C=np.array([range((div-1)*div+1,div*div+1)])#Matriz de indices
    for i in range(div-1,0,-1):
        C=np.append(C,range((i-1)*div+1,div*i+1))
    F=True
    [colors,F]=myFcns.initialScatter(places,initialUAVs,div,radOper,C,autom,F,video) #Estado inicial de algoritmo
    deltaMatrix=np.zeros([div*2,div])
    deltaRight=np.zeros(div) #Matriz de deltas a actualizar por lideres en celdas
    
#    if not autom:
#        sinTerminar=input('Ingrese 1 para sinTerminar')
#    else:
#        sinTerminar=1
        
