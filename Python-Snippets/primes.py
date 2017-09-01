pp = filter(lambda g: not any(g % u == 0 for u in range(2, g)), range(2, 10000))
