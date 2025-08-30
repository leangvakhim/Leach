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
    # Main Loop
    for i in range(Iteration):
        print(f"It = {i}")
        if (i - 1) % Model['SaveIteration'] == 0:
            Networks.append(Network)
        if (i - 1) % np.round(1 / Model['P']) == 0:
            Temp = [0] * len(Network)
            for node, val in zip(Network, Temp):
                node['G'] = val
                node['cl'] = val
        Dead['Normal'][i], Dead['Advance'][i] = DeadCounter(Network)
        Dead['All'][i] = Dead['Normal'][i] + Dead['Advance'][i]
        Network = Leach_SelectCluster(Model, Network)
        HeadClusters[i] = sum(Network['IsCluster'])
        Packet['ToBS'][i] = HeadClusters[i]

        NotCluster = Model['NodeNumber'] - Dead['All'][i] - HeadClusters[i]
        if NotCluster > 0:
            Network = Leach_UsedEnergy(Model, Network)
            Packet['ToCH'][i] = NotCluster
    # Result
    Result = {}
    Result['Dead'] = Dead
    Result['Networks'] = Networks
    Result['Packet'] = np.cumsum(Packet['ToBS'] + Packet['ToCH'])
    Dead['All'][Dead['All'] == 0] = np.inf
    Location = np.argmin(Dead['All'])
    Result['FirstDead'] = Location

    return Result