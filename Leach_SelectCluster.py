import numpy as np
from sklearn.cluster import KMeans
import random

def Leach_SelectCluster(Model, Network):
    Temp = [0] * len(Network)

    for node, val in zip(Network, Temp):
        node['IsCluster'] = val
    
    AliveIndex = [node['Energy'] > 0 for node in Network[:-1]]
    Alive = [i for i, is_Alive in enumerate(AliveIndex) if is_Alive]

    Input = np.array([[node.X, node.Y] for node in Network[:-1]])
    Input = Input[Alive]
    K = min(len(Alive), Model['NCluster'])
    kmeans_model = KMeans(n_clusters=K, random_state=42)
    cluster_labels = kmeans_model.fit_predict(Input)
    Temp = cluster_labels.tolist()

    for index, label in zip(Alive, Temp):
        Network[index]['ClusterIndex'] = label
    
    for i in range(K):
        Index = [idx for idx, is_Alive in enumerate(AliveIndex) if is_Alive and Network[idx]['ClusterIndex'] == i]
        IndexG = [idx for idx in Index if Network[idx]['G'] <= 0]

        if IndexG:
            Selected = random.choice(IndexG)
        else:
            Selected = random.choice(Index)
        
        Network[Selected]['IsCluster'] = 1
        Network[Selected]['G'] = round(1 / Model['P']) - 1
        if Network[Selected]['Distance'] > Model['BaseDistance']:
            Network[Selected]['Energy'] = Network[Selected]['Energy'] - (Model['Energy']['Send_Bit'] + Model['Energy']['Aggregation_Bit'] * 4000) + Model['Energy']['Ampli_Upper'] * 4000 * (Network[Selected]['Distance'] ** 2)
        else:
            Network[Selected]['Energy'] = Network[Selected]['Energy'] - (Model['Energy']['Send_Bit'] + Model['Energy']['Aggregation_Bit'] * 4000) + Model['Energy']['Ampli_Under'] * 4000 * (Network[Selected]['Distance'] ** 2)

    return Network