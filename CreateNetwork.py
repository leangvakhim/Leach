import numpy as np
from CalcDistance import CalcDistance

def CreateNetwork(Model):
    # Node Structure
    Node = {}
    Node['X'] = []
    Node['Y'] = []
    Node['G'] = 0
    Node['Energy'] = []
    Node['IsAdvance'] = []
    Node['IsCluster'] = 0
    Node['Distance'] = []
    Node['cl'] = []
    Node['ClusterIndex'] = []
    # Create Network
    Condition = Model['P'] * Model['NodeNumber'] + 1
    Network = np.tile(Node, (Model['NodeNumber']+1, 1))
    Network[-1]['X'] = Model['Sink']['X']
    Network[-1]['Y'] = Model['Sink']['Y']
    Network[-1].Energy = np.inf
    for i in range(Model['NodeNumber']):
        Network[i]['X'] = np.random.uniform(low=1, high=Model['Area']['X'])
        Network[i]['Y'] = np.random.uniform(low=1, high=Model['Area']['Y'])
        Network[i]['Distance'] = CalcDistance(Network[i], Network[-1])
        if i >= Condition:
            Network[i]['Energy'] = Model['Energy']['Joules']
            Network[i]['IsAdvance'] = 0
        else:
            Network[i]['Energy'] = (Model['Energy']['Joules']) * (1 + Model['Alpha'])
            Network[i]['IsAdvance'] = 1
    
    return Network