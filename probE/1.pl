P_Student_success :: student_roll(L, P_Student_success, P_Student_fail, D, success); P_Student_fail :: student_roll(L, P_Student_success, P_Student_fail, D, fail) :- student(L, P_Student_success, P_Student_fail, D).

student(f, 0.2, 0.8, D ) :- between(1, 1, D).
student(f, 0.25, 0.75, D ) :- between(1, 1, D).
student(f, 0.3333333333333333, 0.6666666666666666, D ) :- between(1, 1, D).

alias_Y(Y1) :- student_roll(f, 0.25, 0.75, 1, Y1 ) .
alias_X(X1) :- student_roll(f, 0.2, 0.8, 1, X1 ) .
alias_Z(Z1) :- student_roll(f, 0.3333333333333333, 0.6666666666666666, 1, Z1 ) .




:- use_module(library(lists)).
count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).

countall(List,X,C) :-
    sort(List,List1),
    member(X,List1),
    count(List,X,C).

query(q(_)).