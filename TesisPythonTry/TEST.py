import numpy as np
from numpy import doc
import GRIDassgmtFunctions as GRIDFcns
from matplotlib import pyplot as plt
import cv2
from mpl_toolkits import mplot3d
import time

[radOper,PtOptimum,vOptimum,capJoules]=GRIDFcns.CalcularParametrosEnergeticos()
print(radOper)
print(PtOptimum)
print(vOptimum)

a=np.array([[True, False, False,False],[False, False, False,False],[False, True, False,False]])
theboolean=np.dot(np.ones(a.shape[0]),a).astype(int)
print(np.where(theboolean==True)[0])
