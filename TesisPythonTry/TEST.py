import numpy as np
from numpy import doc
import GRIDassgmtFunctions as GRIDFcns
from matplotlib import pyplot as plt
import cv2
from mpl_toolkits import mplot3d
import time
import json
[radOper,PtOptimum,vOptimum,capJoules]=GRIDFcns.CalcularParametrosEnergeticos()
print(radOper)
print(PtOptimum)
print(vOptimum)

w=np.ones(10)
wIter=np.c_[w,w*2,w,w]

print(w[1:])