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
placesPerUAV=6 #Proporción de objetivos por UAV
consumoDensidad=[] #valores medios y desviación estándar por densidad
consumoIteracion=[] #valores medios y desviación estándar en consumo por iteración
desviacionConsumoUAVs=0 #max desv de consumo entre UAVs (ideal 0)
divIniciales=3 #divisiones iniciales
simulacionesPorDensidad=100 #n sim por densidad
dt=0.3

video=0 #obtener un video de simulación (1) ejecutar sin video (0)
autom=1 #autom sim(1)/ver todo(0)
changeDiv=1 #cambiar div durante sim(1)/ mantener div(0)
video=True

''' ############################  Inicializacion escenario, UAVs, Puntos Recolección y objetivos  ############################ '''
nPlaces=90 #Numero de Objetivos
nUAVs=round(nPlaces/placesPerUAV) #Numero de UAVs segun densidad deseada
nRecolectors=5 #Numero de Puntos Recolección/despliegue

places=np.random.rand(nPlaces,2)*radOper/1000 #(x,y) posiciones [km] en AreaOperaciones 
recolectors=np.random.rand(nRecolectors,2)*radOper/1000 #(x,y) posiciones [km] en AreaOperaciones
consumoUAVs= np.zeros(nUAVs) #Registro de consumo por UAV

initialUAVs= np.random.rand(nUAVs,2)*radOper/1000 #Ubicaciones iniciales en Recolectores aleatorios   
print(recolectors)
for initialUAVsIndex in range(nUAVs):
    initialUAVs[initialUAVsIndex]=recolectors[int(round(np.random.rand()*nRecolectors-0.5))] + (np.random.rand(1,2)-0.5)
print(initialUAVs)

