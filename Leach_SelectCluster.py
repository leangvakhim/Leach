import numpy as np
from sklearn.cluster import KMeans
import random

def Leach_SelectCluster(Model, Network):
    for node in Network[:-1]:
        node['IsCluster'] = 0
    
    AliveIndices = [i for i, node in enumerate(Network[:-1]) if node['Energy'] > 0]
    
    if not AliveIndices:
        return Network

    AliveNodes = [Network[i] for i in AliveIndices]
    
    Input = np.array([[node['X'], node['Y']] for node in AliveNodes])
    
    K = min(len(AliveNodes), Model['NCluster'])
    
    if K == 0:
        return Network
        
    kmeans_model = KMeans(n_clusters=K, random_state=42, n_init=10)
    cluster_labels = kmeans_model.fit_predict(Input)
    
    for i, label in enumerate(cluster_labels):
        node_index = AliveIndices[i]
        Network[node_index]['ClusterIndex'] = label
    
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
        
        ch_node = Network[Selected_CH_index]
        if ch_node['Distance'] > Model['BaseDistance']:
            ch_node['Energy'] -= (Model['Energy']['Send_Bit'] * 4000) + (Model['Energy']['Ampli_Upper'] * 4000 * (ch_node['Distance'] ** 2))
        else:
            ch_node['Energy'] -= (Model['Energy']['Send_Bit'] * 4000) + (Model['Energy']['Ampli_Under'] * 4000 * (ch_node['Distance'] ** 2))

    return Network