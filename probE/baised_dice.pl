coin(fair,0.5, D) :- between(1,2,D).
coin(b1,0.7,1).

H::flip(F, D, 1); T::flip(F, D, 0) :- coin(F, H ,D), T is 1 - H.

q :- flip(fair,1,X), flip(fair,2,Y),flip(b1,1,Z), (X+Y+Z =:= 2;X+Y+Z =:= 1;X+Y+Z =:= 0).

query(q).
