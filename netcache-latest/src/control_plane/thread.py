# # import multiprocessing
# # import psutil
# # import random

# # def iHateThis():
# #     tab = []
# #     for i in range(100000):
# #         tab.append(random.randint(1, 10000))
# #     tab.sort()
# #     return tab;

# # hate = multiprocessing.Process(name='hate', target=iHateThis)
# # hate.start()

# # while(True):
# #     currentProcess = psutil.Process()
# #     print(currentProcess.cpu_percent(interval=5))

# #!/usr/bin/env python
# """
# Produces load on all available CPU cores

# Updated with suggestion to prevent Zombie processes
# Linted for Python 3
# Source: 
# insaner @ https://danielflannery.ie/simulate-cpu-load-with-python/#comment-34130
# """
# import time
# import math
# import multiprocessing
# import threading 
# from threading import Thread
# import struct
# import random
# import socket

# def multiprocessing_func1(x):
# 	# a=2
# 	print("start1")
# 	starttime = time.time()
# 	for i in range(1,x):
# 		for j in range(1,x):
# 			for k in range(1,x):
# 				for l in range(1,x):
# 					for m in range(1,x):
# 						a= math.sqrt(4)
# 	duration = time.time() - starttime
# 	print("end1")
# 	print(duration)



# def multiprocessing_func2(x):
# 	# a=2
# 	print("start2")
# 	starttime = time.time()
# 	for i in range(1,x):
# 		for j in range(1,x):
# 			for k in range(1,x):
# 				for l in range(1,x):
# 					for m in range(1,x):
# 						a= math.sqrt(4)
# 	duration = time.time() - starttime
# 	print("end2")
# 	print(duration)

# def multiprocessing_func3(x):
# 	# a=2
# 	print("start3")
# 	starttime = time.time()
# 	for i in range(1,x):
# 		for j in range(1,x):
# 			for k in range(1,x):
# 				for l in range(1,x):
# 					for m in range(1,x):
# 						a= math.sqrt(4)
# 	duration = time.time() - starttime
# 	print("end3")
# 	print(duration)

# def multiprocessing_func4(x):
# 	# a=2
# 	print("start4")
# 	starttime = time.time()
# 	for i in range(1,x):
# 		for j in range(1,x):
# 			for k in range(1,x):
# 				for l in range(1,x):
# 					for m in range(1,x):
# 						a= math.sqrt(4)
# 	duration = time.time() - starttime
# 	print("end4")
# 	print(duration)




    
# if __name__ == '__main__':

# 	x=40
	
# 	starttime= time.time()

# 	fun1=threading.Thread(target=multiprocessing_func1(x)).start()
# 	fun2=threading.Thread(target=multiprocessing_func2(x)).start()
#  	fun3=threading.Thread(target=multiprocessing_func3(x)).start()
# 	fun4=Thread(target=multiprocessing_func4(x)).start()



# 	# fun1.join()
# 	# fun2.join()
# 	# fun3.join()
# 	# fun4.join()

# 	print(time.time()-starttime)


# 	# controller=Thread(target = NCacheController('s1').main())
#  #    my_function=Thread(target = func2)

    

#  #    controller.start()
#  #    my_function.start()

#  #    controller.join()
#  #    my_function.join()


import time
import threading
import random
import os
import time
import psutil
from threading import Thread
import struct
import random

rocket = 0
start_time= time.time()

def func1():
    global rocket
    print('start func1')
    begin_time= time.time()
    a=2
    for i in range(1,1000):
    	for j in range(1,1000):
    		for k in range(1,100):
    			a=a+1
    
    print ('end func1')
    print("Duration of func1 is", time.time()-begin_time)

def func2():
    global rocket
    begin_time= time.time()
    a=0
    for i in range(1,1000):
    	for j in range(1,1000):
            for k in range(1,100):
                a=a+1
    print ('start func2')
    print ('end func2')

    print("Duration of func2 is", time.time()-begin_time)


if __name__=='__main__':
	# temp_time= time.time()
    p1 = threading.Thread(target=func1)
    p2 = threading.Thread(target=func2)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    curr_pid= os.getpid()
    proc = psutil.Process(curr_pid)
    treads_list = proc.threads()

    print(len(treads_list))

    for i in treads_list:
        # print(i.cpu_percent())
        o = i[0]
        print(o)
        th = psutil.Process(o)
        # thread_file.write(str(th))
        cpu_perc= th.cpu_percent(interval=1)
        # cpu_perc=get_threads_cpu_percent(th,1)
        # cpu_perc = 0
        # thread_file.write("\n")
        # thread_file.write(str(cpu_perc))
        # thread_file.write("\n")
        print('PID %s use %% CPU = %s' % (o, cpu_perc))

    
    print("Execution time is",time.time()-start_time)

    
# if __name__=='__main__':
# 	# temp_time= time.time()
#     func1()
#     func2()



# thread_test.py
