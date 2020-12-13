"""
Métodos para visualizar datos de simulación de caracterización.

@author: Juan Sebastián González Rojas 201612109
@email: js.gonzalez15@uniandes.edu.co
"""
import json
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import rc
# Nombres de archivos JSON según información almacenada de simulaciones
# Nomenclatura: AlgoritmoAnalisisParticionID
# ej: tesisDivsGRID1 Algoritmo: Propuesta Tesis, Análisis: Variar Particiones, Partición: GRID, ID:1
glosario=[["tesisDivsGRID1.json","tesisDivsGRID2.json","tesisFleetGRID1.json","tesisFleetGRID2.json"]]
glosario.append(["tesisGRIDDivsGRID1.json","tesisGRIDDivsGRID2.json","tesisGRIDFleetGRID1.json","tesisGRIDFleetGRID2.json"])
glosario.append(["GRIDDivsGRID1.json","GRIDDivsGRID2.json","GRIDFleetGRID1.json","GRIDFleetGRID2.json"])

legends=[""," (GRID)"]
colors=["r","b"]
for comparing in range(2,3):
    reading=glosario[comparing][2]
    json_file=open("./jsons/"+ reading,"r",encoding="utf-8")
    simData=json.load(json_file)
    json_file.close()

    npArrayData=np.array(simData["dataP"]) #promedios de simulación por cada p
    npArrayDesv=np.array(simData["desvP"]) #desviación estándar de simulación
    npArrayDataTotal=np.array(simData["dataPTotal"]) #promedios de simulación total de la flota
    npArrayDesvTotal=np.array(simData["desvPTotal"]) #desviación estándar de simulación

    npArrayData=npArrayData[0,0]-npArrayData
    npArrayDataTotal=npArrayDataTotal[0,0]-npArrayDataTotal

    if reading.startswith("GRID"):
        npArrayData=npArrayData[:6,:]#int(simData["qperUAV"]),:]
        npArrayDataTotal=npArrayDataTotal[:6,:]#int(simData["qperUAV"]),:]
        npArrayDesv=npArrayDesv[:6,:]#int(simData["qperUAV"]),:]
        npArrayDesvTotal=npArrayDesvTotal[:6,:]#int(simData["qperUAV"]),:]

    nP=round(int(simData["nQ"])/int(simData["qPerUAV"]))
    deltaIter=npArrayData[1:]-npArrayData[0:-1]
    deltaDesv=np.sqrt(np.add(np.square(npArrayDesv[1:]),np.square(npArrayDesv[0:-1])))

    divs=np.array([1,2,3,4]) #Divisiones utilizadas en simulación
    theFleet=np.array(range(45,110,15))

    rc('text', usetex=True)
    rc('font', size=14)
    rc('legend', fontsize=13)
    rc('text.latex', preamble=r'\usepackage{cmbright}')
    #for column in range(divs.shape[0]): #npArrayData.shape[1]
    if "Fleet" in reading:
        for fleetSize in range(0,5):
            #Gráfica de promedios UAV
            #plt.plot(np.array(range(npArrayData.shape[0])),npArrayData[:,fleetSize],label="Targets ="+str(theFleet[fleetSize]))

            #Gráfica de promedios total
            #plt.plot(np.array(range(npArrayDataTotal.shape[0])),npArrayDataTotal[:,fleetSize],label="Targets ="+str(theFleet[fleetSize]))

            #Gráfica de consumo por iteración
            #plt.errorbar(np.array(range(1,deltaIter.shape[0]+1)),deltaIter[:,fleetSize],yerr=npArrayDesv[1:,fleetSize],capsize=5,label="Targets ="+str(theFleet[fleetSize]))

            #Gráfica de evolución acumulado de consumo
            plt.errorbar(np.array(range(npArrayData.shape[0])),npArrayData[:,fleetSize],yerr=npArrayDesv[:,fleetSize],capsize=5,label="nQ= "+str(theFleet[fleetSize]))
            plt.title('Iteration Total Consumption per UAV (Cells: 9'+", qPerUAV: "+str(simData["qPerUAV"])+")")
            #plt.title('Iteration Total Consumption per UAV (nQ: '+simData["nQ"]+", nP: "+str(nP)+")")

            #Gráfica de evolución acumulado de consumo total
            #plt.errorbar(np.array(range(npArrayDataTotal.shape[0])),npArrayDataTotal[:,fleetSize], yerr=npArrayDesvTotal[:,fleetSize], capsize=5, label="Targets= "+str(theFleet[fleetSize]))
            
    else:   
        for column in range(4):
            #Gráfica de promedios UAV
            #plt.plot(np.array(range(npArrayData.shape[0])),npArrayData[:,column],label="Nodes ="+str(divs[column]**2))

            #Gráfica de promedios total
            #plt.plot(np.array(range(npArrayDataTotal.shape[0])),npArrayDataTotal[:,column],label="Nodes ="+str(divs[column]**2))

            #Gráfica de consumo por iteración
            #plt.errorbar(np.array(range(1,deltaIter.shape[0]+1)),deltaIter[:,column],yerr=npArrayDesv[1:,column],capsize=5,label="Nodes ="+str(divs[column]**2))

            #Gráfica de evolución acumulado de consumo
            #plt.errorbar(np.array(range(npArrayData.shape[0])),npArrayData[:,column],yerr=npArrayDesv[:,column],capsize=5,label="Nodes= "+str(divs[column]**2))

            #Gráfica de evolución acumulado de consumo total
            plt.errorbar(np.array(range(npArrayDataTotal.shape[0])),npArrayDataTotal[:,column], yerr=npArrayDesvTotal[:,column], capsize=5, label="Cells= "+str(divs[column]**2))
            #plt.title('Iteration Total Consumption for UAV fleet (div: 3, qPerUAV: 6)')
            plt.title('Iteration Total Consumption for UAV fleet (nQ: '+simData["nQ"]+", nP: "+str(nP)+")")

    #print("Average consumption per iteration:",npArrayData)
    #print("Maximum deviation of simulation: ",np.max(npArrayDesv))
    plt.xlabel('Iteration of Simulation')
    plt.ylabel('Average Energy Consumption (Wh)')
    plt.legend()
    ''' CONDICIONAR TITLE SEGUN PARTICION'''

plt.grid()
plt.show()