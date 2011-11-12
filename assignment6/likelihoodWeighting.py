#Author: Ernesto Rodriguez
#
#Title: Likelyhood Weighting
#
#Queries the given bayesian network using the 
#Likelyhood Weighting probabilistic algorithm.

import graph_tool.all as gt
import graph_tool.topology as t
import numpy
from numpy import zeros
import jbn
import xml.dom.minidom as xd # part of Python standard lib
import random

def reverse(arry):

    o=zeros(arry.shape[0],numpy.int32)
    
    for i in range(0,arry.shape[0]):
        o[i]=arry[arry.shape[0]-i-1];

    return o;

def randomSample(cpt):

    p=random.random()
    c=0
    
    for i in range(0,cpt.shape[0]):
       c=c+cpt[i]
       
       if c>=p:
           return i

def likehoodWeightingHelper(bn,x,ev,n):

    w={}

    for i in x:
        w[i]=[]
        for j in range(0,len(bn.graph.vertex_properties["rv"][i].values)):
            w[i].append(0)

    for i in range(0,n):
        s=weightedSample(bn,ev)
        for k,v in w.items():            
            w[k][s[0][k]]=w[k][s[0][k]]+s[1]


    t={}
    for k,v in w.items():
        t[k]=[]
        for i in range(0,len(v)):
            t[k].append(float(v[i])/sum(v))
    
    return (t,w)

def vertexMap(bn):
    
    m={}

    for i in bn.graph.vertices():
        m[bn.graph.vertex_properties['rv'][i].name.__str__()]=i

    return m

def mapNames(bn,m):

    ret={}
    ver=vertexMap(bn)

    for k,v in m.items():
        try:
            ret[ver[k]]=v
        except KeyError:
            0

    return ret
        

def likehoodWeighting(bn,x,ev,n):

    print 'The query is being executed, note that '+n.__str__()+' samples are being generated so please be patient.\n\n'
    #tmp= jbn.JBN()
    #tmp.graph=prunBN(bn,[vertexMap(bn)[x]])
    query=[]
    vertices=vertexMap(bn)
    for i in x:
        query.append(vertices[i])

    r=likehoodWeightingHelper(bn,query,mapNames(bn,ev),n)
    res={}

    for k,v in r[0].items():
        res[k]=v

    return res
        

#prunBN(bn,[bn.graph.vertex(5)])
def prunBN(bn,x):

    tmp=bn.graph.copy()
    prunningIncomplete=True
    props=map(lambda n:bn.graph.vertex_properties['rv'][n].name.__str__(),x)

    while(prunningIncomplete):
        prunningIncomplete=False
        for v in tmp.vertices():
            if v.out_degree()<1 and not((tmp.vertex_properties['rv'][v].name.__str__() in props)):
                #print(tmp.vertex_properties['rv'][v])
                #print(bn.graph.vertex_properties['rv'][x[0]])
                #print props
                tmp.remove_vertex(v)
                prunningIncomplete=True
                break

    return tmp
                

def weightedSample(bn,ev):

    w=1
    to=reverse(t.topological_sort(bn.graph))
    s={}

    for k,v in ev.items():
        s[k]=v

    for i in to:
        
        try:
            ev[bn.graph.vertex(i)] #Test if it's an evidence node

            cpt=bn.graph.vertex_properties["rv"][bn.graph.vertex(i)].cpt

            #print "\n\n*****************\nEvidence Edge: "+bn.graph.vertex_properties["rv"][bn.graph.vertex(i)].__str__()+" ("+i.__str__()+"):\n\n"

            for e in bn.graph.vertex(i).in_edges():
                cpt=cpt[s[e.source()]]
                #print "Parent Node: "+bn.graph.vertex_properties['rv'][e.source()].__str__()+" | value: "+s[e.source()].__str__()+"\n"

            #print "\nResulting CPT: \n"+cpt.__str__()+"\n\n"
            #print "Evidence value: "+ev[bn.graph.vertex(i)].__str__()+", Probability: "+cpt[ev[bn.graph.vertex(i)]].__str__()
            w=w*cpt[ev[bn.graph.vertex(i)]]

        except KeyError:
            

            #print "\n\n****************\n\nNon-Evidence Node: "+bn.graph.vertex_properties['rv'][bn.graph.vertex(i)].__str__()+" ("+i.__str__()+"):\n\n"
            
            cpt=bn.graph.vertex_properties["rv"][bn.graph.vertex(i)].cpt

            for e in bn.graph.vertex(i).in_edges():
                cpt=cpt[s[e.source()]]
                #print "Parent Node: "+bn.graph.vertex_properties['rv'][e.source()].__str__()+" | value: "+s[e.source()].__str__()+"\n"

                

            #print "The cpt table: \n\n"+cpt.__str__()+"\n\n"
            smpl=randomSample(cpt)
            #print "\n\nThe `chosen one` is: "+smpl.__str__()+"\n\n"
            s[bn.graph.vertex(i)]=smpl
            
    return (s,w)
            

def printResults(r,e,bn):
    print("\n=========================================================\n"+
          "Query Results\n"+
          "==========================================================")
    print("Evidence Random Variables\n"+
          "-----------------------------")

    vertices=vertexMap(bn)
    for k,v in e.items():
        print(k+" = "+bn.graph.vertex_properties['rv'][vertices[k]].values[v])

    print("\n-----------------------------\n"+
          "Results:"+
          "\n-----------------------------")
    
    for k,v in r.items():
        output=bn.graph.vertex_properties['rv'][k].name.__str__()+" | "
        for i in range(0,len(v)):
            output=output+"P("+bn.graph.vertex_properties['rv'][k].values[i]+")="+v[i].__str__()+", "

        print(output)
    
if __name__== '__main__': 

    dom = xd.parse("alarm.xmlbif")
    bn= jbn.JBN()
    bn.load(dom)

    for i in range(0,5):
        #evidence={'CVP':1,'PCWP':2,'HISTORY':1,'TPR':0,'BP':2,'CO':1,'HRBP':0,'HREKG':0,'PAP':2,'SAO2':0,'FIO2':1,'PRESS':3,'EXPCO2':1,'MINVOL':0,'MINVOLSET':1}
        ev=['CVP','PCWP','HISTORY','TPR','BP','CO','HRBP','HREKG','PAP','SAO2','FIO2','PRESS','EXPCO2','MINVOL','MINVOLSET']
        vertices=vertexMap(bn)
        evidence={}
        
        for e in ev:
            evidence[e]=random.randrange(0,len(bn.graph.vertex_properties['rv'][vertices[e]].values))

        x=['LVFAILURE','HYPOVOLEMIA','ANAPHYLAXIS','INSUFFANESTH','PULMEMBOLUS','INTUBATION','KINKEDTUBE','DISCONNECT']
        n=20000
    
        r=likehoodWeighting(bn,x,evidence,n)

        printResults(r,evidence,bn)
        print "\n\n"
