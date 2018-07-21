entity dice[O,T,Th,F,Fv,S](O::1;T::2;Th::3;F::4;F::5;S::6)

Y = dice(0.1666,0.0666,0.0666,0.3666,0.0666,0.2666 | unfair){3}.roll()

entity coin[H,T](H::head;T::tail)

X = coin(1/2,0.5 | f ){4}.roll()
T = coin(0.7,1/34 | u ){4}.roll()

probability( equalAtmost(5,X,tail))
probability( equalAtmost(5,T,tail))
probability( equalAll(Y,4))
