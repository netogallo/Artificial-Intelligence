import unittest
import PMF
import SMAnnealing
import pickle
import gzip
from PMF.PMF import PMFList
from SMAnnealing import Algorithm 


class PMFTest(unittest.TestCase):

    def testProbabilites(self):

        pmf=PMFList(10)
        count={}
        times=1000

        for i in range(0,times):
            
            sel=pmf.choose()

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

    def testSMAnnealing(self):
        
        coords=pickle.load(gzip.open('pt_coords_list.p.gz','rb'))
        print Algorithm.smAnnealing(coords)

if __name__ == '__main__':
    unittest.main()


                
    
