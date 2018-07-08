P_Student_1 :: student_roll(L, P_Student_1, P_Student_2, D, 1); P_Student_2 :: student_roll(L, P_Student_1, P_Student_2, D, 2) :- student(L, P_Student_1, P_Student_2, D).

student(f, 0.2, 0.8, D ) :- between(1, 3, D).
student(f, 0.25, 0.75, D ) :- between(1, 2, D).
student(f, 0.3333333333333333, 0.6666666666666666, D ) :- between(1, 1, D).

alias_Y(Y1, Y2) :- student_roll(f, 0.25, 0.75, 1, Y1 ), student_roll(f, 0.25, 0.75, 2, Y2 ) .
alias_X(X1, X2, X3) :- student_roll(f, 0.2, 0.8, 1, X1 ), student_roll(f, 0.2, 0.8, 2, X2 ), student_roll(f, 0.2, 0.8, 3, X3 ) .
alias_Z(Z1) :- student_roll(f, 0.3333333333333333, 0.6666666666666666, 1, Z1 ) .

q(6810) :- alias_Y(Y1, Y2), alias_X(X1, X2, X3), alias_Z(Z1),  ( ( ( count([X1, X2, X3 , Y1, Y2 , Z1],1, C9029) , C9029 >= 2 ) ; ( count([X1, X2, X3],2, C6450) , C6450 =< 2 ) ) , ( ( ( X1 + Y2 + Z1 ) / 2 ) + 3 =:= 5 ) ) . 



:- use_module(library(lists)).
count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).

countall(List,X,C) :-
    sort(List,List1),
    member(X,List1),
    count(List,X,C).

query(q(_)).