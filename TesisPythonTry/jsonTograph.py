"""
Métodos para visualizar datos de simulación de caracterización.

@author: Juan Sebastián González Rojas 201612109
@email: js.gonzalez15@uniandes.edu.co
"""
import json
from matplotlib import pyplot as plt
from matplotlib import rc
import numpy as np
from matplotlib import rc

import matplotlib as mpl
import matplotlib.font_manager as font_manager

# Nombres de archivos JSON según información almacenada de simulaciones
# Nomenclatura: AlgoritmoAnalisisParticionID
# ej: tesisDivsGRID1 Algoritmo: Propuesta Tesis, Análisis: Variar Particiones, Partición: GRID, ID:1
glosario=[["tesisDivsGRID1.json","tesisDivsGRID2.json","tesisDivsGRID3.json","tesisDivsGRID4.json","tesisFleetGRID1.json","tesisFleetGRID2.json"]]
glosario.append(["tesisGRIDDivsGRID1.json","tesisGRIDDivsGRID2.json","tesisGRIDDivsGRID3.json","tesisGRIDDivsGRID4.json","tesisGRIDFleetGRID1.json","tesisGRIDFleetGRID2.json"])
glosario.append(["GRIDDivsGRID1.json","GRIDDivsGRID2.json","GRIDFleetGRID1.json","GRIDFleetGRID2.json"])

legends=[""," (GRID)"]
colors=["r","b"]
plt.rcParams['font.family'] = 'Nimbus Roman No9 L'
plt.rcParams['pdf.fonttype'] = 42

for comparing in range(0,2):
    reading=glosario[comparing][3]
    print("//---------------------------------//")
    print(reading)
    json_file=open("./jsons/"+ reading,"r",encoding="utf-8")
    simData=json.load(json_file)
    json_file.close()

    print(simData["info"])
    #npArrayData=np.array(simData["dataP"]) #promedios de simulación por cada p
    npArrayData=np.array(simData["w_min"]) #valores mínimos de simulación para todo p    
    #npArrayDesv=np.array(simData["desvP"]) #desviación estándar de simulación
    #npArrayDataTotal=np.array(simData["dataPTotal"]) #promedios de simulación total de la flota
    #npArrayDesvTotal=np.array(simData["desvPTotal"]) #desviación estándar de simulación
    wmin=266*0.05
    #averageDistributed=np.mean(npArrayData[:8,1:])
    #averageCentralized=np.mean(npArrayData[:8,0])
    #print(averageDistributed-averageCentralized)

    valid=8
    npArrayData=npArrayData[:valid,:]#int(simData["qperUAV"]),:]
    #npArrayDataTotal=npArrayDataTotal[:valid,:]#int(simData["qperUAV"]),:]
    #npArrayDesv=npArrayDesv[:valid,:]#int(simData["qperUAV"]),:]
    #npArrayDesvTotal=npArrayDesvTotal[:valid,:]#int(simData["qperUAV"]),:]

    nP=round(int(simData["nQ"])/int(simData["qPerUAV"]))
    #deltaIter=npArrayData[1:]-npArrayData[0:-1]
    #deltaDesv=np.sqrt(np.add(np.square(npArrayDesv[1:]),np.square(npArrayDesv[0:-1])))
    
    divs=np.array([1,2,3,4]) #Divisiones utilizadas en simulación
    theFleet=np.array(range(45,110,15))

    #rc('text', usetex=True)

    #rc('text.latex', preamble=r'\usepackage{cmbright}')
    #for column in range(divs.shape[0]): #npArrayData.shape[1]
    if "Fleet" in reading:
        for fleetSize in range(4):
            #Gráfica de promedios UAV
            plt.plot(np.array(range(npArrayData.shape[0])),npArrayData[:,fleetSize],label="$n_q= $"+str(theFleet[fleetSize]))
            #Gráfica de promedios total
            #plt.plot(np.array(range(npArrayDataTotal.shape[0])),npArrayDataTotal[:,fleetSize],label="$n_q= $"+str(theFleet[fleetSize]))

            #Gráfica de consumo por iteración
            #plt.errorbar(np.array(range(1,deltaIter.shape[0]+1)),deltaIter[:,fleetSize],yerr=npArrayDesv[1:,fleetSize],capsize=5,label="$n_q= $"+str(theFleet[fleetSize]))

            #Gráfica de evolución acumulado de consumo
            #if comparing ==0:
                #plt.errorbar(np.array(range(1,npArrayData.shape[0]+1)),npArrayData[:,fleetSize],yerr=npArrayDesv[:,fleetSize],capsize=5,label="DE-GA, $n_q= $"+str(theFleet[fleetSize]), linewidth=2)
            #else:
                #plt.errorbar(np.array(range(1,npArrayData.shape[0]+1)),npArrayData[:,fleetSize],yerr=npArrayDesv[:,fleetSize],capsize=5,label="Grid, $n_q= $"+str(theFleet[fleetSize]), linestyle="--")
            #plt.title('KPI Performance in 250 Simulations ($n= 9$'+", $n_q$ / $n_v=$ "+str(simData["qPerUAV"])+")")
            #plt.title('Iteration Total Consumption per UAV ($n_q=$ '+simData["nQ"]+", $n_v:$ "+str(nP)+")")

            #Gráfica de evolución acumulado de consumo total
            #plt.errorbar(np.array(range(npArrayDataTotal.shape[0])),npArrayDataTotal[:,fleetSize], yerr=npArrayDesvTotal[:,fleetSize], capsize=5, label="$n_q= $"+str(theFleet[fleetSize]))
            
    else:   
        for column in range(4):
            #Gráfica de promedios UAV
            #plt.plot(np.array(range(npArrayData.shape[0])),npArrayData[:,column],label="$n =$"+str(divs[column]**2))
            if comparing==0:
                plt.plot(np.array(range(npArrayData.shape[0]))+1,npArrayData[:,column],label="DE-GA, $n =$"+str(divs[column]**2))
            else:
                plt.plot(np.array(range(npArrayData.shape[0]))+1,npArrayData[:,column], label="GRID, $n =$"+str(divs[column]**2))
            
            #Gráfica de promedios total
            #plt.plot(np.array(range(npArrayDataTotal.shape[0])),npArrayDataTotal[:,column],label="$n =$"+str(divs[column]**2))

            #Gráfica de consumo por iteración
            #plt.errorbar(np.array(range(1,deltaIter.shape[0]+1)),deltaIter[:,column],yerr=npArrayDesv[1:,column],capsize=5,label="$n =$"+str(divs[column]**2))

            #Gráfica de evolución acumulado de consumo
            #plt.errorbar(np.array(range(npArrayData.shape[0])),npArrayData[:,column],yerr=npArrayDesv[:,column],capsize=5,label="$n =$"+str(divs[column]**2))

            #Gráfica de evolución acumulado de consumo total
            #if comparing ==0:
            #    plt.errorbar(np.array(range(1,npArrayDataTotal.shape[0]+1)),npArrayDataTotal[:,column], yerr=npArrayDesvTotal[:,column], capsize=5, label="DE-GA, $n$ = "+str(divs[column]**2), linewidth=2)
            #else:
            #    plt.errorbar(np.array(range(1,npArrayDataTotal.shape[0]+1)),npArrayDataTotal[:,column], yerr=npArrayDesvTotal[:,column], capsize=5, label="Grid, $n$ = "+str(divs[column]**2), linestyle="--")

            #plt.title('Iteration Total Consumption for UAV fleet ($n =$ 3, $n_q$ / $n_v=$ 6)')
            #plt.title('KPI Performance for 250 Simulations ($n_q= $'+simData["nQ"]+", $n_v$= "+str(nP)+")")
            plt.title('Min energy storage available in fleet ($n_q= $'+simData["nQ"]+", $n_v$= "+str(nP)+")")
    
    
    #print("Average consumption per iteration:",npArrayData)
    #print("Maximum deviation of simulation: ",np.max(npArrayDesv))
    
    ''' CONDICIONAR TITLE SEGUN PARTICION'''
plt.plot(np.array(range(npArrayData.shape[0]))+1,np.ones(npArrayData.shape[0])*wmin,label="$w_{min}$",linestyle="--",color="k")
plt.xlabel('Iteration of Simulation')
plt.ylabel('Energy storage (Wh)')
plt.legend()
plt.grid()
plt.show()