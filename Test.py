import matplotlib.pyplot as plt
from IPython.display import clear_output
from sklearn.cluster import KMeans
import numpy as np
from Leach import CreateModel, CreateNetwork, Leach_Protocol, Direct_Protocol, ShowNetworks
import os

clear_output()
os.system('clear')

x = np.random.uniform(1, 100, size=(100, 1))
y = np.random.uniform(1, 100, size=(100, 1))

kmeans_model = KMeans(n_clusters=5, random_state=42)
A = kmeans_model.fit_predict(np.concatenate((x, y), axis=1))

