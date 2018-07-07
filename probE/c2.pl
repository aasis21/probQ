:- use_module(library(lists)).

dice(f,D) :- between(1,6,D).

1/6::die(F,D, one); 1/6::die(F,D, two); 1/6::die(F,D, three);
1/6::die(F,D, 4); 1/6::die(F,D, 5); 1/6::die(F,D, 6) :- dice(F,D).

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

% p(E,C) :- rolld(X,Y,Z,X1) , L = [X,Y,Z,X1] , countall(L,E,C).

q(equalAtmost_1_X_3) :- rolld(X,Y,Z,X1) , L = [X,Y,Z,X1] , countall(L,E,C), ((C >= 1, E = three )) .
q(equalAtmost_1_X_4) :- rolld(X,Y,Z,X1) , L = [X,Y,Z,X1] , countall(L,E,C), ((C >= 1, E = three )) .


query(q(_)).
% query(p(three,)).
