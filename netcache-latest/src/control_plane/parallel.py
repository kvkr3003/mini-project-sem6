import os
import psutil
from psutil import getloadavg

# Getting loadover15 minutes

print(os.cpu_count())
# load1, load5, load15 = psutil.getloadavg()

# cpu_usage = (load15/os.cpu_count()) * 100

# print("The CPU usage is : ", cpu_usage)
