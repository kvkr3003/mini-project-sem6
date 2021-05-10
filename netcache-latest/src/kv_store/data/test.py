read_file = open('inserted.txt', 'r')
inserted_lines = read_file.readlines()

read_file1 = open('zipf_sample_60000_05.txt', 'r')
zipf_Lines = read_file1.readlines()

read_file2 = open('deleted.txt', 'r')
deleted_lines = read_file2.readlines()

number_of_legitimate_deleted=0
#find percent of legitimate items that were removed from cache
leg_interserction_cache=[]
for i in inserted_lines:
	if i in zipf_Lines:
		leg_interserction_cache.append(i)

# print(leg_interserction_cache)

# print(deleted_lines)

for i in leg_interserction_cache:
	if i in deleted_lines:
		print(i)
		number_of_legitimate_deleted= number_of_legitimate_deleted + 1

# print(len(leg_interserction_cache))

# print(float(5)/float(2))
perc=  100*(float(number_of_legitimate_deleted)/float(len(leg_interserction_cache)))
print("Number of legitimate items are", len(leg_interserction_cache))

print("Percentage of legitimate items deleted", perc)
	