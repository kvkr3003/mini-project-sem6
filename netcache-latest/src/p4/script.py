from itertools import izip

file1= open('s1-out1.log','r')


list_count=[0]* 100000000


dict={'a':10,'b':11,'c':12,'d':13,'e':14,'f':15,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'0':0}
for line1 in file1:
	bl_code=line1[-8:]
	ans1=0
	for i in bl_code:
		if i!='\n':
			ans1= ans1*16 + dict[i]
	list_count[ans1]=list_count[ans1] + 1;


number_of_eq_classes=0
for i in list_count:
	if i>0:
		number_of_eq_classes= number_of_eq_classes + 1;
print(" number_of_eq_classes are", number_of_eq_classes);

for i in range(0,100000000):
	if list_count[i]>0:
		print("Number of packets taking Path", i,"==>", list_count[i])