read_file1 = open('zipf_sample_60000_05.txt', 'r')
zipf_Lines = read_file1.readlines()

current_list=[]
for i in zipf_Lines:
	if i in current_list:
		a=2
	else:
		current_list.append(i)

print(len(current_list))