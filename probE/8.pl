%---------------------------e_def----------------------------
P_Coin_head :: coin_roll(L, P_Coin_head, P_Coin_tail, D, head); P_Coin_tail :: coin_roll(L, P_Coin_head, P_Coin_tail, D, tail) :- coin(L, P_Coin_head, P_Coin_tail, D).
P_Dice_1 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 1); P_Dice_2 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 2); P_Dice_3 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 3); P_Dice_4 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 4); P_Dice_5 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 5); P_Dice_6 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 6) :- dice(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D).

%-----------------------e_instance---------------------------
dice(empty, 0.16666666666, 0.16666666666, 0.16666666666, 0.16666666666, 0.16666666666, 0.16666666666, D ) :- between(1, 2, D).
coin(empty, 0.5, 0.5, D ) :- between(1, 2, D).

%-----------------------e_action-----------------------------
alias_X(X1, X2) :- dice_roll(empty, 0.16666666666, 0.16666666666, 0.16666666666, 0.16666666666, 0.16666666666, 0.16666666666, 1, X1 ), dice_roll(empty, 0.16666666666, 0.16666666666, 0.16666666666, 0.16666666666, 0.16666666666, 0.16666666666, 2, X2 ) .

%--------------------------b_def-----------------------------

%--------------------------b_action--------------------------

%----------------------------query---------------------------
q(1047) :- alias_X(X1, X2),  ( ( X1 + X2 > 7 ) ; ( count([X1, X2],6, C6178) , C6178 = 2 ) ) . 



:- use_module(library(lists)).
count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).
query(q(_)).