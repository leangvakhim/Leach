import matplotlib.pyplot as plt
import time
from Show import Show

def ShowNetworks(Nets1, Nets2):
    plt.figure(figsize=(12, 6))
    
    for i in range(len(Nets1)):
        plt.clf() 
                
        plt.subplot(1, 2, 1)
        round_num = (i + 1) * 100 
        plt.title(f'LEACH Network at round {round_num}')
        Show(Nets1[i])
        
        plt.subplot(1, 2, 2)
        plt.title(f'Direct Network at round {round_num}')
        Show(Nets2[i])
        
        plt.tight_layout()
        plt.pause(0.1) 
        
    plt.show() 