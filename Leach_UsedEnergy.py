import numpy as np
from CalcDistance import CalcDistance

def Leach_UsedEnergy(Model, Network):
    Normal_Indices = [i for i, node in enumerate(Network[:-1]) if not node['IsCluster'] and node['Energy'] > 0]
    
    Cluster_Indices = [i for i, node in enumerate(Network[:-1]) if node['IsCluster']]

    if not Cluster_Indices:
        return Network

    for i in Normal_Indices:
        distances_to_chs = np.array([
            CalcDistance((Network[i]['X'], Network[i]['Y']), (Network[j]['X'], Network[j]['Y'])) 
            for j in Cluster_Indices
        ])
        
        if distances_to_chs.size == 0:
            continue
            
        min_dist = distances_to_chs.min()
        closest_ch_local_index = distances_to_chs.argmin()
        closest_ch_global_index = Cluster_Indices[closest_ch_local_index]

        if min_dist > Model['BaseDistance']:
            energy_used = (Model['Energy']['Send_Bit'] * 4000) + (Model['Energy']['Ampli_Upper'] * 4000 * (min_dist ** 2))
        else:
            energy_used = (Model['Energy']['Send_Bit'] * 4000) + (Model['Energy']['Ampli_Under'] * 4000 * (min_dist ** 2))
        Network[i]['Energy'] -= energy_used
        
        Network[closest_ch_global_index]['Energy'] -= (Model['Energy']['Receive_Bit'] + Model['Energy']['Aggregation_Bit']) * 4000

    return Network