import random

f=open("attack.txt","w")
for i in range(1,20000):
	my_char=chr(random.randrange(97, 97 + 8))
	my_int= random.randint(1, 9999)
	toappend= str(my_char)  + "_"+ str(my_int)
	for j in range(0,5):
		f.write(toappend)
		f.write("\n")
	