% Your model here


:- use_module(library(lists)).


dice(f,probab,D) :- between(1,6,D).
1/6::die(F,D, one); 1/6::die(F,D, two); 1/6::die(F,D, three);
1/6::die(F,D, 4); 1/6::die(F,D, 5); 1/6::die(F,D, 6) :- dice(F,P,D).

%
% p(E,C) :- die(f,1,X),die(f,2,Y),die(f,3,Z),die(f,1,X1), count([X,Y,Z,X1],E,C) .
%
% q :- C = 1 ,p(three,C).
% query(q).
% query(p(three,C)).

count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).

countall(List,X,C) :-
    sort(List,List1),
    member(X,List1),
    count(List,X,C).


p(M) :- die(f,1,X),die(f,2,Y),die(f,3,Z),die(f,1,X1), member(M,[X,Y,Z,X1]), count([X,Y,Z,X1],E,C) .
query(p(_)).

% query(countall([1,2,3,4,5,6,7,7,8,8,8,8,9,gdgh,dsgsgf],X,C)).



% Your model here


:- use_module(library(lists)).


dice(f,probab,D) :- between(1,6,D).
1/6::die(F,D, one); 1/6::die(F,D, two); 1/6::die(F,D, three);
1/6::die(F,D, 4); 1/6::die(F,D, 5); 1/6::die(F,D, 6) :- dice(F,P,D).

%
% p(E,C) :- die(f,1,X),die(f,2,Y),die(f,3,Z),die(f,1,X1), count([X,Y,Z,X1],E,C) .
%
% q :- C = 1 ,p(three,C).
% query(q).
% query(p(three,C)).

count([],X,0).
count([X|T],X,Y):- count(T,X,Z), Y is 1+Z.
count([X1|T],X,Z):- X1\=X,count(T,X,Z).

countall(List,X,C) :-
    sort(List,List1),
    member(X,List1),
    count(List,X,C).
rolld(X,Y,Z,X1) :- die(f,1,X),die(f,2,Y),die(f,3,Z),die(f,1,X1).

cond :- rolld(X,Y,Z,X1) , L = , count(L,4,1).

evidence( cond,true).
p(M,C) :- rolld(X,Y,Z,X1) , L = [X,Y,Z,X1], member(M,L), C=1.
query(p(_,_)).

% query(countall([1,2,3,4,5,6,7,7,8,8,8,8,9,gdgh,dsgsgf],X,C)).
