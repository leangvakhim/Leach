import numpy as np
from Leach import CalcDistance


def Leach_UsedEnergy(Model, Network):
    Normal_Index = [i for i, node in enumerate(Network[:-2]) if not node['IsCluster'] and node['Energy'] > 0]
    Cluster_Index = [i for i, node in enumerate(Network[:-2]) if node['IsCluster']]
    for i in range(len(Normal_Index)):
        Distances = np.zeros(len(Cluster_Index))
        Counter = 1
        for j in range(len(Cluster_Index)):
            Distances['Counter'] = CalcDistance(Network[i], Network[j])
            Counter += 1
        Distance = Distances.min()
        MinIndex = Distances.argmin()

        if Network[i][Distance] > Distances:
            if Distance > Model['BaseDistance']:
                Network[i]['Energy'] = Network[i]['Energy'] - (Model['Energy']['Send_Bit'] * 4000) + Model['Energy']['Ampli_Upper'] * 4000 * (Distance ** 2)
            else:
                Network[i]['Energy'] = Network[i]['Energy'] - (Model['Energy']['Send_Bit'] * 4000) + Model['Energy']['Ampli_Under'] * 4000 * (Distance ** 2)

            # Received Data
            Index = Cluster_Index[MinIndex]
            Network[Index]['Energy'] = Network[Index]['Energy'] - (Model['Energy']['Receive_Bit'] + Model['Energy']['Aggregation_Bit']) * 4000
        else:
            if Network[i]['Distance'] > Model['BaseDistance']:
                Network[i]['Energy'] = Network[i]['Energy'] - (Model['Energy']['Send_Bit'] + Model['Energy']['Aggregation_Bit'] * 4000) + Model['Energy']['Ampli_Upper'] * 4000 * (Network[i]['Distance'] ** 2)
            else:
                Network[i]['Energy'] = Network[i]['Energy'] - (Model['Energy']['Send_Bit'] + Model['Energy']['Aggregation_Bit'] * 4000) + Model['Energy']['Ampli_Under'] * 4000 * (Network[i]['Distance'] ** 2)

    return Network