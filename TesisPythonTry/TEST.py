import numpy as np

trying=np.array([[1,-2],[-2,3],[3,6],[-4,-2]])
tryingNorma=np.linalg.norm(trying,axis=1)
tryingNorma=np.c_[tryingNorma,tryingNorma]
print(tryingNorma)
hey=[1]
hey.append(3)
print(hey)
print(np.divide(trying,tryingNorma))
print((np.array([False, True])-1)*(-1))