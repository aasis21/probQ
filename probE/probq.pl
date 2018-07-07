P_Coin_head :: coin_roll(L, P_Coin_head, P_Coin_tail, D, head); P_Coin_tail :: coin_roll(L, P_Coin_head, P_Coin_tail, D, tail) :- coin(L, P_Coin_head, P_Coin_tail, D).
P_Dice_1 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 1); P_Dice_2 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 2); P_Dice_3 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 3); P_Dice_4 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 4); P_Dice_5 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 5); P_Dice_6 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 6) :- dice(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D).

dice(unfair, 0.1666, 0.0666, 0.0666, 0.3666, 0.0666, 0.2666, D ) :- between(1, 2, D).
coin(f, 0.5, 0.5, D ) :- between(1, 6, D).
coin(u, 0.7, 0.029411764705882353, D ) :- between(1, 6, D).

alias_Y(Y1, Y2) :- dice_roll(unfair, 0.1666, 0.0666, 0.0666, 0.3666, 0.0666, 0.2666, 1, Y1 ), dice_roll(unfair, 0.1666, 0.0666, 0.0666, 0.3666, 0.0666, 0.2666, 2, Y2 ) .
alias_T(T1, T2, T3, T4, T5, T6) :- coin_roll(u, 0.7, 0.029411764705882353, 1, T1 ), coin_roll(u, 0.7, 0.029411764705882353, 2, T2 ), coin_roll(u, 0.7, 0.029411764705882353, 3, T3 ), coin_roll(u, 0.7, 0.029411764705882353, 4, T4 ), coin_roll(u, 0.7, 0.029411764705882353, 5, T5 ), coin_roll(u, 0.7, 0.029411764705882353, 6, T6 ) .
alias_X(X1, X2, X3, X4, X5, X6) :- coin_roll(f, 0.5, 0.5, 1, X1 ), coin_roll(f, 0.5, 0.5, 2, X2 ), coin_roll(f, 0.5, 0.5, 3, X3 ), coin_roll(f, 0.5, 0.5, 4, X4 ), coin_roll(f, 0.5, 0.5, 5, X5 ), coin_roll(f, 0.5, 0.5, 6, X6 ) .

q(equalAtmost_5_T_tail) :-  alias_T(T1, T2, T3, T4, T5, T6) , L = [T1, T2, T3, T4, T5, T6], countall(L, E, C) , E = tail , C =< 5 .
q(equalAtmost_5_X_tail) :-  alias_X(X1, X2, X3, X4, X5, X6) , L = [X1, X2, X3, X4, X5, X6], countall(L, E, C) , E = tail , C =< 5 .
q(equalAll_Y_4) :-  alias_Y(Y1, Y2) , L = [Y1, Y2], countall(L, E, C) , E = 4 , C = 2 .



:- use_module(library(lists)).
count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).

countall(List,X,C) :-
    sort(List,List1),
    member(X,List1),
    count(List,X,C).

query(q(_)).