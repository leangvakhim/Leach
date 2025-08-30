import numpy as np
from DeadCounter import DeadCounter
from Direct_UsedEnergy import Direct_UsedEnergy

def Direct_Protocol(Model, Network):
    Packet = {}
    Dead = {}
    Iteration = Model['Iteration']
    Packet['ToBS'] = np.zeros((Iteration, 1))
    Dead['All'] = np.zeros((Iteration, 1))
    Dead['Normal'] = np.zeros((Iteration, 1))
    Dead['Advance'] = np.zeros((Iteration, 1))

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
        Network = Direct_UsedEnergy(Model, Network)
        Packet['ToBS'][i] = Model['NodeNumber'] - Dead['All'][i]
    # Result
    Result = {}
    Result['Dead'] = Dead
    Result['Networks'] = Networks
    Result['Packet'] = np.cumsum(Packet['ToBS'])
    Dead['All'][Dead['All'] == 0] = np.inf
    Location = np.argmin(Dead['All'])
    Result['FirstDead'] = Location

    return Result