import random

f1 = open("zipf_sample_100000_05.txt")
f2 = open("attack.txt", "r")
f = open("merge_zipf_attack.txt", "w")

f1_lines = f1.readlines()

f2_lines = f2.readlines()

count = 0

temp = random.randint(0, 3*len(f1_lines)//4)

for i in range(temp):
	f.write(f1_lines[i])

for i in range(temp, temp+len(f1_lines)//4):
	temp1 = random.randint(0, 4)
	if temp1 == 1:
		f.write(f1_lines[i])
	else:
		f.write(f2_lines[i])
		count+=1

for i in range(temp+len(f1_lines)//4, len(f1_lines)):
	f.write(f1_lines[i])

print('no. of attack queries merged =' + str(count))