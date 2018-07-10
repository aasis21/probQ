P_Coin_head :: coin_roll(L, P_Coin_head, P_Coin_tail, D, head); P_Coin_tail :: coin_roll(L, P_Coin_head, P_Coin_tail, D, tail) :- coin(L, P_Coin_head, P_Coin_tail, D).

coin(f, 0.5, 0.5, D ) :- between(1, 3, D).

alias_X(X1, X2, X3) :- coin_roll(f, 0.5, 0.5, 1, X1 ), coin_roll(f, 0.5, 0.5, 2, X2 ), coin_roll(f, 0.5, 0.5, 3, X3 ) .

q(3882) :- alias_X(X1, X2, X3),  ( count([X1, X2, X3],head, C4910) , C4910 =< 2 ) . 



:- use_module(library(lists)).
count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).

query(q(_)).