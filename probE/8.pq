X = dice{2}.roll()
probability(X[1] + X[2] > 7 or equalAll(X,6))

Y = coin{2}.roll()
probability(equalAll(Y,head))
