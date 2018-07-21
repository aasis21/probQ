P_Interview_s :: interview_roll(L, P_Interview_s, P_Interview_ns, D, s); P_Interview_ns :: interview_roll(L, P_Interview_s, P_Interview_ns, D, ns) :- interview(L, P_Interview_s, P_Interview_ns, D).

interview(f, 0.14285714285714285, 0.8571428571428571, D ) :- between(1, 1, D).
interview(f, 0.2, 0.8, D ) :- between(1, 1, D).

alias_Hus(Hus1) :- interview_roll(f, 0.14285714285714285, 0.8571428571428571, 1, Hus1 ) .
alias_Wife(Wife1) :- interview_roll(f, 0.2, 0.8, 1, Wife1 ) .

q(2463) :- alias_Hus(Hus1), alias_Wife(Wife1),  ( count([Hus1 , Wife1],s, C4617) , C4617 = 1 ) . 



:- use_module(library(lists)).
count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).

query(q(_)).