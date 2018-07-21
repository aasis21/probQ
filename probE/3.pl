P_Dice_1 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, D, 1); P_Dice_2 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, D, 2); P_Dice_3 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, D, 3) :- dice(L, P_Dice_1, P_Dice_2, P_Dice_3, D).

dice(f, 0.5, 0.3333333333333333, 0.6666666666666666, D ) :- between(1, 5, D).

alias_Y(Y1, Y2, Y3, Y4, Y5) :- dice_roll(f, 0.5, 0.3333333333333333, 0.6666666666666666, 1, Y1 ), dice_roll(f, 0.5, 0.3333333333333333, 0.6666666666666666, 2, Y2 ), dice_roll(f, 0.5, 0.3333333333333333, 0.6666666666666666, 3, Y3 ), dice_roll(f, 0.5, 0.3333333333333333, 0.6666666666666666, 4, Y4 ), dice_roll(f, 0.5, 0.3333333333333333, 0.6666666666666666, 5, Y5 ) .




:- use_module(library(lists)).
count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).

countall(List,X,C) :-
    sort(List,List1),
    member(X,List1),
    count(List,X,C).

query(q(_)).