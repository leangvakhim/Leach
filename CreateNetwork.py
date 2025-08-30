# import numpy as np
# from CalcDistance import CalcDistance

# def CreateNetwork(Model):
#     # Node Structure
#     Node = {}
#     Node['X'] = []
#     Node['Y'] = []
#     Node['G'] = 0
#     Node['Energy'] = []
#     Node['IsAdvance'] = []
#     Node['IsCluster'] = 0
#     Node['Distance'] = []
#     Node['cl'] = []
#     Node['ClusterIndex'] = []
#     # Create Network
#     Condition = Model['P'] * Model['NodeNumber'] + 1
#     Network = np.tile(Node, (Model['NodeNumber']+1, 1))
#     Network[-1]['X'] = Model['Sink']['X']
#     Network[-1]['Y'] = Model['Sink']['Y']
#     Network[-1].Energy = np.inf
#     for i in range(Model['NodeNumber']):
#         Network[i]['X'] = np.random.uniform(low=1, high=Model['Area']['X'])
#         Network[i]['Y'] = np.random.uniform(low=1, high=Model['Area']['Y'])
#         Network[i]['Distance'] = CalcDistance(Network[i], Network[-1])
#         if i >= Condition:
#             Network[i]['Energy'] = Model['Energy']['Joules']
#             Network[i]['IsAdvance'] = 0
#         else:
#             Network[i]['Energy'] = (Model['Energy']['Joules']) * (1 + Model['Alpha'])
#             Network[i]['IsAdvance'] = 1
    
#     return Network

import numpy as np
from CalcDistance import CalcDistance

def CreateNetwork(Model):
    # Create an empty list to hold all the node dictionaries
    Network = []
    
    # --- Create and configure the sensor nodes ---
    for i in range(Model['NodeNumber']):
        Node = {}
        Node['X'] = np.random.uniform(low=1, high=Model['Area']['X'])
        Node['Y'] = np.random.uniform(low=1, high=Model['Area']['Y'])
        Node['G'] = 0
        Node['IsCluster'] = 0
        Node['cl'] = []
        Node['ClusterIndex'] = -1  # Initialize with a non-valid index
        
        # Set node energy based on whether it is an "advanced" node
        if i >= (Model['P'] * Model['NodeNumber']):
            Node['Energy'] = Model['Energy']['Joules']
            Node['IsAdvance'] = 0
        else:
            Node['Energy'] = Model['Energy']['Joules'] * (1 + Model['Alpha'])
            Node['IsAdvance'] = 1
        
        # Add the newly created node to the network list
        Network.append(Node)

    # --- Create and configure the Base Station (Sink) node ---
    SinkNode = {}
    SinkNode['X'] = Model['Sink']['X']
    SinkNode['Y'] = Model['Sink']['Y']
    SinkNode['Energy'] = float('inf')  # Sink has effectively infinite energy
    
    # Add the sink to the end of the network list
    Network.append(SinkNode)

    # --- Calculate the initial distance from each node to the sink ---
    # The sink is the last element in the list, at index -1
    for i in range(Model['NodeNumber']):
        Network[i]['Distance'] = CalcDistance(
            (Network[i]['X'], Network[i]['Y']),
            (Network[-1]['X'], Network[-1]['Y'])
        )

    return Network