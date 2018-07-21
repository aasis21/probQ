P_Student_solve :: student_roll(L, P_Student_solve, P_Student_fail, D, solve); P_Student_fail :: student_roll(L, P_Student_solve, P_Student_fail, D, fail) :- student(L, P_Student_solve, P_Student_fail, D).

student(f, 0.5, 0.5, D ) :- between(1, 1, D).
student(f, 0.3333333333333333, 0.6666666666666666, D ) :- between(1, 1, D).
student(f, 0.25, 0.75, D ) :- between(1, 1, D).

alias_C(C1) :- student_roll(f, 0.25, 0.75, 1, C1 ) .
alias_B(B1) :- student_roll(f, 0.3333333333333333, 0.6666666666666666, 1, B1 ) .
alias_A(A1) :- student_roll(f, 0.5, 0.5, 1, A1 ) .

q(4873) :- alias_C(C1), alias_B(B1), alias_A(A1),  ( count([A1 , B1 , C1],solve, C7636) , C7636 >= 1 ) . 



:- use_module(library(lists)).
count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).

query(q(_)).