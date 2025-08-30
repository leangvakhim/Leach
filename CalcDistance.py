def CalcDistance(coords1, coords2):
    X_dist = (coords1[0] - coords2[0]) ** 2
    Y_dist = (coords1[1] - coords2[1]) ** 2
    
    distance = (X_dist + Y_dist) ** 0.5
    return distance