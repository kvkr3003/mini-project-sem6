from itertools import izip
import matplotlib.pyplot as plt 

file1= open('s1-out1.log','r')


list_count=[0]* 3200000


dict={'a':10,'b':11,'c':12,'d':13,'e':14,'f':15,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'0':0}
for line1 in file1:
	bl_code=line1[-8:]
	ans1=0
	for i in bl_code:
		if i!='\n':
			ans1= ans1*16 + dict[i]
	print(ans1)
	list_count[ans1]=list_count[ans1] + 1;
	# print(ans1)


number_of_eq_classes=0
for i in list_count:
	if i>0:
		number_of_eq_classes= number_of_eq_classes + 1;
print(" number_of_eq_classes are", number_of_eq_classes);

BL_Codes= []
frequency=[]

for i in range(0,3200000):
	if list_count[i]>0:
		print(i,list_count[i]);
		BL_Codes.append(i)
		frequency.append(list_count[i])

# print(BL_Codes)
# print(frequency)

plt.hist(frequency, BL_Codes, range, color = 'green', 
        histtype = 'bar', rwidth = 0.8) 
  
# x-axis label 
plt.xlabel('BL_Codes') 
# frequency label 
plt.ylabel('frequency') 
# plot title 
plt.title('My histogram') 
  
# function to show the plot 
plt.show() 