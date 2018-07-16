X = coin(1/5,5/5){3}.roll()
probab(equalAtmost(2,X,head))

bucket bag( coin{5}, coin(1/4,3/4){2}, ball(red){2}, ball(white){4}, racket{2} )
Y = bag.pick(1,r)
Z = bag.pick(2, r)
K = Z.roll()
