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
from matplotlib import pyplot
import numpy as np

######################################################################################################
##                      Simulación de Método Distribuido: Min Costo UAV/Destino
######################################################################################################

#calculo de radio de Operaciones, consumo y vel óptimos
[radOper,PtOptimum,vOptimum]=GRIDFcns.CalcularParametrosEnergeticos()

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
changeDiv=1 #cambiar div durante sim(1)/ mantener div(0)
video=True

''' ############################  Inicializacion escenario, UAVs, Puntos Recolección y objetivos  ############################ '''
nQ=90 #Numero de Objetivos
nP=round(nQ/qPerUAV) #Numero de UAVs segun densidad deseada
nR=5 #Numero de Puntos Recolección/despliegue

q=np.random.rand(nQ,2)*radOper/1000 #(x,y) posiciones [km] de objetivos en AreaOperaciones 
r=np.random.rand(nR,2)*radOper/1000 #(x,y) posiciones [km] de recolectores en AreaOperaciones
w= np.zeros(nP) #Registro de consumo por UAV

################################ division de espacio en cuadrículas ################################
if autom:
    div=divIniciales #div default
else:
    div=input('Ingrese el numero de divisiones') #base y altura de la malla (div personalizado)
####################################################################################################

p= np.random.rand(nP,2)*radOper/1000   #inicializacion de matriz de UAVs
for pIndex in range(nP): #Ubicaciones iniciales en Recolectores aleatorios 
    p[pIndex]=r[int(round(np.random.rand()*nR-0.5))] + (np.random.rand(1,2)-0.5)
pZero=p
C=np.array([range((div-1)*div+1,div*div+1)]) # Matriz de indices para identificar celdas
for i in range(div-1,0,-1):
    C=np.append(C,[range((i-1)*div+1,div*i+1)],axis=0)

TesisFcns.initialScatter(q,r,p,pZero,div,radOper,C,autom,video) #ploteo inicial

for iter in range(40):
    ''' CONDICIONAR RECORRIDO CON EL NUMERO DE NODOS EN TIPO DE PARTICION ESPACIAL'''
    for nodoActual in range(1,div**2+1): #recorrido sobre todas las celdas 
        [pInNode, indexP, qInNode,indexQ,rNode]= GRIDFcns.pqrInNode(nodoActual,p,q,r,C,radOper,div)
        Amatrix= np.zeros((qInNode.shape[0],pInNode.shape[0])) #inicialización de matriz de pesos

        #Matriz de distancias P_i a Q_i
        xdeltapq= qInNode[:,0].reshape(qInNode.shape[0],1)-pInNode[:,0].reshape(1,pInNode.shape[0])
        ydeltapq= qInNode[:,1].reshape(qInNode.shape[0],1)-pInNode[:,1].reshape(1,pInNode.shape[0])
        distancepq= np.sqrt(np.add(np.square(xdeltapq),np.square(ydeltapq)))
        #Matriz de distancias Q_i a R_i
        xdeltaqr= np.ones(qInNode.shape[0],1)*rNode[0] -qInNode[:,0].reshape(1,qInNode.shape[0])
        ydeltaqr= np.ones(qInNode.shape[0],1)*rNode[1] -qInNode[:,1].reshape(1,qInNode.shape[0])
        distanceqr= np.sqrt(np.add(np.square(xdeltaqr),np.square(ydeltaqr)))

        Amatrix=distancepq*PtOptimum/vOptimum +distanceqr*PtOptimum/vOptimum #matriz de pesos
        wNode=w[indexP]
        asignE=Amatrix>wNode #inicialización de la matriz con arcos que pueden ser recorridos






