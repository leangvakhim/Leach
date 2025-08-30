# def Direct_UsedEnergy(Model, Network):
#     Alive_Index = [i for i, node in enumerate(Network[:-2]) if node['Energy'] > 0]
#     # Alive_Index = [i for i, node in enumerate(Network[:-2]) if node['Energy'] > 0]
#     for i in range(Alive_Index):
#         if Network[i]['Distance'] > Model['BaseDistance']:
#             Network[i]['Energy'] = Network[i]['Energy'] - (Model['Energy']['Send_Bit'] + Model['Energy']['Aggregation_Bit'] * 4000) + Model['Energy']['Ampli_Upper'] * 4000 * (Network[i]['Distance'] ** 2)
#         else:
#             Network[i]['Energy'] = Network[i]['Energy'] - (Model['Energy']['Send_Bit'] + Model['Energy']['Aggregation_Bit'] * 4000) + Model['Energy']['Ampli_Under'] * 4000 * (Network[i]['Distance'] ** 2)

#     return Network

def Direct_UsedEnergy(Model, Network):
    # Get a list of the indices of all nodes that are still alive
    Alive_Indices = [i for i, node in enumerate(Network[:-1]) if node['Energy'] > 0]
    
    # --- THIS IS THE CORRECTED LOOP ---
    # We loop directly through the 'Alive_Indices' list.
    # 'i' will be each index from the list, one by one.
    for i in Alive_Indices:
        node = Network[i]
        distance = node['Distance']
        
        # Deduct energy based on the distance to the sink
        if distance > Model['BaseDistance']:
            energy_used = (Model['Energy']['Send_Bit'] * 4000) + (Model['Energy']['Ampli_Upper'] * 4000 * (distance ** 2))
        else:
            energy_used = (Model['Energy']['Send_Bit'] * 4000) + (Model['Energy']['Ampli_Under'] * 4000 * (distance ** 2))
        
        node['Energy'] -= energy_used

    return Network