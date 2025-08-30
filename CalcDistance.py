def CalcDistance(Node1, Node2):
    X = (Node1[0] - Node2[0]) ** 2
    Y = (Node1[1] - Node2[1]) ** 2
    Out = (X + Y) ** 0.5
    return Out