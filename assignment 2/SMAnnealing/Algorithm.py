import random
import math

minTemp=1
maxTemp=10

def smAnnealing(tuples):

    res=[]
    x=tuples[0]
    res.append((len(res)+1,x))
    tuples.remove(x)

    while(len(tuples)>0):
        
        x=selNext(x,tuples)
        res.append((len(res)+1,x))
        tuples.remove(x)

    return res

def selNext(x,domain):

    best=domain[0] #The best child

    for k in range(minTemp,maxTemp):
        
        random.shuffle(domain)
        tmp=domain[0] #select a random child

        dtmp=cost(x,best)-cost(x,tmp)

        if(dtmp<=0):
            best=tmp
        else:
            if random.random()>probability(dtmp,k):
                best=tmp

    return best
                
        
def probability(energy,time):

    return math.e**(-energy/time)

def cost(a,b):

    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
