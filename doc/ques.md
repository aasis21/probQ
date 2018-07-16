### Entity Based Questions

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

### Bucket Based Questions
Q) A bag contains 7 green and 5 black balls. Three balls are drawn one after the other. The probability of all three balls being green, if the balls drawn are not replaced will be.
```
bucket bag(green{7}, black{5})
X = bag.pick(3,nr)
probab(equalAll(X,green))
```
> Answer = 0.159(c)

Q )   A bag contains 6 white and 4 black balls .2 balls are drawn at random. Find the probability that they are of same colour.
```
bucket bag(white{6}, black{4})
X = bag.pick(2,nr)
probab(equalAll(X,white) or equalAll(X, black))
```
> Answer = 0.466 (c)

Q )   A bag contains 6 white and 4 black balls .2 balls are drawn at random with replacement . Find the probability that they are of same colour.
```
bucket bag(white{6}, black{4})
X = bag.pick(2,r)
probab(equalAll(X,white) or equalAll(X, black))
```
> Answer = 0.52 (c)

Q) A box contains 10 bulbs,of which just three are defective. If a random sample of five bulbs is drawn, find the probability that the sample contains exactly one defective bulb.
```
bucket box( bulb(defective){3}, bulb(good){7} )
X = box.pick(5,nr)
probab(equalFew(1,X, bulb(defective) ))
```
Answer = 0.41 (c)
Q)  Four persons are to be choosen from a group of 3 men, 2 women and 4 children. Find the probability of selecting 1 man,1 woman and 2 children.
```
bucket people(man{3}, woman{2}, child{4})
X = people.pick(4,nr)
probab(equalFew(1,X,man) and equalFew(1,X,woman) and equalFew(2,X,child) )
```
> Answer = 0.28 (c)

Q ) A bag contains contain 4 normal coin and 2 baised coin towards head with 0.6.  What is the probability that both are unbiased when 2 coins are drawn.
```
bucket bag(coin{4}, coin(0.6,0.4){2})
X = bag.pick(2,nr)
probab(X[1] == coin(0.5,0.5) and X[2] == coin(0.5,0.5) )
probab(equalAll(X, coin(1/2,1/2) ))
```
