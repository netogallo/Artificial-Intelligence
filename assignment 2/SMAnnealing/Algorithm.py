import random
import math

maxTime=500
maxTest=50

def smAnnealing(tuples):

    best=tuples[:]
    T=initialTemp(tuples) #Calculate the initial temperature

    for k in range(1,maxTime):

        test=split(best)
        best=[]
        t=schedule(k,T)
        #numItem=int(len(test)*(random.random()-0.01))
        #item=test[numItem][:] #select a random sublist, the sublists become smaller as t increases
        #random.shuffle(item)

        for slist in test:
        #dtem=cost(seg[1])-cost(seg[0])

            item=slist[:]
            random.shuffle(item)
            
            #if(i==numItem):                
            dtem=cost(item)-cost(slist)
                            
            if(dtem<=0):
                best=best+item
            else:
                if random.random()<(probability(dtem,t)):
                    best=best+item
                        #print (probability(dtem,t),t,dtem,"yes")
                else:
                    best=best+slist
                        #print (probability(dtem,t),t,dtem,"no")
    return best          

def split(tuples):

    #cuts=(int(num*10/(maxTime+1)))+1
    cuts=int(6*(random.random()-0.01))+1
    step=(len(tuples)/cuts)+1

    ret=[]

    for i in range(0,len(tuples),step):
        #item=(tuples[i:i+step],tuples[i:i+step])
        #random.shuffle(item[1])
        #ret.append(item)
        ret.append(tuples[i:i+step])

    return ret

def schedule(k,T):

    #return T/(5*(k*(0.4/maxTime)+0.2))
    return float(T)*((1/((k*(float(9)/float(maxTime))+1)))-0.1)
    

def initialTemp(tuples):

    big=0
    sample=tuples[:]

    for i in range(1,maxTest):

        random.shuffle(sample)
        k=abs(cost(tuples)-cost(sample))
              
        if big<k:
            big=k

    print "High temp: "+(big).__str__()
    return (big*2)
        
def probability(dtemp,temp):

    return (math.e**(-dtemp/temp))/2

def cost(tuples):

    k=0

    for i in range(0,len(tuples)):

        try:
            k=k+math.sqrt((tuples[i][0]-tuples[i+1][0])**2 + (tuples[i][1]-tuples[i+1][1])**2)
        except IndexError:
            0

    return k

def tcost(tuples):

    k=0

    for i in range(0,len(tuples)):

        try:
            k=k+math.sqrt((tuples[i][0]-tuples[i+1][0])**2 + (tuples[i][1]-tuples[i+1][1])**2)
        except IndexError:
            k=k+math.sqrt((tuples[i][0]-tuples[0][0])**2 + (tuples[i][1]-tuples[0][1])**2)

    return k
