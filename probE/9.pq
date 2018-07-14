entity apply( 1/3 :: ho; 1/3 :: ht; 1/3 :: ht)
K = apply{3}
H = K.roll()
probability(equalAll(H,ho) or equalAll(H,ht))
