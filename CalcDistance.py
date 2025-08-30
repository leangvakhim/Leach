# def CalcDistance(Node1, Node2):
#     X = (Node1[0] - Node2[0]) ** 2
#     Y = (Node1[1] - Node2[1]) ** 2
#     Out = (X + Y) ** 0.5
#     return Out
def CalcDistance(coords1, coords2):
    # coords1 will be (x1, y1) and coords2 will be (x2, y2)
    X_dist = (coords1[0] - coords2[0]) ** 2
    Y_dist = (coords1[1] - coords2[1]) ** 2
    
    distance = (X_dist + Y_dist) ** 0.5
    return distance