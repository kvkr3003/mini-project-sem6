import argparse
from subprocess import Popen
from p4utils.utils.topology import Topology
import time
import sys

# prev_list_normal=[]
# current_list_normal=[]
def main():
	prev_list=[]
	parser = argparse.ArgumentParser()
	parser.add_argument('--duration', nargs='?', type=int, default=40, help='Duration of traffic')
	args = parser.parse_args()
	duration= args.duration
	past_list= []
	iteration_number=0

	f= open('normal_ks.txt','w')
	start_time= time.time()
	try:
		while True:
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
			my_reg1 = required_array1.split(", ")
			# my_reg1=[]
			# for val in temp1:
			# 	my_reg1.append(val)
			for i in range(0,len(my_reg1)):
				my_reg1[i]= int(my_reg1[i])
			myfile1.close()

			myfile2=open("out2.txt","r")
			count2=0
			line2 = myfile2.readlines()
			# print(line)
			line_to_read2= line2[3]
			required_array2= line_to_read2[22:-1]
			my_reg2 = required_array2.split(", ")
			# my_reg2=[]
			# for val in temp2:
			# 	my_reg2.append(val)
			for i in range(0,len(my_reg2)):
				my_reg2[i]=int(my_reg2[i])
			myfile2.close()

			my_reg3=[]
			for i,j in zip(range(len(my_reg1)),range(len(my_reg2))):
				my_reg3.append([my_reg1[i],my_reg2[j]])

			# print(my_reg3)

			# if iteration_number==0:
			# 	a=2
			# else:
			if iteration_number!=0:
				#calculate current window distribution.
				curr_window=[]
				for i,j,k in zip(my_reg3,prev_list,past_list):
					temp_count= i[1]-j[1]
					current_count= 0.2*temp_count + 0.8*k[1]
					curr_window.append([i[0],current_count])

				for item in curr_window:
					# to_write1= str(item[0])
					# to_write2= str(item[1])
					# f.write("%s," %to_write1)
					# f.write("%s," %to_write2)
					f.write(str(str(item[0]) + ','))
					f.write(str(str(item[1]) + ','))

			#perform ks test ((o-e)^2)/e
			#write in a file the expected valuess.
			f.write("\n")
			prev_list=my_reg3
			if iteration_number==0:
				past_list= my_reg3
			else:
				past_list= curr_window
			iteration_number=iteration_number+1
	finally:
		pass
if __name__ == "__main__":
	main()
	# for i in my_reg3:
	# 	if i[1]>0:
	# 		print(i)
	# print("done")
