%---------------------------e_def----------------------------
P_Coin_head :: coin_roll(L, P_Coin_head, P_Coin_tail, D, head); P_Coin_tail :: coin_roll(L, P_Coin_head, P_Coin_tail, D, tail) :- coin(L, P_Coin_head, P_Coin_tail, D).
P_Dice_1 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 1); P_Dice_2 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 2); P_Dice_3 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 3); P_Dice_4 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 4); P_Dice_5 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 5); P_Dice_6 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 6) :- dice(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D).
P_Apply_ho :: apply_roll(L, P_Apply_ho, P_Apply_ht, P_Apply_hth, D, ho); P_Apply_ht :: apply_roll(L, P_Apply_ho, P_Apply_ht, P_Apply_hth, D, ht); P_Apply_hth :: apply_roll(L, P_Apply_ho, P_Apply_ht, P_Apply_hth, D, hth) :- apply(L, P_Apply_ho, P_Apply_ht, P_Apply_hth, D).

%-----------------------e_instance---------------------------
apply(empty, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, D ) :- between(1, 3, D).

%-----------------------e_action-----------------------------
alias_Z(Z1, Z2, Z3) :- apply_roll(empty, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 1, Z1 ), apply_roll(empty, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 2, Z2 ), apply_roll(empty, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 3, Z3 ) .

%--------------------------b_def-----------------------------
bag_pick(r, 0, default,4,4,8).
bag_pick(nr, 0, default,4,4,8).

%--------------------------b_action--------------------------
EC1/T :: bag_pick(nr, 1,apply(f, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 1 ),EF1,EC2,TF); EC2/T :: bag_pick(nr, 1,white,EC1,EF2,TF):- bag_pick(nr, 0,DONT_CARE,EC1,EC2, T), EF1 is EC1 - 1,EF2 is EC2 - 1,TF is T - 1.
EC1/T :: bag_pick(nr, 2,apply(f, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 1 ),EF1,EC2,TF); EC2/T :: bag_pick(nr, 2,white,EC1,EF2,TF):- bag_pick(nr, 1,DONT_CARE,EC1,EC2, T), EF1 is EC1 - 1,EF2 is EC2 - 1,TF is T - 1.
EC1/T :: bag_pick(nr, 3,apply(f, 0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 1 ),EF1,EC2,TF); EC2/T :: bag_pick(nr, 3,white,EC1,EF2,TF):- bag_pick(nr, 2,DONT_CARE,EC1,EC2, T), EF1 is EC1 - 1,EF2 is EC2 - 1,TF is T - 1.
alias_Y(Y1,Y2,Y3) :- bag_pick(nr, 1, Y1,_ ,_ ,_ ), bag_pick(nr, 2, Y2,_ ,_ ,_ ), bag_pick(nr, 3, Y3,_ ,_ ,_ ).

%----------------------------query---------------------------
q(1597) :- alias_Y(Y1,Y2,Y3),  ( ( Y1 == white ) , ( Y2 == white ) ) . 
q(3744) :- alias_Z(Z1, Z2, Z3),  ( count([Z1, Z2, Z3],ho, C2631) , C2631 = 3 ) . 



:- use_module(library(lists)).
count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).
query(q(_)).