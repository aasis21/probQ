entity apply( 1/3 :: ho; 1/3 :: ht; 1/3 :: hth)
bucket bag(apply(1/3,1/3,1/3){4}, white{4})

Y = bag.pick(3,nr)

probab(Y[1] == white and Y[2] == white )

Z = apply{3}.roll()
probab(equalAll(Z,ho))
