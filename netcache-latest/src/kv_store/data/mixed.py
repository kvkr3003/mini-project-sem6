

# read_file = open('zipf_sample_100000_05.txt', 'r')
# zipf_Lines = read_file.readlines()
# # print(zipf_Lines)
# write_file= open('mixed.txt','a')
# count=0
# for i in zipf_Lines:
# 	if count>50000:
# 		write_file.write(i)
# 	count=count+1

# attack_file=open('attack.txt','r')
# attack_lines=attack_file.readlines()
# print(attack_lines)
# for i in attack_lines:
# 	print("yes")
# 	write_file.write(i)

# count2=0

# for i in zipf_Lines:
# 	if count2>50000:
# 		write_file.write(i)
# 	count2=count2+1
mixed_file= open('mixed.txt','r')
mixed_lines= mixed_file.readlines()
counter=0
for i in mixed_lines:
	if i=="\n":
		print(counter)
	counter=counter+1



