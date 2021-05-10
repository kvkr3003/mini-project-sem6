

# read_file = open('zipf_sample_100000_05.txt', 'r')
# zipf_Lines = read_file.readlines()
# # print(zipf_Lines)
# write_file= open('mixed.txt','a')
# count=0
# for i in zipf_Lines:
# 	if count>50000:
# 		break
# 	write_file.write(i)
# 	count=count+1

# attack_file=open('attack.txt','r')
# attack_lines=read_file.readlines()
# print(attack_lines)
# for i in attack_lines:
# 	print("yes")
# 	write_file.write(i)


# dataset_file=open('dataset.txt','r')
# dataset_lines=dataset_file.readlines()


# temp_file=open('temp.txt','r')
# temp_lines=temp_file.readlines()
# f= open("dataset.txt",'a')
# for i in temp_lines:
# 	currstring=""
# 	for j in i:
# 		if j=="=":
# 			break
# 		currstring= currstring + j
# 	f.write(currstring)
# 	f.write("\n")

# key_bank_file= open("key-bank.txt","r")
# key_bank_lines= key_bank_file.readlines()


# count2=0

# for i in zipf_Lines:
# 	if count2>50000:
# 		write_file.write(i)
# 	count2=count2+1

# filenames = ["server1.txt","server2.txt","server3.txt","server4.txt","server5.txt","server6.txt","server7.txt","server8.txt"]
# with open("key-bank.txt", "w") as outfile:
# 	for filename in filenames:
# 		with open(filename) as infile:
# 			contents = infile.read()
# 			outfile.write(contents)
# count=0
# with open('dataset.txt') as myfile:
# 	for i in dataset_lines:
# 		# print(i)
# 		if i in key_bank_lines:
# 			count=count+1
# 		else:
# 			print(i)
		

# print(count)



data_set= open("dataset2.txt","w")


read_file = open('zipf_sample_100000_05.txt', 'r')
zipf_Lines = read_file.readlines()

attack_file=open('attack.txt','r')
attack_lines=attack_file.readlines()


zip_file_ptr=0
attack_file_ptr=0

total_items=0

# cache initialisation purpose
while total_items<5000:
	data_set.write(zipf_Lines[zip_file_ptr])
	zip_file_ptr= zip_file_ptr + 1
	total_items= total_items + 1


#mixed the attack data with zipf distribution
while total_items < 30000:
	for i in range(1,21):
		data_set.write(attack_lines[attack_file_ptr])
		attack_file_ptr = attack_file_ptr + 1
	for i in range(1,6):
		data_set.write(zipf_Lines[zip_file_ptr])
		zip_file_ptr= zip_file_ptr + 1

	total_items = total_items + 25

# now introduced only attack queries for cache eviction

while total_items<40000:
	data_set.write(attack_lines[attack_file_ptr])
	attack_file_ptr = attack_file_ptr + 1
	total_items= total_items + 1


# these zipf distribution should follow the expecnsive cpu path due to cache eviction.

while total_items < 50000:
	data_set.write(zipf_Lines[zip_file_ptr])
	zip_file_ptr= zip_file_ptr + 1
	total_items= total_items + 1 





print(total_items)