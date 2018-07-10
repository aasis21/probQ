P_Coin_head :: coin_roll(L, P_Coin_head, P_Coin_tail, D, head); P_Coin_tail :: coin_roll(L, P_Coin_head, P_Coin_tail, D, tail) :- coin(L, P_Coin_head, P_Coin_tail, D).
P_Dice_1 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 1); P_Dice_2 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 2); P_Dice_3 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 3); P_Dice_4 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 4); P_Dice_5 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 5); P_Dice_6 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 6) :- dice(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D).
P_Apply_ho :: apply_roll(L, P_Apply_ho, P_Apply_ht, P_Apply_hth, D, ho); P_Apply_ht :: apply_roll(L, P_Apply_ho, P_Apply_ht, P_Apply_hth, D, ht); P_Apply_hth :: apply_roll(L, P_Apply_ho, P_Apply_ht, P_Apply_hth, D, hth) :- apply(L, P_Apply_ho, P_Apply_ht, P_Apply_hth, D).

apply(f, 0.5, 0.16666666666666666, 0.3333333333333333, D ) :- between(1, 3, D).

alias_H(H1, H2, H3) :- apply_roll(f, 0.5, 0.16666666666666666, 0.3333333333333333, 1, H1 ), apply_roll(f, 0.5, 0.16666666666666666, 0.3333333333333333, 2, H2 ), apply_roll(f, 0.5, 0.16666666666666666, 0.3333333333333333, 3, H3 ) .

q(7920) :- alias_H(H1, H2, H3),  ( ( count([H1, H2, H3],ho, C1410) , C1410 = 3 ) ; ( count([H1, H2, H3],ht, C1498) , C1498 = 3 ) ; ( count([H1, H2, H3],hth, C4155) , C4155 = 3 ) ) . 



:- use_module(library(lists)).
count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).

query(q(_)).