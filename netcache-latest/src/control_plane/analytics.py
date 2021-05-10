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

f= open('table.txt','w')
p1=(Popen("simple_switch_CLI --thrift-port 9090 < input.txt >out1.txt",shell=True))
p1.wait()

for pid in pid_list:
    pid.wait()


# for i in my_reg3:
# 	if i[1]>0:
# 		print(i)
print("done")
