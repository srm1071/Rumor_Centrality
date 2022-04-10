import pandas as pd
import networkx as nx
import numpy as np
from sys import exit
import matplotlib.pyplot as plt

def nodesof_subgraph():
    data1 = pd.read_csv("mutation_suraj.csv", delimiter=",")
    bar=input('please enter tumour barcode: ')

    node=[]
    barcodes=data1['Tumor_Sample_Barcode']
    nodes=data1['Hugo_Symbol']
    for i in range(len(barcodes)):
        if(barcodes[i]==bar):
            node.append(nodes[i])
    return node

def getList(dict):
    list = []
    for key in dict.keys():
        list.append(key)
          
    return list

def between(sett,sub):
    key=[]
    k=nx.betweenness_centrality(subg)
    sortd= dict(reversed(sorted(k.items(), key=lambda item: item[1])))
    key=getList(sortd)
    
    #print(key)
    return key

def NI(sett,sub):
    indeg=[0]*(max(sett)+1)
    arr=[0]*(max(sett)+1)
    for i in range(len(sett)):
        indeg[sett[i]]=sub.in_degree(sett[i])                           
    maxn = np.argsort(indeg)
    maxn=maxn[::-1]
    return maxn[0:10]

def rumor_center(g):
    list1=list(g.nodes())
    count=[0]*(max(list1)+1)
    rand=[]
    rand=between(list1,g)
    rand1=rand
    for i in range(len(rand)):
        k=rand[i]
        paths=[]
        for j in range(len(list1)):
            if ((nx.has_path(g, list1[j], k))==True):
                paths.append(list1[j])

        for m in range(len(paths)):
            count[paths[m]]=count[paths[m]]+1
    maxn=[]
    count1=sorted(count)
    maxn = np.argsort(count)
    maxn=maxn[::-1]
    C=[]
    Px=[]

    for i in range(len(maxn)):
        Px=[]
        C.append(maxn[i])
        for j in range(len(rand)):
            if ((nx.has_path(g, maxn[i], rand[j]))==True):
                Px.append(rand[j])
        rand=set(rand).difference(set(Px))
        rand=list(rand)
        if(len(rand)==0):
            return C,rand
            exit()
    return C,rand
    


node=nodesof_subgraph()  
g1 = nx.DiGraph()
data = pd.read_csv("reg_net1.csv", delimiter=",")
source=data['source_gene_id']
dest=data['desti_gene_id']
sdict=list(zip(source,data['source_entrez_id']))
ddict=list(zip(dest,data['target_entrez_id']))
set1=set(source)
set2=set(dest)
sett=list(set1.union(set2))
dsett=list(set(sdict).union(set(ddict)))

for i in range(len(sett)):
    g1.add_node(dsett[i][1])
    
for i in range(len(source)):
    g1.add_edge(sdict[i][1],ddict[i][1])

nodes=[0]*len(node)
for i in range(len(node)):
    for j in range(len(dsett)):
        if(node[i]==dsett[j][0]):
            nodes[i]=dsett[j][1]

subg = g1.subgraph(nodes)
print('total no of nodes are: ',len(list(subg.nodes())))
centers,moni=rumor_center(subg)
print("centers are: ",centers)
