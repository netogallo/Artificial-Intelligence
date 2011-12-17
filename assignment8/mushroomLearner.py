#NBC Bayesian Network for Mushroom Classification
#
#Authors: Shailen Sobhee And Ernesto Rodriguez
#
#Description: Use a Naive Bayesian network to classify 
#mushrooms as poisonous or eatable. The mushroom samples
#are given in a cvs file 'training.data'. Preform
#a K-Fold validation and determine error rates.

import graph_tool.all as gt
from jbn_nbc import *
from numpy import zeros
import xml.dom.minidom as xd # part of Python standard lib

#Sample the specified data file, and Generate the 
#Probability tables of the NBC. Theese tables are
#Dirrilecht distributed.
def learnCPT(bn,ev,order,rvOrder):
    
    ret=bn.graph
    #ret = JBN()    
    #ret.graph=bn.graph.copy()
    #count=bn.graph.copy()
    #Workaround since python cant copy objects properly
    
    #Counter with the ammount of samples found for each category
    count={}

    #Clear data from the NBC
    for v in ret.vertices():        
        cpt=ret.vertex_properties['rv'][v].cpt
        ret.vertex_properties['rv'][v].cpt=copy.deepcopy(zeros(shape=cpt.shape))
        count[v]=copy.deepcopy(zeros(shape=cpt.shape))
        

    f=open(ev,'r')
    stop=0

    #Sample every line of the dataset
    for line in f:
        stop=stop+1
        if stop>100:
            #break;
            0

        #Obtain the descition (poisonous or eatable)
        descition=line.split(',')[0]

        #Increment the counter for the gien descition
        values=ret.vertex_properties['rv'][ret.vertex(0)].values
        count[ret.vertex(0)][rvOrder.index(descition)]+=1
        a=[1]*len(count[ret.vertex(0)]) 

        #Update the probability table of poisonus or eatable
        #according to Dirrilicht Distribution with alpha=1
        for k in range(0,len(ret.vertex_properties['rv'][ret.vertex(0)].cpt)):
            s=sum(count[ret.vertex(0)])+1*len(count[ret.vertex(0)])
            t=a[k]+count[ret.vertex(0)][k]
            #print count[ret.vertex(rvOrder.index(descition))]
            pn=float(t)/float(s)
            ret.vertex_properties['rv'][ret.vertex(0)].cpt[k]=pn

        #Obtain the attributes of the sample
        attributes=line.replace('\n','').split(',')[1:]

        #Update probability tables and counters for each attribute
        for i in range(0,len(attributes)):
        
        #Update the cpt of the BN given the observed evidence of a given attribute
            if(attributes[i]!='?'):
                
                #Update the counter for that particular attribute and desition
                values=ret.vertex_properties['rv'][ret.vertex(order[i])].values
                count[ret.vertex(order[i])][rvOrder.index(descition)][values.index(attributes[i])]+=1

                #alpha=1 for all attributes
                a=[1]*len(count[ret.vertex(order[i])][rvOrder.index(descition)]) 
                
                #Update probability tables according to the Dirrilecht distribution
                #with alpha=1 for all attributes. The updated table is the table corresponding
                #to the node of the attribute currently being analyzed and the desition of
                #this particular sample (eatable or poisonous)
                for k in range(0,len(ret.vertex_properties['rv'][ret.vertex(order[i])].cpt)):
                    s=sum(count[ret.vertex(order[i])][k])+1*len(count[ret.vertex(order[i])][k])
                    for j in range(0,len(ret.vertex_properties['rv'][ret.vertex(order[i])].cpt[k])):
                        t=a[j]+count[ret.vertex(order[i])][k][j]
                        pn=float(t)/float(s)
                        ret.vertex_properties['rv'][ret.vertex(order[i])].cpt[k][j]=pn

    f.close()

    return bn,count
    
#Partition the Samples into a training set and a 
#test set (they are placed in separate files)
def partition(i,k,sample):
    
    tn='training.data'
    vl='validation.data'

    f=open(sample,'r')
    t=open(tn,'w')
    v=open(vl,'w')
    j=i

    for line in f:
        if j<k:
            j=j+1
            v.write(line)
        else:
            t.write(line)
            j=0

    f.close()
    t.close()
    v.close()

    return (tn,vl)

#Test the bayesian network in a particular
#validation set, calculate the errors
#and error rate.
def validateBN(bn,vSet,evOrder,rvOrder):

    n=0
    e=0
    dict_e_names_values= Evidence(bn.graph)
    dict_q_names_factor= {}
    dict_q_names_factor["decision"]= None
    
    f=open(vSet,'r')

    for line in f:
        n=n+1

        if n>100:
            #break;
            0

        dict_e_names_values.sampleLine(line,evOrder)
        dict_q_names_rv= bn.posteriorQuery(dict_q_names_factor, dict_e_names_values)
    
        #print "\n*** The final PMFs for the query RVs for the evidence are: (SORTED by decreasing likelihood)"
        sorted_q_dict = sorted(dict_q_names_factor.iteritems(), key=lambda t: t[1].table[0], reverse=True)
        for (q_name, q_factor) in sorted_q_dict:
            #print line.split(',')[0]
            if q_factor.table[rvOrder.index(line.split(',')[0])] <= 0.50:
                e+=1
            #for ix in range(len(q_factor.table)):
                #sys.stdout.write('\t P(%s=%s | evidence)=%f\n' % (q_name, dict_q_names_rv[q_name].values[ix], q_factor.table[ix]))                
                

    f.close()

    return e,n
    
#Split the samples into a training set and a test set, train
#the BN with the training set and test it with the validation
#set. Determine error rate and number of errors.
def kFoldCrossValidation(bn,k,samples,sOrder,evOrder,rvOrder):
    
    for i in range(0,k):
        
        t,v=partition(i,k,samples)

        b=learnCPT(bn,t,sOrder,rvOrder)

        e=validateBN(bn,v,evOrder,rvOrder)

        print("=============================================\n"+
              "K-Fold Validation iteration: "+(i+1).__str__()+
              "\n=============================================\n");
        

        print ("Errors encountered during classification: "
               +e[0].__str__()+" | Total Ammount of Samples: "
               +e[1].__str__()+" | Error rate: "
               +(float(e[0])/e[1]).__str__()+"\n")

        print("=============================================")

    
if __name__== '__main__': 
    #Order of nodes according to the order of the attributes in the sample
    sOrder=[15,18,17,11,1,20,14,9,3,21,13,5,6,7,8,22,19,16,4,2,10,12]
    rvOrder=['p','e']
    bn=JBN()
    dom = xd.parse("nbc_mushroom.xmlbif")
    bn.load(dom)
    samples='agaricus-lepiota.data'
    #bn2=learnCPT(bn,file,order,orderRv)

    evOrder=[None,"cap-shape","cap-surface","cap-color","bruises","odor","gill-attachment","gill-spacing","gill-size","gill-color","stalk-shape","stalk-root","stalk-surface-above-ring","stalk-surface-below-ring","stalk-color-above-ring","stalk-color-below-ring",None,"veil-color","ring-number","ring-type","spore-print-color","population","habitat"]

    kFoldCrossValidation(bn,5,samples,sOrder,evOrder,rvOrder)
    res=learnCPT(bn,samples,sOrder,rvOrder)
