import random

class PMFList:

    def __init__(self,numItems):

        self.items=[]
        pList=[]

        for i in range(0,numItems):
            
            pList.append(random.random())

        normFactor=1/sum(pList)
        count=1;

        for p in pList:            
            self.items.append(("Item "+count.__str__(),p*normFactor))
            count=count+1

    def choose(self):

        p=random.random()

        l=0

        for i in self.items:

            l=l+i[1]
            
            if p<=l:
                return i
            
