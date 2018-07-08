
entity student[S,F](S :: 1; F :: 2)

X = student(1/5,4/5){3}.roll()
Y = student(1/4,3/4){2}.roll()
Z = student(1/3,2/3){1}.roll()

probability(
    ( equalAtleast( 2, [ X | Y | Z ] , 1) or equalAtmost( 2, X , 2) )
    and (( X[1] + Y[2] + Z[1] ) / 2) + 3 == 5
)
