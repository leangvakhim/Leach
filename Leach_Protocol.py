# import numpy as np
# from DeadCounter import DeadCounter
# from Leach_SelectCluster import Leach_SelectCluster
# from Leach_UsedEnergy import Leach_UsedEnergy

# def Leach_Protocol(Model, Network):
#     Iteration = Model['Iteration']
#     Packet = {
#         'ToCH' : np.zeros((Iteration, 1)),
#         'ToBS' : np.zeros((Iteration, 1))
#     }
#     Dead = {
#         'All' : np.zeros((Iteration, 1)),
#         'Normal' : np.zeros((Iteration, 1)),
#         'Advance' : np.zeros((Iteration, 1))
#     }
#     HeadClusters = np.zeros((Iteration, 1))
#     Networks = []
#     # Main Loop
#     for i in range(Iteration):
#         print(f"It = {i}")
#         if (i - 1) % Model['SaveIteration'] == 0:
#             Networks.append(Network)
#         if (i - 1) % np.round(1 / Model['P']) == 0:
#             Temp = [0] * len(Network)
#             for node, val in zip(Network, Temp):
#                 node['G'] = val
#                 node['cl'] = val
#         Dead['Normal'][i], Dead['Advance'][i] = DeadCounter(Network)
#         Dead['All'][i] = Dead['Normal'][i] + Dead['Advance'][i]
#         Network = Leach_SelectCluster(Model, Network)
#         HeadClusters[i] = sum(Network['IsCluster'])
#         Packet['ToBS'][i] = HeadClusters[i]

#         NotCluster = Model['NodeNumber'] - Dead['All'][i] - HeadClusters[i]
#         if NotCluster > 0:
#             Network = Leach_UsedEnergy(Model, Network)
#             Packet['ToCH'][i] = NotCluster
#     # Result
#     Result = {}
#     Result['Dead'] = Dead
#     Result['Networks'] = Networks
#     Result['Packet'] = np.cumsum(Packet['ToBS'] + Packet['ToCH'])
#     Dead['All'][Dead['All'] == 0] = np.inf
#     Location = np.argmin(Dead['All'])
#     Result['FirstDead'] = Location

#     return Result

import numpy as np
from DeadCounter import DeadCounter
from Leach_SelectCluster import Leach_SelectCluster
from Leach_UsedEnergy import Leach_UsedEnergy

def Leach_Protocol(Model, Network):
    Iteration = Model['Iteration']
    Packet = {
        'ToCH' : np.zeros((Iteration, 1)),
        'ToBS' : np.zeros((Iteration, 1))
    }
    Dead = {
        'All' : np.zeros((Iteration, 1)),
        'Normal' : np.zeros((Iteration, 1)),
        'Advance' : np.zeros((Iteration, 1))
    }
    HeadClusters = np.zeros((Iteration, 1))
    Networks = []

    # Main Simulation Loop
    for i in range(Iteration):
        print(f"LEACH Iteration = {i}")

        if (i > 0 and i % Model['SaveIteration'] == 0):
            Networks.append(Network)

        # Reset cluster eligibility every round for all nodes
        if (i > 0 and i % np.round(1 / Model['P']) == 0):
            for node in Network[:-1]: # Exclude sink
                node['G'] = 0

        Dead['Normal'][i], Dead['Advance'][i] = DeadCounter(Network)
        Dead['All'][i] = Dead['Normal'][i] + Dead['Advance'][i]
        
        Network = Leach_SelectCluster(Model, Network)
        
        # --- THIS IS THE CORRECTED LINE ---
        # It now correctly loops through each node in the network (excluding the sink)
        # and sums their 'IsCluster' values (which are either 1 for a CH or 0).
        HeadClusters[i] = sum(node['IsCluster'] for node in Network[:-1])
        Packet['ToBS'][i] = HeadClusters[i]

        # Calculate how many non-cluster-head nodes are alive
        NotCluster = Model['NodeNumber'] - Dead['All'][i] - HeadClusters[i]
        if NotCluster > 0:
            Network = Leach_UsedEnergy(Model, Network)
            Packet['ToCH'][i] = NotCluster
            
    # --- Prepare Final Results ---
    Result = {}
    Result['Dead'] = Dead
    Result['Networks'] = Networks
    Result['Packet'] = np.cumsum(Packet['ToBS'] + Packet['ToCH'])
    
    # Find the iteration of the first dead node
    dead_all_temp = np.copy(Dead['All'])
    dead_all_temp[dead_all_temp == 0] = np.inf # Replace 0s with infinity
    Location = np.argmin(dead_all_temp)
    Result['FirstDead'] = Location

    return Result