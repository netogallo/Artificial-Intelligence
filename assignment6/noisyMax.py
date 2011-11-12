from itertools import product
from numpy import ndarray
from numpy import zeros

#x1=AppData
#x2=PrtDriver
#x3=PrtMem
#x4=NtwrkCnfg

#	(0, 0, 0, 0): 1, 0;
#	(1, 0, 0, 0): 0.3, 0.7;
#	(0, 1, 0, 0): 0.4, 0.6;
#	(0, 0, 1, 0): 0.2, 0.8;
#	(0, 0, 0, 1): 0.4, 0.6;


c1=[[1,0.3],[0,0.7]]
c2=[[1,0.4],[0,0.6]]
c3=[[1,0.2],[0,0.8]]
c4=[[1,0.4],[0,0.6]]

p=[c1,c2,c3,c4]

def C(y,x,cx):

    sum=0
    for i in range(0,y+1):
        sum=sum+cx[i][x]

    return sum

def Q(y,xi):
    
    mul=1
    for i in range(0,len(xi)):
        mul=mul*C(y,xi[i],p[i])

    return mul


def CPT():

    cpt=zeros(shape=(2,2,2,2,2)) #P(Y=y | X1=x1,X2=x2,X3=x3,X4=x4)=cpt[y,x1,x2,x3,x4]

    for x in product([0,1],repeat=4):
        cpt[0][x]=Q(0,x)
        cpt[1][x]=Q(1,x)-Q(0,x)

        print('-----------------------------------------------\n'+
              'AppData='+x[0].__str__()+' | PrtDriver='+x[1].__str__()+
              ' | PrtMem='+x[2].__str__()+' | NtwrkCnfg='+x[3].__str__()+
              ' || '+'P(NtGrbld=0)='+cpt[0][x].__str__()+'| P(NtGrbld=1)='
              +cpt[1][x].__str__())
        

    return cpt

if __name__== '__main__': 
    
    CPT()
