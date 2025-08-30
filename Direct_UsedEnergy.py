def Direct_UsedEnergy(Model, Network):
    Alive_Index = [i for i, node in enumerate(Network[:-2]) if node['Energy'] > 0]
    # Alive_Index = [i for i, node in enumerate(Network[:-2]) if node['Energy'] > 0]
    for i in range(Alive_Index):
        if Network[i]['Distance'] > Model['BaseDistance']:
            Network[i]['Energy'] = Network[i]['Energy'] - (Model['Energy']['Send_Bit'] + Model['Energy']['Aggregation_Bit'] * 4000) + Model['Energy']['Ampli_Upper'] * 4000 * (Network[i]['Distance'] ** 2)
        else:
            Network[i]['Energy'] = Network[i]['Energy'] - (Model['Energy']['Send_Bit'] + Model['Energy']['Aggregation_Bit'] * 4000) + Model['Energy']['Ampli_Under'] * 4000 * (Network[i]['Distance'] ** 2)

    return Network