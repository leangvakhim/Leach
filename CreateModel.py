def CreateModel():
    Model = {}
    Model['Area'] = {
        'X': 300,
        'Y': 300
    }

    Model['Iteration'] = 1000
    Model['NodeNumber'] = 200
    Model['PHeadCluster'] = 0.1
    Model['P'] = 0.1
    Model['Alpha'] = 1
    Model['SaveIteration'] = 100
    Model['NCluster'] = 17

    Model['Sink'] = {
        'X': Model['Area']['X'] / 2,
        'Y': Model['Area']['Y'] / 2
    }

    # Energy Model
    Energy = {
        'Joules': 0.5,
        'Send_Bit': 50**-9,
        'Receive_Bit': 50**-9,
        'Aggregation_Bit': 5**-9,
        'Ampli_Upper': 1**-11,
        'Ampli_Under': 13**-16
    }

    Model['Energy'] = Energy
    Model['BaseDistance'] = (Energy['Ampli_Upper'] / Energy['Ampli_Under']) ** 0.5

    return Model