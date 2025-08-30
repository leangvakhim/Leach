import matplotlib.pyplot as plt
from IPython.display import clear_output
from sklearn.cluster import KMeans
import numpy as np
import os

clear_output()
os.system('clear')

x = np.random.uniform(1, 100, size=(100, 1))
y = np.random.uniform(1, 100, size=(100, 1))

kmeans_model = KMeans(n_clusters=5, random_state=42)
A = kmeans_model.fit_predict(np.concatenate((x, y), axis=1))

plt.plot(x[A == 0], y[A == 0], marker='s', color=(0.7, 0, 0))
plt.plot(x[A == 1], y[A == 1], marker='s', color=(1, 0, 0))
plt.plot(x[A == 2], y[A == 2], marker='s', color=(0, 1, 0))
plt.plot(x[A == 3], y[A == 3], marker='s', color=(0, 0, 1))
plt.plot(x[A == 4], y[A == 4], marker='s', color=(0.5, 0, 0.5))

plt.show()