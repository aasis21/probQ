P_Dice_1 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 1); P_Dice_2 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 2); P_Dice_3 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 3); P_Dice_4 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 4); P_Dice_5 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 5); P_Dice_6 :: dice_roll(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D, 6) :- dice(L, P_Dice_1, P_Dice_2, P_Dice_3, P_Dice_4, P_Dice_5, P_Dice_6, D).
P_Coin_head :: coin_roll(L, P_Coin_head, P_Coin_tail, D, head); P_Coin_tail :: coin_roll(L, P_Coin_head, P_Coin_tail, D, tail) :- coin(L, P_Coin_head, P_Coin_tail, D).
P_Student_solve :: student_roll(L, P_Student_solve, P_Student_fail, D, solve); P_Student_fail :: student_roll(L, P_Student_solve, P_Student_fail, D, fail) :- student(L, P_Student_solve, P_Student_fail, D).

student(f, 0.5, 0.5, D ) :- between(1, 1, D).
student(f, 0.3333333333333333, 0.6666666666666666, D ) :- between(1, 1, D).
student(f, 0.25, 0.75, D ) :- between(1, 1, D).

alias_A(A1) :- student_roll(f, 0.5, 0.5, 1, A1 ) .
alias_B(B1) :- student_roll(f, 0.3333333333333333, 0.6666666666666666, 1, B1 ) .
alias_C(C1) :- student_roll(f, 0.25, 0.75, 1, C1 ) .

q(9972) :- alias_C(C1), alias_B(B1), alias_A(A1),  ( count([A1 , B1 , C1],solve, C4395) , C4395 >= 1 ) . 



:- use_module(library(lists)).
count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).

query(q(_)).