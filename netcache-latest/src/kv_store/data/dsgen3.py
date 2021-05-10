

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

total_legitimate_count = input ("Enter total number of legitimate items :")
total_attack_count= input("Enter total number of attack items: ")

total_items = total_legitimate_count + total_attack_count

data_set= open("dataset.txt","w")


read_file = open('zipf_sample_60000_05.txt', 'r')
zipf_Lines = read_file.readlines()

my_list=[]


attack_file=open('attack.txt','r')
attack_lines=attack_file.readlines()


zip_file_ptr=0
attack_file_ptr=0

current_items=0

# cache initialisation purpose
while current_items< 0.30*total_items:
	data_set.write(zipf_Lines[zip_file_ptr])
	zip_file_ptr= zip_file_ptr + 1
	current_items= current_items + 1
	total_legitimate_count= total_legitimate_count - 1
	if zipf_Lines[zip_file_ptr] not in my_list:
		my_list.append(zipf_Lines[zip_file_ptr])



while current_items < 0.50*total_items:
		data_set.write(attack_lines[attack_file_ptr])
		attack_file_ptr = attack_file_ptr + 1
		total_attack_count= total_attack_count - 1 
		current_items= current_items + 1


		# data_set.write(zipf_Lines[zip_file_ptr])
		# zip_file_ptr= zip_file_ptr + 1
		# total_legitimate_count= total_legitimate_count - 1 
		# current_items= current_items + 1
		# if zipf_Lines[zip_file_ptr] not in my_list:
		# 	my_list.append(zipf_Lines[zip_file_ptr])
			

print(current_items,total_attack_count,total_legitimate_count)

while current_items< 0.625*total_items:
	data_set.write(zipf_Lines[zip_file_ptr])
	zip_file_ptr= zip_file_ptr + 1
	current_items= current_items + 1
	total_legitimate_count= total_legitimate_count - 1
	data_set.write(attack_lines[attack_file_ptr])
	attack_file_ptr = attack_file_ptr + 1
	total_attack_count= total_attack_count - 1 
	current_items= current_items + 1
	if zipf_Lines[zip_file_ptr] not in my_list:
		my_list.append(zipf_Lines[zip_file_ptr])

# total_items= 0.5*total_items

# now introduced only attack queries for cache eviction

# while current_items<0.85*total_items and total_attack_count>0:
# 	data_set.write(attack_lines[attack_file_ptr])
# 	attack_file_ptr = attack_file_ptr + 1
# 	current_items= current_items + 1
# 	total_attack_count= total_attack_count-1


print(current_items,total_attack_count,total_legitimate_count)
# total_items=0.75*total_items


# these zipf distribution should follow the expecnsive cpu path due to cache eviction.

while current_items < total_items and total_legitimate_count>0:
	data_set.write(zipf_Lines[zip_file_ptr])
	zip_file_ptr= zip_file_ptr + 1
	current_items= current_items + 1 
	total_legitimate_count= total_legitimate_count - 1
	if zipf_Lines[zip_file_ptr] not in my_list:
		my_list.append(zipf_Lines[zip_file_ptr])
		


print("Number of distinct items are", len(my_list))
# print(my_list)
print(current_items,total_attack_count,total_legitimate_count)
