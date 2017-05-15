#encoding=utf-8
from exa_algrithm import exact_algrim
import numpy as np
import pandas as pd
import time
start =time.clock()
data1 = open('Data1.txt','r')
dr = data1.readlines()
minmum_f_list = pd.DataFrame()
for i in range(len(dr)):
    if i%9==0:
        n = dr[i]
        A = dr[i+1]
        D = dr[i+2]
        Ch = dr[i+3]
        Cb = dr[i+4]
        a = dr[i+5]
        ch = dr[i+6]
        lambd = dr[i+7]
        d = dr[i+8]
        ea = exact_algrim(float(Cb),float(Ch),np.array([float(i) for i in lambd.split(',')]),np.array([float(i) for i in ch.split(',')]),float(A),np.array([float(i) for i in a.split(',')]),int(n),float(D),np.array([float(i) for i in d.split(',')])*float(D))
        minum_f = ea.func()
        #print minum_f
        minmum_f_list = minmum_f_list.append(minum_f)
        print('Running time: %s Seconds'%(time.clock()-start))
minmum_f_list.to_csv('output.csv',header=False)
end = time.clock()
print('Running time: %s Seconds'%(end-start))