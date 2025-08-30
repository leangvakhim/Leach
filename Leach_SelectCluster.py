# import numpy as np
# from sklearn.cluster import KMeans
# import random

# def Leach_SelectCluster(Model, Network):
#     Temp = [0] * len(Network)

#     for node, val in zip(Network, Temp):
#         node['IsCluster'] = val
    
#     AliveIndex = [node['Energy'] > 0 for node in Network[:-1]]
#     Alive = [i for i, is_Alive in enumerate(AliveIndex) if is_Alive]

#     Input = np.array([[node['X'], node['Y']] for node in Network[:-1]])
#     Input = Input[Alive]
#     K = min(len(Alive), Model['NCluster'])
#     kmeans_model = KMeans(n_clusters=K, random_state=42)
#     cluster_labels = kmeans_model.fit_predict(Input)
#     Temp = cluster_labels.tolist()

#     for index, label in zip(Alive, Temp):
#         Network[index]['ClusterIndex'] = label
    
#     for i in range(K):
#         Index = [idx for idx, is_Alive in enumerate(AliveIndex) if is_Alive and Network[idx]['ClusterIndex'] == i]
#         IndexG = [idx for idx in Index if Network[idx]['G'] <= 0]

#         if IndexG:
#             Selected = random.choice(IndexG)
#         else:
#             Selected = random.choice(Index)
        
#         Network[Selected]['IsCluster'] = 1
#         Network[Selected]['G'] = round(1 / Model['P']) - 1
#         if Network[Selected]['Distance'] > Model['BaseDistance']:
#             Network[Selected]['Energy'] = Network[Selected]['Energy'] - (Model['Energy']['Send_Bit'] + Model['Energy']['Aggregation_Bit'] * 4000) + Model['Energy']['Ampli_Upper'] * 4000 * (Network[Selected]['Distance'] ** 2)
#         else:
#             Network[Selected]['Energy'] = Network[Selected]['Energy'] - (Model['Energy']['Send_Bit'] + Model['Energy']['Aggregation_Bit'] * 4000) + Model['Energy']['Ampli_Under'] * 4000 * (Network[Selected]['Distance'] ** 2)

#     return Network

import numpy as np
from sklearn.cluster import KMeans
import random

def Leach_SelectCluster(Model, Network):
    # Reset IsCluster flag for all sensor nodes
    for node in Network[:-1]:
        node['IsCluster'] = 0
    
    # Get a list of indices for nodes that are still alive
    AliveIndices = [i for i, node in enumerate(Network[:-1]) if node['Energy'] > 0]
    
    # If no nodes are alive, there's nothing to do
    if not AliveIndices:
        return Network

    # Create a list of the actual alive node dictionaries
    AliveNodes = [Network[i] for i in AliveIndices]
    
    # Create the input for KMeans using correct dictionary syntax
    Input = np.array([[node['X'], node['Y']] for node in AliveNodes])
    
    # Determine the number of clusters
    K = min(len(AliveNodes), Model['NCluster'])
    
    # --- THIS IS THE FINAL FIX ---
    # If K is 0 (because all nodes are dead), we can't cluster.
    # So, we return the network as-is and end the function here for this round.
    if K == 0:
        return Network
        
    # Run the KMeans algorithm
    kmeans_model = KMeans(n_clusters=K, random_state=42, n_init=10)
    cluster_labels = kmeans_model.fit_predict(Input)
    
    # Assign cluster indices back to the nodes
    for i, label in enumerate(cluster_labels):
        node_index = AliveIndices[i]
        Network[node_index]['ClusterIndex'] = label
    
    # --- Elect Cluster Heads within each cluster ---
    for i in range(K):
        cluster_members_indices = [
            idx for idx in AliveIndices if Network[idx].get('ClusterIndex') == i
        ]
        
        if not cluster_members_indices:
            continue

        eligible_for_ch = [idx for idx in cluster_members_indices if Network[idx]['G'] <= 0]
        
        if eligible_for_ch:
            Selected_CH_index = random.choice(eligible_for_ch)
        else:
            Selected_CH_index = random.choice(cluster_members_indices)
        
        Network[Selected_CH_index]['IsCluster'] = 1
        Network[Selected_CH_index]['G'] = round(1 / Model['P']) - 1
        
        # Reduce energy of the new Cluster Head
        ch_node = Network[Selected_CH_index]
        if ch_node['Distance'] > Model['BaseDistance']:
            ch_node['Energy'] -= (Model['Energy']['Send_Bit'] * 4000) + (Model['Energy']['Ampli_Upper'] * 4000 * (ch_node['Distance'] ** 2))
        else:
            ch_node['Energy'] -= (Model['Energy']['Send_Bit'] * 4000) + (Model['Energy']['Ampli_Under'] * 4000 * (ch_node['Distance'] ** 2))

    return Network