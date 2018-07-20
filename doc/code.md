### Entity Definition
> entity_def :  ENTITY  IDEN  ed_feature
```
entity coin(1/2 :: head;1/2:: tail)
entity dice(1/3 :: 1; 1/3 :: 2; 1/3 :: 3)
```
-  If default probab is not given, its assumed to be zero.

- Layout
	```
	{
		'entity': coin,
		'feature' :  OrderedDict( [('head', '0.5'), ('tail', '0.5')] ),
		'p_default': ['0.5', '0.5']
	}
	```
-  This layout is passed to solver.add_enitity that generates problog string.
	```
	P_Coin_head :: coin_roll(L, P_Coin_head, P_Coin_tail, D, head); \
	P_Coin_tail :: coin_roll(L, P_Coin_head, P_Coin_tail, D, tail)  \
	:- coin(L, P_Coin_head, P_Coin_tail, D).
	```
- This layout is also saved in parser entity dict.
- Parser also checks that the probab sum is less than 1.
- ToDo :  add other feature explicitly with prob 0 when feature length is 1.

### Enitity Instance
>  entity_instance_wrap : ALIAS ASSIGNMENT entity_instance 
>  entity_instance : IDEN ei_params ei_number 
```
X = coin(1/4,3/4){3}
Y = coin{2}
```
- If no parameters is passed default value is assigned.
- Layout:
	```
	{
		'id' : 'X',
		'type': 'entity_instance',
		'instance' : {
						 'type':'entity_instance',
						 'entity': coin,
						 'label': 'default',
						 'params':[0.25, 0.75]  ,
						 'count' : 3
					}
					
		
	}
	```
- This layout is added to parser alias dict as ID as key.
- Instance is sent to solver.add_entity_instance which generates :
	```
	coin(default, 0.5, 0.5, D ) :- between(1, 3, D).
	```
- ToDo : make flag, the name of alias.

####   Enitity Action
> entity_action : ALIAS ASSIGNMENT ALIAS DOT ROLL LEFTSMALLBRACKET option_number RIGHTSMALLBRACKET
---
> entity_action : ALIAS ASSIGNMENT entity_instance DOT ROLL LEFTSMALLBRACKET option_number RIGHTSMALLBRACKET
```
A = coin(1/5,4/5){2}
B = A.roll()
----------------------------------------
B = coin(1/5,4/5){2}.roll()
```
- Layout :
	```
	{
		'id' : 'B',
		'type': 'entity_action',
		'return': 'alias_B(B1, B2, B3)',
		'length': 2,
		'instance' : {
						 'type':'entity_instance',
						 'entity': coin,
						 'label': 'b',
						 'params':['0.2', '0.8']  ,
						 'count' : 2
					}
					
		
	}
	```
- This layout is added to parser alias dict as ID as key.
- instance and id is sent to solver.add_enitity_action to generate this problog string:
	```
	 alias_B(B1, B2, B3) :- coin_roll(b, 0.2, 0.8, 1, B1 ), \
		 coin_roll(b, 0.2, 0.8,2, B2 ), coin_roll(b, 0.2, 0.8, 3, B3 ) .
	```

#### Bucket Definition
>  bucket_def : BUCKET IDEN LEFTSMALLBRACKET bucket_item_list RIGHTSMALLBRACKET
```
bucket bag( coin{5}, coin(1/4,3/4){2},
		    ball(red){2}, ball(white){4}, racket{2} )
```
- Bucket item
	- Enitity Instance
		-  coin{3}
		-  Picking it gives coin with its params.
		- Ones picked, rolling it gives either head or tail i.e same as entity_action
	- Atom : 
		- racket{2}, Picking it gives racket, Ones picked, rolling it gives racket.
		- ball(white){2}, picking it gives ball(white),  Ones picked, rolling it gives white.
- Layout : 
	```
	{
		'bucket': 'bag',
		'size': 15,
		'r_state': 0,
		'nr_state': 0,
		'instances': [
			{
				'type': 'entity_instance',
				'entity': 'coin',
				'label': 'default', 
				'params': ['0.5', '0.5'],
				'count': 5
			}, 
			{
				'type': 'entity_instance',
				'entity': 'coin',
				'label': 'f', 
				'params': ['0.25', '0.75'],
				'count': 2
			}, 
			{'count': 2, 'type': 'atom', 'name': 'ball(red)'}, 
			{'count': 4, 'type': 'atom', 'name': 'ball(white)'}, 
			{'count': 2, 'type': 'atom', 'name': 'racket'}]
	}
	```
- This layout is sent to solver.add_bucket_def to produce :
	```
	bag_pick(r, 0, default,5,2,2,4,2,15).
	bag_pick(nr, 0, default,5,2,2,4,2,15).
	```
- This layout is added to parser bucket dict with name as key.

### Bucket Action
>  bucket_action : ALIAS ASSIGNMENT IDEN DOT PICK LEFTSMALLBRACKET NUMBER COMMA IDEN RIGHTSMALLBRACKET 
```
X = bag.pick(2,r)
Y = bag.pick(3,nr)
```
- Layout:
	```
	{
		'id' : 'X',
		'type': 'bucket_action',
		'return': 'alias_X(X1, X2, X3)',
		'length': 2,
		'pick_type' : 'nr',
		'bucket' : {bucket_from_above}
	}
	```
-   This layout is added to parser alias dict as ID as key.
- bucket, pick_type and id is sent to solver.add_bucket_action to generate this problog string:
	```
	EC1/T  ::  bag_pick(r, 1,coin(bag_r, 0.5, 0.5, 1 ),EF1,EC2,EC3,EC4,EC5,TF); \
	EC2/T :: bag_pick(r, 1,coin(bag_r, 0.25, 0.75, 1 ),EC1,EF2,EC3,EC4,EC5,TF); \
	EC3/T :: bag_pick(r, 1,ball(red),EC1,EC2,EF3,EC4,EC5,TF); \
	EC4/T :: bag_pick(r, 1,ball(white),EC1,EC2,EC3,EF4,EC5,TF); \ 
	EC5/T :: bag_pick(r, 1,racket,EC1,EC2,EC3,EC4,EF5,TF) \
	:- bag_pick(r, 0,DONT_CARE,EC1,EC2,EC3,EC4,EC5, T), \
	  EF1 is EC1,EF2 is EC2,EF3 is EC3,EF4 is EC4,EF5 is EC5,TF is T .

	alias_Y(Y1) :- bag_pick(r, 1, Y1,_ ,_ ,_ ,_ ,_ ,_ ).
	```

<!--stackedit_data:
eyJoaXN0b3J5IjpbMTgwNzU0MjMyMF19
-->