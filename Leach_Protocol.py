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

    for i in range(Iteration):
        print(f"LEACH Iteration = {i}")

        if (i > 0 and i % Model['SaveIteration'] == 0):
            Networks.append(Network)

        if (i > 0 and i % np.round(1 / Model['P']) == 0):
            for node in Network[:-1]: 
                node['G'] = 0

        Dead['Normal'][i], Dead['Advance'][i] = DeadCounter(Network)
        Dead['All'][i] = Dead['Normal'][i] + Dead['Advance'][i]
        
        Network = Leach_SelectCluster(Model, Network)

        HeadClusters[i] = sum(node['IsCluster'] for node in Network[:-1])
        Packet['ToBS'][i] = HeadClusters[i]

        NotCluster = Model['NodeNumber'] - Dead['All'][i] - HeadClusters[i]
        if NotCluster > 0:
            Network = Leach_UsedEnergy(Model, Network)
            Packet['ToCH'][i] = NotCluster
            
    Result = {}
    Result['Dead'] = Dead
    Result['Networks'] = Networks
    Result['Packet'] = np.cumsum(Packet['ToBS'] + Packet['ToCH'])
    
    dead_all_temp = np.copy(Dead['All'])
    dead_all_temp[dead_all_temp == 0] = np.inf 
    Location = np.argmin(dead_all_temp)
    Result['FirstDead'] = Location

    return Result