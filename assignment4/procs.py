from numpy import *
import pickle
import gzip

jpmf= pickle.load(gzip.open('jpmf.p.gz','rb'))

#Solution for Q 1.4
pA1=jpmf.sum(5).sum(4).sum(3).sum(2).sum(1)
pB1=jpmf.sum(5).sum(4).sum(3).sum(1).sum(0)
pC1=jpmf.sum(5).sum(3).sum(2).sum(1).sum(0)
pA2=jpmf.sum(5).sum(4).sum(3).sum(2).sum(0)

#P(B1|A1,A2)
pbaa=jpmf.sum(5).sum(4).sum(3)
paa=jpmf.sum(5).sum(4).sum(3).sum(2)
res3=zeros(pbaa.shape)

for i in range(0,pbaa.shape[0]):
    for j in range(0,pbaa.shape[1]):
        for k in range(0,pbaa.shape[2]):
            res3[i,j,k]=pbaa[i,j,k]/paa[i,j]

#C1/B1=P(C1,B1)/P(B1) 
pcb=jpmf.sum(5).sum(3).sum(1).sum(0)
pb=jpmf.sum(5).sum(4).sum(3).sum(1).sum(0)
res1=zeros(pcb.shape)

for i in range(0,pcb.shape[0]):
    for j in range(0,pcb.shape[1]):
        res1[i,j]=pcb[i,j]/pb[i]

#P(A1)*P(A2)*P(B2|A2,A1)*P(C1,B1)
res4=zeros(shape=(pA1.shape[0],pA2.shape[0],pB1.shape[0],pC1.shape[0]))

for a1 in range(0,pA1.shape[0]):
    for a2 in range(0,pA2.shape[0]):
        for b1 in range(0,pB1.shape[0]):
            for c1 in range(0,pC1.shape[0]):
                res4[a1,a2,b1,c1]=pA1[a1]*pA2[a2]*res3[a1,a2,b1]*res1[b1,c1]

#Sumation
pA1C1=res4.sum(2).sum(1)

#Normalization
for a1 in range(0,pA1C1.shape[0]):
    for c1 in range(0,pA1C1.shape[1]):
        pA1C1[a1,c1]=pA1C1[a1,c1]/pC1[c1]

#Problem 2

pA1B1=jpmf.sum(5).sum(4).sum(3).sum(1)
pB1gA1=zeros(pA1B1.shape)

for a1 in range(0,pA1B1.shape[0]):
    for b1 in range(0,pA1B1.shape[1]):
        
