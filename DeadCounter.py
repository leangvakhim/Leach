def DeadCounter(Network):
    # Index_Advance = [i for i, node in enumerate(Network) if node['IsAdvance']]
    # Index_Normal = [i for i, node in enumerate(Network) if not node['IsAdvance']]
    # Normal = sum(Network[i]['Energy'] <= 0 for i in Index_Normal)
    # Advance = sum(Network[i]['Energy'] <= 0 for i in Index_Advance)
    Normal = sum(1 for node in Network[:-1] if not node['IsAdvance'] and node['Energy'] <= 0)
    Advance = sum(1 for node in Network[:-1] if node['IsAdvance'] and node['Energy'] <= 0)

    return Normal, Advance