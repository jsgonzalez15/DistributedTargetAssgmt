"""
Métodos para visualizar datos de simulación de caracterización.

@author: Juan Sebastián González Rojas 201612109
@email: js.gonzalez15@uniandes.edu.co
"""
import json
from matplotlib import pyplot as plt
import numpy as np

# Nombres de archivos JSON según información almacenada de simulaciones
# Nomenclatura: AlgoritmoAnalisisParticionID
# ej: tesisDivsGRID1 Algoritmo: Propuesta Tesis, Análisis: Variar Particiones, Partición: GRID, ID:1
glosario=["tesisDivsGRID1.json","tesisDivsGRID2.json","tesisFleetGRID1.json","tesisFleetGRID2.json"]
glosario.append(["GRIDDivsGRID1.json","GRIDDivsGRID2.json","GRIDFleetGRID1.json","GRIDFleetGRID2.json"])

json_file=open("./jsons/"+ glosario[0],"r",encoding="utf-8")
simData=json.load(json_file)
json_file.close()

npArrayData=np.array(simData["dataP"]) #promedios de simulación por cada p
npArrayDesv=np.array(simData["desvP"]) #desviación estándar de simulación
npArrayDataTotal=np.array(simData["dataPTotal"]) #promedios de simulación total de la flota
npArrayDesvTotal=np.array(simData["desvPTotal"]) #desviación estándar de simulación

npArrayData=npArrayData[0,0]-npArrayData

nP=round(int(simData["nQ"])/int(simData["qPerUAV"]))
deltaIter=npArrayData[1:]-npArrayData[0:-1]
deltaDesv=np.sqrt(np.add(np.square(npArrayDesv[1:]),np.square(npArrayDesv[0:-1])))

divs=np.array([1,2,3,4]) #Divisiones utilizadas en simulación
#for column in range(divs.shape[0]): #npArrayData.shape[1]
for column in range(4):
    #Gráfica de líneas
    plt.plot(np.array(range(npArrayData.shape[0])),npArrayData[:,column],label="Nodes ="+str(divs[column]**2))

    #Gráfica de consumo por iteración
    #plt.errorbar(np.array(range(1,deltaIter.shape[0]+1)),deltaIter[:,column],yerr=npArrayDesv[1:,column],capsize=5,label="Nodes ="+str(divs[column]**2))

    #Gráfica de evolución acumulado de consumo
    #plt.errorbar(np.array(range(npArrayData.shape[0])),npArrayData[:,column],yerr=npArrayDesv[:,column],capsize=5,label="Nodes= "+str(divs[column]**2))

    #Gráfica de evolución acumulado de consumo total
    #plt.errorbar(np.array(range(npArrayDataTotal.shape[0])),npArrayDataTotal[:,column], yerr=npArrayDesvTotal[:,column], capsize=5, label="Nodes= "+str(divs[column]**2))

#print("Average consumption per iteration:",npArrayData)
#print("Maximum deviation of simulation: ",np.max(npArrayDesv))
plt.xlabel('Iteration of Simulation')
plt.ylabel('Average Energy Consumption (Wh)')
plt.legend()
''' CONDICIONAR TITLE SEGUN PARTICION'''
plt.title('Iteration Average Consumption per UAV (nQ: '+simData["nQ"]+", nP: "+str(nP)+")")
plt.grid()
plt.show()