# import numpy as np
# from CalcDistance import CalcDistance


# def Leach_UsedEnergy(Model, Network):
#     Normal_Index = [i for i, node in enumerate(Network[:-2]) if not node['IsCluster'] and node['Energy'] > 0]
#     Cluster_Index = [i for i, node in enumerate(Network[:-2]) if node['IsCluster']]
#     for i in range(len(Normal_Index)):
#         Distances = np.zeros(len(Cluster_Index))
#         Counter = 1
#         for j in range(len(Cluster_Index)):
#             Distances['Counter'] = CalcDistance(Network[i], Network[j])
#             Counter += 1
#         Distance = Distances.min()
#         MinIndex = Distances.argmin()

#         if Network[i][Distance] > Distances:
#             if Distance > Model['BaseDistance']:
#                 Network[i]['Energy'] = Network[i]['Energy'] - (Model['Energy']['Send_Bit'] * 4000) + Model['Energy']['Ampli_Upper'] * 4000 * (Distance ** 2)
#             else:
#                 Network[i]['Energy'] = Network[i]['Energy'] - (Model['Energy']['Send_Bit'] * 4000) + Model['Energy']['Ampli_Under'] * 4000 * (Distance ** 2)

#             # Received Data
#             Index = Cluster_Index[MinIndex]
#             Network[Index]['Energy'] = Network[Index]['Energy'] - (Model['Energy']['Receive_Bit'] + Model['Energy']['Aggregation_Bit']) * 4000
#         else:
#             if Network[i]['Distance'] > Model['BaseDistance']:
#                 Network[i]['Energy'] = Network[i]['Energy'] - (Model['Energy']['Send_Bit'] + Model['Energy']['Aggregation_Bit'] * 4000) + Model['Energy']['Ampli_Upper'] * 4000 * (Network[i]['Distance'] ** 2)
#             else:
#                 Network[i]['Energy'] = Network[i]['Energy'] - (Model['Energy']['Send_Bit'] + Model['Energy']['Aggregation_Bit'] * 4000) + Model['Energy']['Ampli_Under'] * 4000 * (Network[i]['Distance'] ** 2)

#     return Network

import numpy as np
from CalcDistance import CalcDistance

def Leach_UsedEnergy(Model, Network):
    # Get indices of non-cluster head nodes that are still alive
    Normal_Indices = [i for i, node in enumerate(Network[:-1]) if not node['IsCluster'] and node['Energy'] > 0]
    
    # Get indices of nodes that are currently cluster heads
    Cluster_Indices = [i for i, node in enumerate(Network[:-1]) if node['IsCluster']]

    # If there are no cluster heads, nodes can't send data
    if not Cluster_Indices:
        return Network

    # Loop through each normal (non-CH) node
    for i in Normal_Indices:
        # --- THIS IS THE CORRECTED PART ---
        # Calculate the distance from the current node to ALL cluster heads
        # It correctly passes the (X, Y) tuples to CalcDistance
        distances_to_chs = np.array([
            CalcDistance((Network[i]['X'], Network[i]['Y']), (Network[j]['X'], Network[j]['Y'])) 
            for j in Cluster_Indices
        ])
        
        # If there are no distances, skip to the next node
        if distances_to_chs.size == 0:
            continue
            
        # Find the minimum distance and the index of the closest cluster head
        min_dist = distances_to_chs.min()
        closest_ch_local_index = distances_to_chs.argmin()
        closest_ch_global_index = Cluster_Indices[closest_ch_local_index]

        # --- Energy reduction for the normal node sending data ---
        if min_dist > Model['BaseDistance']:
            energy_used = (Model['Energy']['Send_Bit'] * 4000) + (Model['Energy']['Ampli_Upper'] * 4000 * (min_dist ** 2))
        else:
            energy_used = (Model['Energy']['Send_Bit'] * 4000) + (Model['Energy']['Ampli_Under'] * 4000 * (min_dist ** 2))
        Network[i]['Energy'] -= energy_used
        
        # --- Energy reduction for the cluster head receiving the data ---
        # The CH also uses energy to receive and aggregate the data
        Network[closest_ch_global_index]['Energy'] -= (Model['Energy']['Receive_Bit'] + Model['Energy']['Aggregation_Bit']) * 4000

    return Network