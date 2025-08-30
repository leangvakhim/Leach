import matplotlib.pyplot as plt
import time
from Show import Show

def ShowNetworks(Nets1, Nets2):
    plt.figure()
    for i in range(len(Nets1)):
        plt.clf()
        plt.subplot(1, 2, 1)
        plt.title(['Leach', ' It : ', i])
        Show(Nets1[:, i])
        plt.subplot(1, 2, 2)
        plt.title(['Direct', ' It : ', i])
        Show(Nets2[:, i])
        time.sleep(0.001)
    plt.show()
    return None