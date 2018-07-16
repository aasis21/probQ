%---------------------------e_def----------------------------
P_Dice_1 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 1); P_Dice_2 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 2); P_Dice_3 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 3); P_Dice_4 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 4); P_Dice_5 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 5); P_Dice_6 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 6) :- dice(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D).
P_Coin_head :: coin_roll(L, P_Coin_head, P_Coin_tail, D, head); P_Coin_tail :: coin_roll(L, P_Coin_head, P_Coin_tail, D, tail) :- coin(L, P_Coin_head, P_Coin_tail, D).

%-----------------------e_instance---------------------------
coin(f, 0.2, 1.0, D ) :- between(1, 3, D).


%-----------------------e_action-----------------------------
alias_X(X1, X2, X3) :- coin_roll(f, 0.2, 1.0, 1, X1 ), coin_roll(f, 0.2, 1.0, 2, X2 ), coin_roll(f, 0.2, 1.0, 3, X3 ) .

%--------------------------b_def-----------------------------
bag_pick_with_state(r, 0, default,5,2,2,4,2,15).
bag_pick_with_state(nr, 0, default,5,2,2,4,2,15).
bag_pick(Type, State, Atom) :- bag_pick_with_state(Type, State, Atom,_ , _ , _ , _ , _ , _ ). 
coin( X1 , 0.5, 0.5, X2 ) :- bag_pick(_,X2,coin( X1 , 0.5, 0.5, _)).
coin( X1 , 0.25, 0.75, X2 ) :- bag_pick(_,X2,coin( X1 , 0.25, 0.75, _)).
red( bag_r , X2 ) :- bag_pick(_,X2,ball(red)). 
red( bag_nr , X2 ) :- bag_pick(_,X2,ball(red)). 

white( bag_r , X2 ) :- bag_pick(_,X2,ball(white)). 
white( bag_nr , X2 ) :- bag_pick(_,X2,ball(white)). 

racket( bag_r , X2 ) :- bag_pick(_,X2,racket). 
racket( bag_nr , X2 ) :- bag_pick(_,X2,racket). 


%--------------------------b_action--------------------------
EC1/T :: bag_pick_with_state(r, 1,coin(bag_r, 0.5, 0.5, 1 ),EF1,EC2,EC3,EC4,EC5,TF); EC2/T :: bag_pick_with_state(r, 1,coin(bag_r, 0.25, 0.75, 1 ),EC1,EF2,EC3,EC4,EC5,TF); EC3/T :: bag_pick_with_state(r, 1,ball(red),EC1,EC2,EF3,EC4,EC5,TF); EC4/T :: bag_pick_with_state(r, 1,ball(white),EC1,EC2,EC3,EF4,EC5,TF); EC5/T :: bag_pick_with_state(r, 1,racket,EC1,EC2,EC3,EC4,EF5,TF):- bag_pick_with_state(r, 0,DONT_CARE,EC1,EC2,EC3,EC4,EC5, T), EF1 is EC1,EF2 is EC2,EF3 is EC3,EF4 is EC4,EF5 is EC5,TF is T .

alias_Y(Y1) :- bag_pick(r, 1, Y1).

EC1/T :: bag_pick_with_state(r, 2,coin(bag_r, 0.5, 0.5, 1 ),EF1,EC2,EC3,EC4,EC5,TF); EC2/T :: bag_pick_with_state(r, 2,coin(bag_r, 0.25, 0.75, 1 ),EC1,EF2,EC3,EC4,EC5,TF); EC3/T :: bag_pick_with_state(r, 2,ball(red),EC1,EC2,EF3,EC4,EC5,TF); EC4/T :: bag_pick_with_state(r, 2,ball(white),EC1,EC2,EC3,EF4,EC5,TF); EC5/T :: bag_pick_with_state(r, 2,racket,EC1,EC2,EC3,EC4,EF5,TF):- bag_pick_with_state(r, 1,DONT_CARE,EC1,EC2,EC3,EC4,EC5, T), EF1 is EC1,EF2 is EC2,EF3 is EC3,EF4 is EC4,EF5 is EC5,TF is T .

EC1/T :: bag_pick_with_state(r, 3,coin(bag_r, 0.5, 0.5, 1 ),EF1,EC2,EC3,EC4,EC5,TF); EC2/T :: bag_pick_with_state(r, 3,coin(bag_r, 0.25, 0.75, 1 ),EC1,EF2,EC3,EC4,EC5,TF); EC3/T :: bag_pick_with_state(r, 3,ball(red),EC1,EC2,EF3,EC4,EC5,TF); EC4/T :: bag_pick_with_state(r, 3,ball(white),EC1,EC2,EC3,EF4,EC5,TF); EC5/T :: bag_pick_with_state(r, 3,racket,EC1,EC2,EC3,EC4,EF5,TF):- bag_pick_with_state(r, 2,DONT_CARE,EC1,EC2,EC3,EC4,EC5, T), EF1 is EC1,EF2 is EC2,EF3 is EC3,EF4 is EC4,EF5 is EC5,TF is T .

alias_Z(Z1,Z2) :- bag_pick(r, 2, Z1),bag_pick(r, 3, Z2).


%----------------------------query---------------------------
q(1972) :- alias_X(X1, X2, X3),  ( count([X1, X2, X3],head, C9641) , C9641 =< 2 ) . 



:- use_module(library(lists)).
count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).
query(q(_)).