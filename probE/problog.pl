P_Dice_1 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 1); P_Dice_2 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 2); P_Dice_3 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 3); P_Dice_4 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 4); P_Dice_5 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 5); P_Dice_6 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 6) :- dice(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D).

dice(unfair, 0.1666, 0.0666, 0.0666, 0.3666, 0.0666, 0.2666, D ) :- between(1, 3, D).

alias_Y(Y1, Y2, Y3) :- dice_roll(unfair, 0.1666, 0.0666, 0.0666, 0.3666, 0.0666, 0.2666, 1, Y1 ), dice_roll(unfair, 0.1666, 0.0666, 0.0666, 0.3666, 0.0666, 0.2666, 2, Y2 ), dice_roll(unfair, 0.1666, 0.0666, 0.0666, 0.3666, 0.0666, 0.2666, 3, Y3 ) .

q(equalAtmost_2_Y_4) :-  alias_Y(Y1, Y2, Y3) , L = [Y1, Y2, Y3], countall(L, E, C) , E = 4 , C =< 2 .



:- use_module(library(lists)).
count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).

countall(List,X,C) :-
    sort(List,List1),
    member(X,List1),
    count(List,X,C).

query(q(_)).