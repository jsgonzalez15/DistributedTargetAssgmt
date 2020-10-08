"""
2. Réplica método distribuido GRID target Assignment y extensión a asignación de tareas no monotónicas.

Temas:
* Consumo energético.
* Eficiencia de método iterativo.
* Incidencia en concentración de agentes y división iterativa.
* Efectos de puntos de inicio en el mapa.

@author: Juan Sebastián González Rojas 201612109
@email: js.gonzalez15@uniandes.edu.co
"""
import GRIDassgmtFunctions as GRIDFcns
from matplotlib import pyplot
import numpy as np
######################################################################################################
##                          Simulación Metodos Distribuidos: GRID Assignment
######################################################################################################
 
#calculo de radio de Operaciones, consumo y vel óptimos
[radOper,PtOptimum,vOptimum]=GRIDFcns.CalcularParametrosEnergeticos()

[densidadMin,densidadMax]=[10,10] #Rango de densidades a simular
consumoDensidad=[] #valores medios y desviación estándar por densidad
consumoIteracion=[] #valores medios y desviación estándar en consumo por iteración
desviacionConsumoUAVs=0 #max desv de consumo entre UAVs (ideal 0)
divIniciales=3 #divisiones iniciales
placesPerUAV=6
dt=0.3

video=0 #obtener un video de simulación (1) ejecutar sin video (0)
autom=1 #autom sim(1)/ver todo(0)
changeDiv=1 #cambiar div durante sim(1)/ mantener div(0)
simulacionesPorDensidad=100 #n sim por densidad
video=True #guardar video de la simulación

######################################################################################################
##                          Simulacion para diferentes densidades por celda
######################################################################################################
for densidadActualSim in range(densidadMin,densidadMax+1,2): #Densidad (#targets/celda)

    consumoTotal=[] #Vector de Consumo en toda la sim
    consumoAcumulado=[]  #Vector de Consumo acumulado por sim 
    ''' ############################  Inicializacion escenario, UAVs y objetivos  ############################ '''
    actualizaciones=0
    if autom:
        div=divIniciales #div default
    else:
        div=input('Ingrese el numero de divisiones') #base y altura de la malla (div personalizado)

    nPlaces=densidadActualSim*div**2
    nUAVs=round(nPlaces/placesPerUAV) #Numero de UAVs segun densidad deseada
    places=np.random.rand(nPlaces,2)*radOper/1000 #(x,y) posiciones [km] en AreaOperaciones 
    consumoUAVs= np.zeros(nUAVs) #Registro de consumo por UAV

    #(x,y,asign) posiciones [km] y asignaciones (+1) Lider (-1) No Asignado
    initialUAVs= np.concatenate(((np.random.rand(nUAVs,2)*radOper/1000),np.zeros((nUAVs,1))),axis=1)
    C=np.array([range((div-1)*div+1,div*div+1)]) # Matriz de indices para identificar celdas
    for i in range(div-1,0,-1):
        C=np.append(C,[range((i-1)*div+1,div*i+1)],axis=0)
    print(C)
    
    GRIDFcns.initialScatter(places,initialUAVs,div,radOper,C,autom,video) #Estado inicial de algoritmo
    deltaMatrix=np.zeros([div*2,div])
    deltaRight=np.zeros(div) #Matriz de deltas a actualizar por lideres en celdas
    
#    if not autom:
#        sinTerminar=input('Ingrese 1 para sinTerminar')
#    else:
#        sinTerminar=1
    ####################################################################################################################################################
    ##  INICIO                               Simulacion de asignacion Monotonica GRID target Assgmt (Densidad Actual)
    ####################################################################################################################################################
    targetsMet=[] #Targets que han sido alcanzados
    iterations=0 #Iteraciones hasta alcanzar objetivos
    #while (len(targetsMet)<len(initialUAVs)) and (len(targetsMet)<len(places)): #Sim hasta:(a) todos los UAV llegaron, o, (b) targets agotados
    for i in range(50):
        for celdaActual in range(1,div**2): #recorrido sobre todas las celdas
            asignados=0 #cantidad de UAVs asignados en celda de iteracion actual
            distancias=[] #vector de distancias actuales entre asignados y objetivos
            [CurrentCellInfo,aNumber,indicesUAVinCell,indicesTargetsInCell]=GRIDFcns.uavAndTargetInCell(celdaActual,initialUAVs,places,C,radOper,div)
            currentRow=div-1-(celdaActual-1)//div
            currentColumn=(celdaActual-1)%div
            print(str(currentRow)+","+str(currentColumn))
            deltaMatrix[(currentRow+1)*2-1][currentColumn]=len(CurrentCellInfo)-2*aNumber #calculo de delta local
            if currentRow !=0: #calculo de delta columna
               deltaMatrix[currentRow*2,currentColumn]=deltaMatrix[(currentRow-1)*2,currentColumn]+deltaMatrix[(currentRow-1)*2+1,currentColumn]
            if aNumber!=0: #Revision de la celda cuando hay UAVs presentes
                GRIDFcns.initialScatter(places,initialUAVs,div,radOper,C,autom,video)
                if len(CurrentCellInfo)-aNumber<aNumber:
                    asignados=len(CurrentCellInfo)-aNumber
                else:
                    asignados=aNumber
                distancias=np.array(CurrentCellInfo[aNumber:aNumber+asignados])-np.array(CurrentCellInfo[0:aNumber])[:,[0,1]]
                normas=np.linalg.norm(distancias,axis=1)
                normasMatrix=np.c_[normas,normas]
                vunit=np.divide(distancias,normasMatrix) #vector unitario de movimiento UAV-lugar
                dx=vunit*dt #vector de movimiento según dt
                dxnorm=np.linalg.norm(dx,axis=1)
                arrivingBool=dxnorm>normas*dt #vector de booleanos para movimiento de llegada
                
                print("Celda actual")
                print(celdaActual)
                print("Indices:"+str(currentRow)+","+str(currentColumn)+" lugar "+str(C[currentRow,currentColumn]))
                print("CurrentCellInfo")
                print(CurrentCellInfo)
                print("InitialUAVs")
                print(initialUAVs)
                #print("Distancias a asignacion")
                #print(distancias)
                CurrentCellInfo[0:aNumber]=CurrentCellInfo[0:aNumber]+distancias*arrivingBool*dt #llegada
                CurrentCellInfo[0:aNumber]=CurrentCellInfo[0:aNumber]+dx*(arrivingBool-1)*(-1) #movimiento
                initialUAVs[indicesUAVinCell]=CurrentCellInfo[0:aNumber] #actualizacion en informacion global
            
#            for celdaActual=1:div-1:#Recorrido ultima fila (actualizacion delta columnas siguientes
#                    deltaRight(div-celdaActual)= deltaRight(div-celdaActual+1)+deltaMatrix(2*div,div-celdaActual+1)+deltaMatrix(2*div-1,div-celdaActual+1)
#            
    iterations=iterations+1
    ####################################################################################################################################################
    ##  FIN                                 Simulacion de asignacion Monotonica GRID target Assgmt (Densidad Actual)
    ####################################################################################################################################################
    