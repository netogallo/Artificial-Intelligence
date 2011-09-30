#PMF and Simulated Annealing Testing File
#Author: Ernesto Rodriguez
#Course: Artificial Intelligence Fall 2011 Jacobs University
#
#This program measures the occurance of items in a PMF and
#calculates the shortest path to traverse 25 points using
#simulated annealing

import unittest
import PMF
import SMAnnealing
import pickle
import gzip
from PMF.PMF import PMFList
from SMAnnealing import Algorithm 
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import time
import re

class PMFTest(unittest.TestCase):

    def testProbabilites(self):

        pmf=PMFList(10)
        count={}
        times=10000
        exp=re.compile('\d+')

        o=[]
        for i in range(0,times):
            
            sel=pmf.choose()
            o.append(int(exp.search(sel[0]).group()))

            try: 
                count[sel]=count[sel]+1
            except KeyError:
                count[sel]=1

        print("-------------------------------\n"+
              "Results table of the PMF test:\n"+
              "-------------------------------")

        for k,i in count.items():
            print("Item name: "+k[0]+" | Item probability: "+
                  k[1].__str__()+" | Ocurrences: "+i.__str__()+
                  " | Item empirical probability ("+
                  times.__str__()+" runs)"+
                  ": "+(float(i)/times).__str__())
            

        plt.hist(o)
        plt.xlabel('Item number (1-'+len(count).__str__()+')')
        plt.ylabel('Number of occurrences')
        plt.show()
        

    def testSMAnnealing(self):
        
        coords=pickle.load(gzip.open('pt_coords_list.p.gz','rb'))
        result=Algorithm.smAnnealing(coords)
        #print Algorithm.split(coords)
        print len(result)
        sum=0

        print ("The total cost of the found path is: "+Algorithm.tcost(result).__str__())

        xpath=[]
        ypath=[]
        for i in range(0,len(result)):
            
            xpath.append(result[i][0])
            ypath.append(result[i][1])

        xpath.append(result[0][0])
        ypath.append(result[0][1])

        
        plt.plot(xpath,ypath,marker='o')
        plt.plot([result[0][0],result[1][0]],[result[0][1],result[1][1]],marker='o',color='r')
        plt.plot([result[1][0]],[result[1][1]],marker='o',color='b')
        plt.title("The Found path (cost: "+Algorithm.tcost(result).__str__()+')')
        plt.show()        

if __name__ == '__main__':
    unittest.main()


                
    
