def DeadCounter(Network):
    Index_Advance = [i for i, node in enumerate(Network) if node['IsAdvance']]
    Index_Normal = [i for i, node in enumerate(Network) if not node['IsAdvance']]
    Normal = sum(Network[i]['Energy'] <= 0 for i in Index_Normal)
    Advance = sum(Network[i]['Energy'] <= 0 for i in Index_Advance)

    return Normal, Advance