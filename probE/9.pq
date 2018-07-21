entity apply( 1/3 :: ho; 1/3 :: ht; 1/3 :: hth)
K = apply(1/2,1/6,2/6){3}
H = K.roll()
probability(equalAll(H,ho) or equalAll(H,ht) or equalAll(H,hth))
