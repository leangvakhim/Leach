import numpy as np
from CalcDistance import CalcDistance

def CreateNetwork(Model):
    Network = []
    
    for i in range(Model['NodeNumber']):
        Node = {}
        Node['X'] = np.random.uniform(low=1, high=Model['Area']['X'])
        Node['Y'] = np.random.uniform(low=1, high=Model['Area']['Y'])
        Node['G'] = 0
        Node['IsCluster'] = 0
        Node['cl'] = []
        Node['ClusterIndex'] = -1  
        
        if i >= (Model['P'] * Model['NodeNumber']):
            Node['Energy'] = Model['Energy']['Joules']
            Node['IsAdvance'] = 0
        else:
            Node['Energy'] = Model['Energy']['Joules'] * (1 + Model['Alpha'])
            Node['IsAdvance'] = 1
        
        Network.append(Node)

    SinkNode = {}
    SinkNode['X'] = Model['Sink']['X']
    SinkNode['Y'] = Model['Sink']['Y']
    SinkNode['Energy'] = float('inf') 
    
    Network.append(SinkNode)

    for i in range(Model['NodeNumber']):
        Network[i]['Distance'] = CalcDistance(
            (Network[i]['X'], Network[i]['Y']),
            (Network[-1]['X'], Network[-1]['Y'])
        )

    return Network