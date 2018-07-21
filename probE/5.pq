entity interview(s;ns)
Hus = interview(1/7,6/7){1}.roll()
Wife = interview(1/5,4/5){1}.roll()
probability(equalFew(1,[Hus|Wife],s))
