import matplotlib.pyplot as plt
from IPython.display import clear_output
from CreateModel import CreateModel
from CreateNetwork import CreateNetwork
from Leach_Protocol import Leach_Protocol
from Direct_Protocol import Direct_Protocol
from ShowNetworks import ShowNetworks
import os

clear_output()
os.system('clear')

# Define M
Model = CreateModel()
Network = CreateNetwork(Model)
Leach_Result = Leach_Protocol(Model, Network)
Direct_Result = Direct_Protocol(Model, Network)

# Show M
# Show Dead
plt.subplot(2, 1, 1)
plt.title('Died Dead')
plt.plot(Leach_Result['Dead']['All'])
plt.plot(Direct_Result['Dead']['All'])
plt.legend(['Leach', 'Direct'])
plt.subplot(2, 1, 2)
plt.title('All packet sent')
plt.plot(Leach_Result['Packet'])
plt.plot(Direct_Result['Packet'])
plt.legend(['Leach', 'Direct'])
ShowNetworks(Leach_Result['Networks'], Direct_Result['Networks'])
