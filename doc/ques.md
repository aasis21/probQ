Q) A problem is given to three students whose chances of solving it are 1/2, 1/3 and 1/4 respectively. What is the probability that the problem will be solved?
```
entity student(do;n_do)
A = student(1/2,1/2){1}.roll()
B = student(1/3,2/3){1}.roll()
C = student(1/4,3/4){1}.roll()
probab( equalAtleast(1,[A|B|C], do) )
```
> Answer = 0.75 (c)

Q) A man and his wife appear in an interview for two vacancies in the same post. The probability of husband's selection is (1/7) and the probability of wife's selection is (1/5). What is the probability that only one of them is selected ?
```
entity interview(s; ns)
Hus = interview(1/7,6/7){1}.roll()
Wife = interview(1/5,4/5){1}.roll()
probab(equalFew(1,[Hus|Wife],s))
```
> Answer = 	0.285 (c)

Q) Two dice are thrown together . What is the probability that the sum of the number on the two faces is divided by 4 or 6.
```
X = dice(1/6,1/6,1/6,1/6,1/12,3/12){2}.roll()
probab((X[1]+ X[2] / 4 == 1 ) or (X[1]+ X[2] / 4 == 2 ) or (X[1]+ X[2] / 4 == 3 ) or (X[1]+ X[2] / 6 == 2 ) or (X[1]+ X[2] / 6 == 1 ) )

```
Q) Three unbiased coins are tossed. What is the probability of getting at most two heads?
```
X = coin{3}.roll()
probab(equalAtmost(2,X,head))
```
> Answer = 0.875 (c)

Q) In a simultaneous throw of pair of dice. Find the probability of getting the total more than 7.
```
X = dice{2}.roll()
probab(X[1] + X[2] > 7)
```
> Answer = 0.416 (c) // parse list of alias

Q) Three houses are available in a locality. Three persons apply for the houses. Each applies for one house without consulting others. The probability that all the three apply for the same house is ?
```
entity apply( 1/3 :: ho; 1/3 :: ht; 1/3 :: hth)
H = apply{3}.roll()
probab(equalAll(H,ho) or equalAll(H,ht) or equalAll(H,hth))
```
> Answer = 0.1111 (c) // allow ho as h1

Q) Two brother appeared for an exam. The probability of selection of A is 1/7 and that of B is 2/9. Find the probability that both of them are selected.

```
entity exam( pass; fail)
X = exam(1/7,6/7){1}.roll()
Y = exam(2/9,7/9){1}.roll()
probab(equalAll([X|Y],pass))
```
> Answer = 0.031 (c)

Q) In a single throw of two dice , find the probability that neither a (1,1) nor a total of 8 will appear.
```
X = dice{2}.roll()
probab( not ((X[1] + X[2] == 8) or equalAll(X,1) ) )
```
> Answer (c)

Q) A coin is tossed 5 times. What is the probability that head appears an odd number of times?
```
X = coin{5}.roll()
probability( ) // new construct.
```
