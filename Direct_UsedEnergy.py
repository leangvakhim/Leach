def Direct_UsedEnergy(Model, Network):
    Alive_Indices = [i for i, node in enumerate(Network[:-1]) if node['Energy'] > 0]

    for i in Alive_Indices:
        node = Network[i]
        distance = node['Distance']
        
        if distance > Model['BaseDistance']:
            energy_used = (Model['Energy']['Send_Bit'] * 4000) + (Model['Energy']['Ampli_Upper'] * 4000 * (distance ** 2))
        else:
            energy_used = (Model['Energy']['Send_Bit'] * 4000) + (Model['Energy']['Ampli_Under'] * 4000 * (distance ** 2))
        
        node['Energy'] -= energy_used

    return Network