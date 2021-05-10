import random

f=open("attack.txt","w")
s = set()
break_point = 5
for i in range(2,200):
	for k in range(1000//i):
		my_char=chr(random.randrange(97, 97 + 8))
		my_int= random.randint(1, 10000)
		toappend= str(my_char)  + "_"+ str(my_int)

		while s != set() and (toappend in s):
			my_char=chr(random.randrange(97, 97 + 8))
			my_int= random.randint(1, 10000)
			toappend= str(my_char)  + "_"+ str(my_int)

		s.add(toappend)
			

for i in range(0,100000//break_point):
	my_char=chr(random.randrange(97, 97 + 8))
	my_int= random.randint(1, 10000)
	toappend= str(my_char)  + "_"+ str(my_int)

	while s != set() and (toappend in s):
		my_char=chr(random.randrange(97, 97 + 8))
		my_int= random.randint(1, 10000)
		toappend= str(my_char)  + "_"+ str(my_int)

	s.add(toappend)
	for j in range(break_point):
		f.write(toappend)
		f.write("\n")
