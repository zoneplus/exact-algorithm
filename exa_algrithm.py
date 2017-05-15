#encoding=utf-8
import numpy as np
import math
import pandas as pd
import sys
import matplotlib.pyplot as plt
#from bisearchi import bisearching
'''Cb = 2;Ch = 0.5;lambd = np.array([1.0,0.5,0.2])
ch = np.array([0.095,0.0235,0.01])
A = 100
a = np.array([80,70,20])
#H = 214.7692
#h = np.array([85.5,16.92,4.2])
n = 3
D = 600
d = np.array([900,720,420])'''
class exact_algrim(object):
    def __init__(self,Cb,Ch,lambd,ch,A,a,n,D,d):
        self.Cb = Cb
        self.Ch = Ch
        self.lambd = lambd#numpyarray
        self.ch = ch#numpyarray
        self.A = A
        self.a = a#numpyarray
        self.n = n#number of item
        self.D = D
        self.d = d#numpyarray
        #self.k = k#numpyarray
    def F(self):
        return self.Cb/(self.Cb+self.Ch+np.sum(self.lambd*self.ch))
    def H(self):
        CH = self.Ch+sum(self.lambd*self.ch)
        return (self.F()*CH-sum(self.lambd*self.ch))*self.D
    def h(self):
        return self.ch*self.d
    def T(self):
        H = self.H()
        h = self.h()
        U = math.sqrt(2*float(self.A+sum(self.a))/(H+sum(h)))
        L = float(self.A)/(math.sqrt(2*float(self.A+sum(self.a))*(H+sum(h))))
        return (L,U)
    def C(self):
        H = self.H()
        h = self.h()
        return math.sqrt(2*float(self.A+sum(self.a))*(H+sum(h)))
    def t(self,k,j):
        t_t = math.sqrt(2*self.a[j]/self.h()[j])*math.sqrt(1.0/k-1.0/(k+1))
        return float('%.11f'%t_t)
    def jonction_points(self,n,L,U):
            item = {}
            k_num_dic = {}
            item.setdefault(L,[])
            for j1 in range(n):
                k = 1
                item[j1] = []
                if self.t(k,j1)<L:
                    pass
                if self.t(k,j1)>U:
                    k = k+1
                while self.t(k,j1)>=L and self.t(k,j1)<=U:
                    item[j1].append(self.t(k,j1))
                    k = k+1
                k_num_dic[j1] = k
            item.pop(L)
            #print "item",item
            return (item,k_num_dic)
    def merge(self,lis):
        nums1 = lis[0]
        for l in range(len(lis))[1:]:
            nums3 = []
            nums2 = lis[l]
            m = len(nums1)
            n = len(nums2)
            i = 0;j = 0
            while i<m and j<n:
                if nums1[i]>nums2[j]:
                    nums3.append(nums1[i])
                    i = i+1
                else:
                    nums3.append(nums2[j])
                    j = j+1
            while i<m:
                nums3.append(nums1[i])
                i = i+1
            while j<n:
                nums3.append(nums2[j])
                j = j+1
            nums1 = nums3
        return nums3
    def optim_K(self,n,points_set,k_num_dic):
        K_list = []
         for i in range(len(points_set)-1):
            interval_list = []
            for key in range(n):#dict is not in order!!
                k_lis = 1
                #print k_num_dic[key]+1
                for k in range(k_num_dic[key]+1)[1:]:
                    if points_set[i+1]>self.t(1,key):
                        k_lis = 1
                    elif k>=2 and points_set[i+1]>=self.t(k,key) and points_set[i+1]<=self.t(k-1,key):
                        k_lis= k
                    else:
                        pass
                interval_list.append(k_lis)
            K_list.append(interval_list)
        return K_list
    def T_K(self,K):
        T_K_F =math.sqrt(2.0*(self.A+sum(1.0*self.a/K))/(self.H()+sum(self.h()*K)))
        return float('%.11f'%T_K_F)
    def target(self,K,T):
        return (K,T,self.A/T+self.H()*T/2+sum(1.0*self.a/K)/T+T*sum(self.h()*K)/2)
    def bisearching(self,s,tag):
        lo = 0
        hi = len(s)-1
        while lo<hi:
            mid = (lo+hi)//2
            print s[mid] 
             
            if s[mid][1]<s[mid][2][0]:
                minf = ea.target(s[mid][0],s[mid][2][0])
                print "--------------------------",self.C(),minf
            elif s[mid][1]>s[mid][2][1]:
                minf = ea.target(s[mid][0],s[mid][2][1])
                print "--------------------------",self.C(),minf
            else:
                minf = ea.target(s[mid][0],s[mid][1])
                print "--------------------------",self.C(),minf
            mindif = minf[2]-tag
            if mindif<0:
                print s[mid-1]
                return mid-1
            elif mindif>0:  
                lo = mid +1 
            else:
                return mid  
          
    def func(self):
        ea = exact_algrim(self.Cb,self.Ch,self.lambd,self.ch,self.A,self.a,self.n,self.D,self.d)
        bound_tup = ea.T()
        L = bound_tup[0]
        U = bound_tup[1]
        item_dict,k_num_dic = ea.jonction_points(self.n,L,U)
        junc_point_list = []
        for value in item_dict.values():
            junc_point_list.append(value)
        e = ea.merge(junc_point_list)

        points_set = []
        points_set.append(U)
        for t in e:
            points_set.append(t)
        points_set.append(L)
        points_set.reverse()
        print 'points_set',points_set
        K_list = ea.optim_K(self.n,points_set,k_num_dic)
        T_value_K = []
        for K_set in K_list:
            K_set = np.array(K_set)
            result_t = ea.T_K(K_set)
            T_value_K.append(result_t)
        junc_list = []
        for p in range(len(points_set)-1):
            junc_tup = ()
            junc_tup = (points_set[p],points_set[p+1])
            junc_list.append(junc_tup)
        minf_set = []
        f_set = []
        z_set = []
        comb = zip(K_list,T_value_K,junc_list)
        c= self.C()
        print c
        ind = self.bisearching(comb,c)
        for k,t,p in zip(K_list,T_value_K,junc_list)[ind:]:
            if t<p[0]:
                minf = ea.target(k,min(p[0],p[1]))
                minf_set.append(minf)
            elif t>p[1]:
                minf = ea.target(k,max(p[0],p[1]))
                minf_set.append(minf)
            else:
                minf = ea.target(k,t)
                minf_set.append(minf)
            for z in  np.arange(p[0],p[1],0.0001).tolist():
                f = ea.target(k,z)
                f_set.append(f[2])
                z_set.append(z)
        df = pd.DataFrame(minf_set)
        r = min(df[2])
        print df[df[2]==r]
        return df[df[2]==r]
'''ea = exact_algrim(Cb,Ch,lambd,ch,A,a,n,D,d)
ea.func()'''
