entity dice(1;2;3;4;5;6)
X = dice(1/6,1/6,1/6,1/6,1/6,1/6){2}.roll()
Y = dice(1/6,1/6,1/6,1/6,1/6,1/6){3}.roll()
probability( sum( (X[1:2]|Y[2]),4) ) 