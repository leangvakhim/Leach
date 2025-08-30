import matplotlib.pyplot as plt

def Show(Network):
    for i in range(len(Network) - 1):
        if Network[i]['Energy'] > 0:
            if Network[i]['IsCluster']:
                plt.plot(Network[i]['X'], Network[i]['Y'], marker='*', color=(0, 0, 0))
            else:
                if not Network[i]['IsAdvance']:
                    plt.plot(Network[i]['X'], Network[i]['Y'], marker='o', color=(0.3,0.7,0.9))
                else:
                    plt.plot(Network[i]['X'], Network[i]['Y'], marker='+', color=(0.6,0.3,0.9))
        else:
            plt.plot(Network[i]['X'], Network[i]['Y'], marker='.', color='red', linestyle='None', markersize=10)
    
    plt.plot(Network[-1]['X'], Network[-1]['Y'], marker='x', color=(0.5,0.5,0.5), linestyle='None', markersize=20)

    return None



