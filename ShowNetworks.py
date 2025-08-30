# import matplotlib.pyplot as plt
# import time
# from Show import Show

# def ShowNetworks(Nets1, Nets2):
#     plt.figure()
#     for i in range(len(Nets1)):
#         plt.clf()
#         plt.subplot(1, 2, 1)
#         plt.title(['Leach', ' It : ', i])
#         Show(Nets1[:, i])
#         plt.subplot(1, 2, 2)
#         plt.title(['Direct', ' It : ', i])
#         Show(Nets2[:, i])
#         time.sleep(0.001)
#     plt.show()
#     return None
import matplotlib.pyplot as plt
import time
from Show import Show

def ShowNetworks(Nets1, Nets2):
    plt.figure(figsize=(12, 6))
    
    # Loop through each saved network snapshot
    for i in range(len(Nets1)):
        plt.clf() # Clear the figure for the new animation frame
        
        # --- THIS IS THE CORRECTED PART ---
        # We now use simple list indexing 'Nets1[i]' and 'Nets2[i]'
        
        # Display the LEACH network
        plt.subplot(1, 2, 1)
        # Calculate the round number based on the save interval
        round_num = (i + 1) * 100 
        plt.title(f'LEACH Network at round {round_num}')
        Show(Nets1[i])
        
        # Display the Direct network
        plt.subplot(1, 2, 2)
        plt.title(f'Direct Network at round {round_num}')
        Show(Nets2[i])
        
        plt.tight_layout()
        plt.pause(0.1) # Pause briefly to create the animation effect
        
    plt.show() # Show the final state