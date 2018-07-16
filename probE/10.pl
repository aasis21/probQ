%---------------------------e_def----------------------------
P_Coin_head :: coin_roll(L, P_Coin_head, P_Coin_tail, D, head); P_Coin_tail :: coin_roll(L, P_Coin_head, P_Coin_tail, D, tail) :- coin(L, P_Coin_head, P_Coin_tail, D).
P_Dice_1 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 1); P_Dice_2 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 2); P_Dice_3 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 3); P_Dice_4 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 4); P_Dice_5 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 5); P_Dice_6 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 6) :- dice(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D).

%-----------------------e_instance---------------------------

%-----------------------e_action-----------------------------

%--------------------------b_def-----------------------------
bag_pick_with_state(r, 0, default,4,2,6).
bag_pick_with_state(nr, 0, default,4,2,6).
bag_pick(Type, State, Atom) :- bag_pick_with_state(Type, State, Atom,_ , _ , _ ). 

%--------------------------b_action--------------------------
EC1/T :: bag_pick_with_state(nr, 1,coin(0.5, 0.5),EF1,EC2,TF); EC2/T :: bag_pick_with_state(nr, 1,coin(0.6, 0.4),EC1,EF2,TF):- bag_pick_with_state(nr, 0,DONT_CARE,EC1,EC2, T), EF1 is EC1 - 1, EF1 >= 0,EF2 is EC2 - 1, EF2 >= 0,TF is T - 1, TF >= 0.

EC1/T :: bag_pick_with_state(nr, 2,coin(0.5, 0.5),EF1,EC2,TF); EC2/T :: bag_pick_with_state(nr, 2,coin(0.6, 0.4),EC1,EF2,TF):- bag_pick_with_state(nr, 1,DONT_CARE,EC1,EC2, T), EF1 is EC1 - 1, EF1 >= 0,EF2 is EC2 - 1, EF2 >= 0,TF is T - 1, TF >= 0.

alias_X(X1,X2) :- bag_pick(nr, 1, X1),bag_pick(nr, 2, X2).


%----------------------------query---------------------------
q(2193) :- alias_X(X1,X2),  ( count([X1, X2],coin(0.5, 0.5), C5824) , C5824 = 2 ) . 
q(5116) :- alias_X(X1,X2),  ( ( X1 == coin(0.5, 0.5) ) , ( X2 == coin(0.5, 0.5) ) ) . 



:- use_module(library(lists)).
count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).
query(q(_)).