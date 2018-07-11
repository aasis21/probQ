P_Dice_1 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 1); P_Dice_2 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 2); P_Dice_3 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 3); P_Dice_4 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 4); P_Dice_5 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 5); P_Dice_6 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 6) :- dice(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D).
P_Coin_head :: coin_roll(L, P_Coin_head, P_Coin_tail, D, head); P_Coin_tail :: coin_roll(L, P_Coin_head, P_Coin_tail, D, tail) :- coin(L, P_Coin_head, P_Coin_tail, D).
P_Interview_s :: interview_roll(L, P_Interview_s, P_Interview_ns, D, s); P_Interview_ns :: interview_roll(L, P_Interview_s, P_Interview_ns, D, ns) :- interview(L, P_Interview_s, P_Interview_ns, D).

interview(f, 0.14285714285714285, 0.8571428571428571, D ) :- between(1, 1, D).
interview(f, 0.2, 0.8, D ) :- between(1, 1, D).

alias_Hus(Hus1) :- interview_roll(f, 0.14285714285714285, 0.8571428571428571, 1, Hus1 ) .
alias_Wife(Wife1) :- interview_roll(f, 0.2, 0.8, 1, Wife1 ) .

q(3228) :- alias_Hus(Hus1), alias_Wife(Wife1),  ( count([Hus1 , Wife1],s, C1567) , C1567 = 1 ) . 



:- use_module(library(lists)).
count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).

query(q(_)).