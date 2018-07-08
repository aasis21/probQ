 # The probability of success of three students X, Y and Z in the one examination
 # are 1/5, 1/4 and 1/3 respectively. Find the probability of success of at least two.

 entity student[S,F](
    S :: success; F :: fail
 )

 X = student(1/5,4/5){1}.roll()
 Y = student(1/4,3/4){1}.roll()
 Z = student(1/3,2/3){1}.roll()


probability(
            ( equalAtleast( 2, [ X | Y | Z ] , success) or equalAtmost( 2, X , fail) and equalAll( X , fail) )
            and (( X + Y + Z ) / 2) - 3 == 5

            )
#  entity student[S](S :: success; 1-S::fail)


# correct ans: 1/6 = 0.16666667
