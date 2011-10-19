#Jacobs University Bremen
#Artificial Intellignence Fall 2011
#Ernesto Rodriguez
#
#This program calculates varios probabilities from a given
#pdf for six variables held within a n-dimensional array.

from numpy import *
import pickle
import gzip

jpmf= pickle.load(gzip.open('jpmf.p.gz','rb'))

#Probability of A1
pA1=jpmf.sum(5).sum(4).sum(3).sum(2).sum(1)
print "The probabilities of A1 are: "+pA1.__str__()+"\n"

#Probability of A2
pA2=jpmf.sum(5).sum(4).sum(3).sum(2).sum(0)
print "The probabilities of A2 are: "+pA2.__str__()+"\n"

#B2/A2 Consider Flipping the table P(B2,A2)/P(A2)
pba=jpmf.sum(5).sum(4).sum(2).sum(0)
pa=jpmf.sum(5).sum(4).sum(3).sum(2).sum(0)
res=zeros(pba.shape)

for i in range(0,pba.shape[0]):
    for j in range(0,pba.shape[1]):
        res[i,j]=pba[i,j]/pa[i]

print "The probabilities of B2|A2 are: "+res.__str__()+"\n"

#C1/B1=P(C1,B1)/P(B1) 
pcb=jpmf.sum(5).sum(3).sum(1).sum(0)
pb=jpmf.sum(5).sum(4).sum(3).sum(1).sum(0)
res1=zeros(pcb.shape)

for i in range(0,pcb.shape[0]):
    for j in range(0,pcb.shape[1]):
        res1[i,j]=pcb[i,j]/pb[i]

print "The probabilities for C1|B1 are: "+res1.__str__()+"\n"

#C2/B1=P(C2,B1)/P(B1)
pc2b1=jpmf.sum(4).sum(3).sum(1).sum(0)
pb1=jpmf.sum(5).sum(4).sum(3).sum(1).sum(0)
res2=zeros(pc2b1.shape)

for i in range(0,pc2b1.shape[0]):
    for j in range(0,pc2b1.shape[1]):
        res2[i,j]=pc2b1[i,j]/pb1[i] 

print "The probabilities of C2|B2 are: "+res2.__str__()+"\n"

#B1/A1,A2=P(B1,A1,A2)/P(A1,A2)
pbaa=jpmf.sum(5).sum(4).sum(3)
paa=jpmf.sum(5).sum(4).sum(3).sum(2)
res3=zeros(pbaa.shape)
res31=[]

for i in range(0,pbaa.shape[0]):
    for j in range(0,pbaa.shape[1]):
        for k in range(0,pbaa.shape[2]):
            res3[i,j,k]=pbaa[i,j,k]/paa[i,j]
            res31.append((("A1="+i.__str__(),"A2="+j.__str__(),"B1="+k.__str__()),pbaa[i,j,k]/paa[i,j]))
            

print "The probabilities of B1|A1,A2 are as follows: \n\n"

for i in res31:
    print i[0].__str__()+"  |  "+i[1].__str__()+"\n"

#Check that B2 and A1 are conditionally independent given A2

#P B2,A2
pb2a2=jpmf.sum(5).sum(4).sum(2).sum(0)

#P A2
pa2=jpmf.sum(5).sum(4).sum(3).sum(2).sum(0)

#P B2,A2,A1
pb2a2a1=jpmf.sum(5).sum(4).sum(2)

#P A2,A1
pa2a1=jpmf.sum(5).sum(4).sum(3).sum(2)

res4=zeros(pb2a2.shape)
res5=zeros(pb2a2a1.shape)

for i in range(0,pb2a2.shape[0]):
    for j in range(0,pb2a2.shape[1]):
        res4[i,j]=pb2a2[i,j]/pa2[i]

for i in range(0,pb2a2a1.shape[0]):
    for j in range(0,pb2a2a1.shape[1]):
        for k in range(0,pb2a2a1.shape[2]):
            res5[i,j,k]=pb2a2a1[i,j,k]/pa2a1[i,j]

print "The probabilites of B2|A2,A1 are\n\n: "+res4.__str__()+"\n\n"

print "The probabilites of B2|A1 are:\n\n"+res5.__str__()+"\n\n"

print "We can see that both tables are the same which means that if we know A1 there is no knowledge gained from knowing A2.\n\n"

#Find C1,C2 and check if they are independent. Are they conditionally independent given B1.

#P C1,C2
pc1c2=jpmf.sum(3).sum(2).sum(1).sum(0)

#P C1
pc1=jpmf.sum(5).sum(3).sum(2).sum(1).sum(0)

#P C1
pc2=jpmf.sum(4).sum(3).sum(2).sum(1).sum(0)

#P B1
pb1=jpmf.sum(5).sum(4).sum(3).sum(1).sum(0)

#P C1,C2,B1
pc1c2b1=jpmf.sum(3).sum(1).sum(0)
pc1b1=jpmf.sum(5).sum(3).sum(1).sum(0)

res6=zeros(pc1c2b1.shape)

res7=zeros(pc1c2.shape)
res8=zeros(pc1c2.shape)
res9=zeros(shape=(pc1c2.shape[1],pc1c2.shape[0]))
res10=zeros(pc1c2b1.shape)

for i in range(0,pc1c2.shape[0]):
    for j in range(0,pc1c2.shape[1]):
        res8[i,j]=pc1c2[i,j]/pc1[i]

for i in range(0,pc1c2.shape[1]):
    for j in range(0,pc1c2.shape[0]):
        res9[i,j]=pc1c2[j,i]/pc2[i]

for i in range(0,pc1c2b1.shape[0]):
    for j in range(0,pc1c2b1.shape[1]):
        for k in range(0,pc1c2b1.shape[2]):
            res6[i,j,k]=pc1c2b1[i,j,k]/pb1[i]

for i in range(0,pc1c2b1.shape[0]):
    for j in range(0,pc1c2b1.shape[1]):
        for k in range(0,pc1c2b1.shape[2]):
            res10[i,j,k]=pc1c2b1[i,j,k]/pc1b1[i,j]
        

print "Check if C2 and C1 are independent (P(C2|C1)=P(C2) and P(C1|C2)=P(C1)): \n\n"

print "Probabilites fo C2: \n"
print pc2.__str__()+"\n\n"

print "Probabilites fo C2|C1: \n"
print res8.__str__()+"\n\n"

print "We can see that they are not independent since the probability tables are different\n\n"

print "Check if C2,C1 are conditionally independent given B1: \n\n"
print "Now we compute the probability of C2|B1,C1: \n\n"
print res10.__str__()+"\n\n"
print "We can see that once we specify an idex for B1. The probabilities are the same regardless of which C1 event occurs so C2,C1 are conditionally independent given B1"
