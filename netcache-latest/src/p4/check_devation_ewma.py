import argparse
from subprocess import Popen
from p4utils.utils.topology import Topology
import time
import math

parser = argparse.ArgumentParser()
parser.add_argument('--duration', nargs='?', type=int, default=40, help='Duration of traffic')


args = parser.parse_args()
duration= args.duration

start_time= time.time()
pid_list = []

prev_list_normal=[]
current_list_normal=[]

iteration_number=0

f= open('attack.txt','w')

file_chisq= open('chi-sq-results.txt','w')


g=0
window_count= -1
while True:
	window_count= window_count + 1
	time.sleep(5)
	p1=(Popen("simple_switch_CLI --thrift-port 9090 < commands1.txt >out1.txt",shell=True))
	p1.wait()

	p2=(Popen("simple_switch_CLI --thrift-port 9090 < commands2.txt >out2.txt",shell=True))
	p2.wait()

	myfile1=open("out1.txt","r")
	count1=0
	line1 = myfile1.readlines()
	# print(line)
	line_to_read1= line1[3]
	required_array1= line_to_read1[21:-1]
	temp1= required_array1.split(", ")
	my_reg1=[]
	for val in temp1:
		my_reg1.append(val)
	
	myfile1.close()


	myfile2=open("out2.txt","r")
	count2=0
	line2 = myfile2.readlines()
	# print(line)
	line_to_read2= line2[3]
	required_array2= line_to_read2[22:-1]
	temp2= required_array2.split(", ")
	my_reg2=[]
	for val in temp2:
		my_reg2.append(val)
	
	myfile2.close()

	for i in range(0,len(my_reg1)):
		my_reg1[i]= int(my_reg1[i])

	for i in range(0,len(my_reg2)):
		my_reg2[i]=int(my_reg2[i])

	my_reg3=[]
	for i,j in zip(range(len(my_reg1)),range(len(my_reg2))):
		my_reg3.append([my_reg1[i],my_reg2[j]])


	# print(my_reg3)

	if iteration_number==0:
		a=2
	else:
		
		myfile_normal=open("normal.txt","r")
		line3= myfile_normal.readlines()
		# print(line_number)
		line_to_read3= line3[len(line3)-1]
		required_array3= line_to_read3[0:-2]
		temp3= required_array3.split(",")
		normal_bl_code={}
		normal_list=[]
		# print(temp3)
		for i in range(0,len(temp3)):
			# print(temp3[i])
			temp3[i]= int(float(temp3[i]))
			# print(temp3[i])
		for i in range(0,len(temp3)-1,2):
			if temp3[i+1]>0:
				normal_bl_code[temp3[i]]=temp3[i+1]
				normal_list.append(temp3[i])
				# print(temp3[i],temp3[i+1])

		#calculate current window distribution.
		actual_bl_code={}
		actual_list=[]
		curr_window=[]
		for i,j in zip(my_reg3,prev_list):
			temp_count= i[1]-j[1]
			current_count= temp_count
			curr_window.append([i[0],current_count])
			if current_count>0:
				actual_bl_code[i[0]]=current_count
				actual_list.append(i[0])


		

		#perform chi square with normal


		normal_only_list= [x for x in normal_list if x not in actual_list]
		actual_only_list= [x for x in actual_list if x not in normal_list]
		nrml_atck_int= set(normal_list).intersection(actual_list)

		

		# print(normal_list)

		# print(actual_list)

		#chi square test
		chi_sq_normal=0

		for i in nrml_atck_int:
			observed_value= actual_bl_code[i]
			expected_value= normal_bl_code[i]
			squared_val = (observed_value-expected_value)*(observed_value-expected_value)
			val_to_add= squared_val/expected_value
			chi_sq_normal=chi_sq_normal+val_to_add

		for i in normal_only_list:
			observed_value= 0
			expected_value= normal_bl_code[i]
			squared_val = (observed_value-expected_value)*(observed_value-expected_value)
			val_to_add= squared_val/expected_value
			chi_sq_normal=chi_sq_normal+val_to_add
			

		for i in actual_only_list:
			observed_value= actual_bl_code[i]
			expected_value= 1
			squared_val = (observed_value-expected_value)*(observed_value-expected_value)
			val_to_add= squared_val/expected_value
			chi_sq_normal=chi_sq_normal+val_to_add

		union_val= len(normal_list)+len(actual_list)-len(nrml_atck_int)
		if union_val>0:
			print("################ Normal chi square ################ ")
			print("Window: ",window_count)
			print(window_count,chi_sq_normal,union_val)


		# printing_message= "Chi square results"
		# message_to_write= "Chi square results" + str(line_number) + "," str(chi_sq_normal) + "," + str(union_val)
		file_chisq.write("chi square results--> ")
		file_chisq.write("Current window is ")
		file_chisq.write(str(window_count))
		file_chisq.write(" ")
		file_chisq.write("Value for chi square is ")
		file_chisq.write(str(chi_sq_normal))
		file_chisq.write(" ")
		file_chisq.write("Total number of equivalence classes ")
		file_chisq.write(str(union_val))
		file_chisq.write("\n")
		# f.write("%s,", message_to_write)
		


		# numerator_rmse=0


		# for i in nrml_atck_int:
		# 	observed_value= actual_bl_code[i]
		# 	expected_value= normal_bl_code[i]
		# 	squared_val = (observed_value-expected_value)*(observed_value-expected_value)
		# 	numerator_rmse= numerator_rmse + squared_val

		# for i in normal_only_list:
		# 	observed_value= 0
		# 	expected_value= normal_bl_code[i]
		# 	squared_val = (observed_value-expected_value)*(observed_value-expected_value)
		# 	numerator_rmse= numerator_rmse + squared_val
			

		# for i in actual_only_list:
		# 	observed_value= actual_bl_code[i]
		# 	expected_value= 0
		# 	squared_val = (observed_value-expected_value)*(observed_value-expected_value)
		# 	numerator_rmse= numerator_rmse + squared_val


		# total_rmse_ans= numerator_rmse/(len(normal_list)+len(actual_list)-len(nrml_atck_int))
		# rmse= math.sqrt(total_rmse_ans)

		# print(line_number,rmse)
		

			


		
		for item in curr_window:
			to_write1= str(item[0])
			to_write2= str(item[1])
			f.write("%s," %to_write1)
			f.write("%s," %to_write2)



		#perform chi sqaure test ((o-e)^2)/e
		#write in a file the chi value.
	f.write("\n")
	prev_list=my_reg3
	iteration_number=iteration_number+1
	print("\n")





for pid in pid_list:
    pid.wait()


# for i in my_reg3:
# 	if i[1]>0:
# 		print(i)
print("done")
