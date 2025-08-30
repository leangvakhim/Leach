def DeadCounter(Network):
    Normal = sum(1 for node in Network[:-1] if not node['IsAdvance'] and node['Energy'] <= 0)
    Advance = sum(1 for node in Network[:-1] if node['IsAdvance'] and node['Energy'] <= 0)

    return Normal, Advance