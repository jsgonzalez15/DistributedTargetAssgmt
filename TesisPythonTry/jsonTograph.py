import json
from matplotlib import pyplot as plt
import numpy as np

json_file=open("dataStoredTesisGRIDB.json","r",encoding="utf-8")
simData=json.load(json_file)
json_file.close()

npArrayData=np.array(simData["data"]) #promedios de simulación
npArrayDesv=np.array(simData["desv"]) #desviación estándar de simulación

npArrayData=npArrayData/3600 #Conversión de Joules a Wh
npArrayData=npArrayData[0,0]-npArrayData
npArrayDesv=npArrayDesv/3600 #Conversión de Joules a Wh
npArrayDesv[0,:]=0

nP=round(int(simData["nQ"])/int(simData["qPerUAV"]))
deltaIter=npArrayData[1:]-npArrayData[0:-1]
deltaDesv=np.sqrt(np.add(np.square(npArrayDesv[1:]),np.square(npArrayDesv[0:-1])))

divs=np.array([1,2,3,4]) #Divisiones utilizadas en simulación
for column in range(divs.shape[0]): #npArrayData.shape[1]
    #Gráfica de líneas
    #plt.plot(np.array(range(npArrayData.shape[0])),npArrayData[:,column],label="Nodes ="+str(divs[column]**2))
    #Gráfica de consumo por iteración
    plt.errorbar(np.array(range(1,deltaIter.shape[0]+1)),deltaIter[:,column],yerr=npArrayDesv[1:,column],capsize=5,label="Nodes ="+str(divs[column]**2))
    #Gráfica de evolución acumulado de consumo
    #plt.errorbar(np.array(range(npArrayData.shape[0])),npArrayData[:,column],yerr=npArrayDesv[:,column],capsize=5,label="Nodes ="+str(divs[column]**2))

print("Average consumption per iteration:",npArrayData)
print("Maximum deviation of simulation: ",np.max(npArrayDesv))
plt.xlabel('Iteration of Simulation')
plt.ylabel('Average Energy Consumption (Wh)')
plt.legend()
''' CONDICIONAR TITLE SEGUN PARTICION'''
plt.title('Average Accumulative Consumption per UAV (nQ: '+simData["nQ"]+", nP: "+str(nP)+")")
plt.grid()
plt.show()