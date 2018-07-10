entity apply( 1/3 :: ho; 1/3 :: ht; 1/3 :: hth)
H = apply{3}.roll()
probability(equalAll(H,ho) or equalAll(H,ht) or equalAll(H,hth))
