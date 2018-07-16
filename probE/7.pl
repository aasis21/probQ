%---------------------------e_def----------------------------
P_Dice_1 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 1); P_Dice_2 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 2); P_Dice_3 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 3); P_Dice_4 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 4); P_Dice_5 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 5); P_Dice_6 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 6) :- dice(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D).
P_Coin_head :: coin_roll(L, P_Coin_head, P_Coin_tail, D, head); P_Coin_tail :: coin_roll(L, P_Coin_head, P_Coin_tail, D, tail) :- coin(L, P_Coin_head, P_Coin_tail, D).

%-----------------------e_instance---------------------------
coin(x, 0.2, 0.8, D ) :- between(1, 3, D).


%-----------------------e_action-----------------------------
alias_X(X1, X2, X3) :- coin_roll(x, 0.2, 0.8, 1, X1 ), coin_roll(x, 0.2, 0.8, 2, X2 ), coin_roll(x, 0.2, 0.8, 3, X3 ) .

%--------------------------b_def-----------------------------
bag_pick_with_state(r, 0, default,5,2,2,4,2,15).
bag_pick_with_state(nr, 0, default,5,2,2,4,2,15).
bag_pick(Type, State, Atom) :- bag_pick_with_state(Type, State, Atom,_ , _ , _ , _ , _ , _ ). 

%--------------------------b_action--------------------------
EC1/T :: bag_pick_with_state(r, 1,coin(0.5, 0.5),EF1,EC2,EC3,EC4,EC5,TF); EC2/T :: bag_pick_with_state(r, 1,coin(0.25, 0.75),EC1,EF2,EC3,EC4,EC5,TF); EC3/T :: bag_pick_with_state(r, 1,ball(red),EC1,EC2,EF3,EC4,EC5,TF); EC4/T :: bag_pick_with_state(r, 1,ball(white),EC1,EC2,EC3,EF4,EC5,TF); EC5/T :: bag_pick_with_state(r, 1,racket,EC1,EC2,EC3,EC4,EF5,TF):- bag_pick_with_state(r, 0,DONT_CARE,EC1,EC2,EC3,EC4,EC5, T), EF1 is EC1,EF2 is EC2,EF3 is EC3,EF4 is EC4,EF5 is EC5,TF is T .

EC1/T :: bag_pick_with_state(r, 2,coin(0.5, 0.5),EF1,EC2,EC3,EC4,EC5,TF); EC2/T :: bag_pick_with_state(r, 2,coin(0.25, 0.75),EC1,EF2,EC3,EC4,EC5,TF); EC3/T :: bag_pick_with_state(r, 2,ball(red),EC1,EC2,EF3,EC4,EC5,TF); EC4/T :: bag_pick_with_state(r, 2,ball(white),EC1,EC2,EC3,EF4,EC5,TF); EC5/T :: bag_pick_with_state(r, 2,racket,EC1,EC2,EC3,EC4,EF5,TF):- bag_pick_with_state(r, 1,DONT_CARE,EC1,EC2,EC3,EC4,EC5, T), EF1 is EC1,EF2 is EC2,EF3 is EC3,EF4 is EC4,EF5 is EC5,TF is T .

alias_Z(Z1,Z2) :- bag_pick(r, 1, Z1),bag_pick(r, 2, Z2).

EC1/T :: bag_pick_with_state(nr, 1,coin(0.5, 0.5),EF1,EC2,EC3,EC4,EC5,TF); EC2/T :: bag_pick_with_state(nr, 1,coin(0.25, 0.75),EC1,EF2,EC3,EC4,EC5,TF); EC3/T :: bag_pick_with_state(nr, 1,ball(red),EC1,EC2,EF3,EC4,EC5,TF); EC4/T :: bag_pick_with_state(nr, 1,ball(white),EC1,EC2,EC3,EF4,EC5,TF); EC5/T :: bag_pick_with_state(nr, 1,racket,EC1,EC2,EC3,EC4,EF5,TF):- bag_pick_with_state(nr, 0,DONT_CARE,EC1,EC2,EC3,EC4,EC5, T), EF1 is EC1 - 1,EF2 is EC2 - 1,EF3 is EC3 - 1,EF4 is EC4 - 1,EF5 is EC5 - 1,TF is T - 1.

alias_Y(Y1) :- bag_pick(nr, 1, Y1).


%----------------------------query---------------------------
q(2002) :- alias_Y(Y1),  ( Y1 == ball(white) ) . 
q(2406) :- alias_X(X1, X2, X3),  ( ( count([X1, X2, X3],head, C4420) , C4420 =< 2 ) , ( X1 == head ) ) . 



:- use_module(library(lists)).
count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).
query(q(_)).