# from __future__ import division
import argparse, numpy
import matplotlib.pyplot as plt
from subprocess import Popen
from p4utils.utils.topology import Topology
import time
import math

def plot_graph(x, y, xlabel, ylabel, title):
    plt.plot(x, y, 'r')
    # plt.plot(x[1], y[1], 'g')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(str(title + '.png'))

def ks_test(expected, actual):
	actual = numpy.array(actual)
	actual = actual/(float)(numpy.sum(actual))
	expected = numpy.array(expected)
	expected = expected/(float)(numpy.sum(expected))

	cumulative_exp = numpy.cumsum(expected)
	cumulative_act = numpy.cumsum(actual)
	diff = numpy.abs(cumulative_act - cumulative_exp)
	max_diff = numpy.max(diff)
	return max_diff

def expected_list():
	myfile_normal=open("normal_ks.txt","r")
	line3= myfile_normal.readlines()
	# print(line_number)
	line_to_read3= line3[len(line3)-1]
	required_array3= line_to_read3[0:-2]
	temp3= required_array3.split(",")
	normal_bl_code={}
	normal_list=[]
	for i in range(0,len(temp3)):
		temp3[i]= int(float(temp3[i]))
	for i in range(0,len(temp3)-1,2):
		if temp3[i+1]>0:
			normal_bl_code[temp3[i]]=temp3[i+1]
			normal_list.append(temp3[i])
	return normal_bl_code, normal_list

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--duration', nargs='?', type=int, default=40, help='Duration of traffic')
	args = parser.parse_args()
	duration= args.duration
	iteration_number=0

	f= open('attack.txt','w')
	# temp = open('temp.txt','w')
	temp1 = open('temp1.txt','w') # for storing the final ks result list
	# file_ks= open('chi-sq-results.txt','w')
	file_ks= open('ks-results.txt','w')
	normal_bl_code, normal_list = expected_list()
	start_time= time.time()
	ks_result_list = []
	chi_result_list = []
	window_count= -1
	try:
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
			line_to_read1= line1[3]
			required_array1= line_to_read1[21:-1]
			my_reg1= required_array1.split(", ")
			for i in range(0,len(my_reg1)):
				my_reg1[i]= int(my_reg1[i])
			myfile1.close()


			myfile2=open("out2.txt","r")
			count2=0
			line2 = myfile2.readlines()
			# print(line)
			line_to_read2= line2[3]
			required_array2= line_to_read2[22:-1]
			my_reg2= required_array2.split(", ")
			for i in range(0,len(my_reg2)):
				my_reg2[i]=int(my_reg2[i])
			myfile2.close()


			my_reg3=[]
			for i,j in zip(range(len(my_reg1)),range(len(my_reg2))):
				my_reg3.append([my_reg1[i],my_reg2[j]])
			if iteration_number!=0:
				packets_seen=0

				#calculate current window distribution.
				actual_bl_code={}
				actual_list=[]
				curr_window=[]
				for i,j in zip(my_reg3,prev_list):
					temp_count= i[1]-j[1]
					current_count= temp_count
					packets_seen += temp_count
					curr_window.append([i[0],current_count])
					if current_count>0:
						actual_bl_code[i[0]]=current_count
						actual_list.append(i[0])

				normal_only_list= [x for x in normal_list if x not in actual_list]
				actual_only_list= [x for x in actual_list if x not in normal_list]
				nrml_atck_int= set(normal_list).intersection(actual_list)
				# temp.write(str(normal_only_list))
				# temp.write(str(actual_only_list))
				# temp.write(str(nrml_atck_int))
				# temp.write('\n')

				expected = []
				actual = []
				for i in nrml_atck_int:
					actual.append(actual_bl_code[i])
					expected.append(normal_bl_code[i])
				for i in normal_only_list:
					actual.append(0)
					expected.append(normal_bl_code[i])
				for i in actual_only_list:
					actual.append(actual_bl_code[i])
					expected.append(1)
				# temp1.write(str(expected))
				# temp1.write(str(actual))
				# temp1.write('\n')
				try:
					#perform ks test 
					#write in a file the result of ks_test.
					ks_result = ks_test(expected, actual)
				except:
					continue

				union_val= len(normal_list)+len(actual_list)-len(nrml_atck_int)
				if union_val>0:
					print("################ ks_test ################ ")
					print("Window: ",window_count)
					print(window_count,ks_result,union_val)

				file_ks.write("ks results--> ")
				file_ks.write("Current window is ")
				file_ks.write(str(window_count))
				file_ks.write(" ")
				file_ks.write("deviaton from ks test is ")
				file_ks.write(str(ks_result))
				file_ks.write(" ")
				file_ks.write("Total number of equivalence classes ")
				file_ks.write(str(union_val))
				file_ks.write("\n")
				ks_result_list.append(ks_result)
				# f.write("%s,", message_to_write)

				''' 
				the below part was used to compare the results of ks test with initially available chi square test
				since, we have verified it, we are commenting it and proceeding with kstest and commenting the chi square part
				'''
				# chi_sq_normal=0

				# for i in nrml_atck_int:
				# 	observed_value= actual_bl_code[i]
				# 	expected_value= normal_bl_code[i]
				# 	squared_val = (observed_value-expected_value)*(observed_value-expected_value)
				# 	val_to_add= squared_val/expected_value
				# 	chi_sq_normal=chi_sq_normal+val_to_add

				# for i in normal_only_list:
				# 	observed_value= 0
				# 	expected_value= normal_bl_code[i]
				# 	squared_val = (observed_value-expected_value)*(observed_value-expected_value)
				# 	val_to_add= squared_val/expected_value
				# 	chi_sq_normal=chi_sq_normal+val_to_add

				# # for i in actual_only_list:
				# # 	observed_value= actual_bl_code[i]
				# # 	expected_value= 1
				# # 	squared_val = (observed_value-expected_value)*(observed_value-expected_value)
				# # 	val_to_add= squared_val/expected_value
				# # 	chi_sq_normal=chi_sq_normal+val_to_add
				# chi_result_list.append(chi_sq_normal)
				# if union_val>0:
				# 	print("################ Normal chi square ################ ")
				# 	print("Window: ",window_count)
				# 	print(window_count,chi_sq_normal,union_val)


				# # printing_message= "Chi square results"
				# # message_to_write= "Chi square results" + str(line_number) + "," str(chi_sq_normal) + "," + str(union_val)
				# file_ks.write("chi square results--> ")
				# file_ks.write("Current window is ")
				# file_ks.write(str(window_count))
				# file_ks.write(" ")
				# file_ks.write("Value for chi square is ")
				# file_ks.write(str(chi_sq_normal))
				# file_ks.write(" ")
				# file_ks.write("Total number of equivalence classes ")
				# file_ks.write(str(union_val))
				# file_ks.write("\n\n")
				# # f.write("%s,", message_to_write)

				for item in curr_window:
					f.write(str(str(item[0]) + ','))
					f.write(str(str(item[1]) + ','))

			f.write("\n")
			prev_list=my_reg3
			iteration_number=iteration_number+1
			print("\n")
	finally:
		temp1.write(str(ks_result_list))
		# temp1.write('\n')
		# temp1.write(str(chi_result_list))
		try:
			plot_graph(range(1, len(ks_result_list) + 1), ks_result_list,'window number','ks deviation','ks deviation plot')
		except:
			print("since the program was not ended as soon as the workload is done, due to appending of inapporpriate values to list, error occured in graph plotting")
		# plot_graph(range(1, window_count), chi_result_list,'window number','chi value','chi square plot')
if __name__ == "__main__":
	main()

