import numpy as np
from sklearn.naive_bayes import GaussianNB
import os
import json
import glob

def discretize(latency):
	if latency < 2.0:
		return str(0)
	elif latency < 4.0:
		return str(1)
	elif latency < 6.0:
		return str(2)
	elif latency < 8.0:
		return str(3)
	else:
		return str(4)
def calc(phase):
	num_of_0s = 0
	correct = 0
	index = 0
	for j in y_pred:
		if j == phase:
			num_of_0s += 1
			if target[index] == phase:
				correct += 1
		index += 1
	actual_0s = 0
	for k in target:
		if k == phase:
			actual_0s += 1
	return (correct/float(num_of_0s), correct/float(actual_0s))





num_of_data = 0
for i in glob.glob("./diffbd/*.txt"):
	f = open(i, "r")
	try:
		x = json.load(f)
	except:
		continue
	num_of_data += 1
for i in glob.glob("./diffbd/*.json"):
	num_of_data += 1
data = np.zeros((num_of_data, 3))
target = np.zeros(num_of_data)
ind = 0
print num_of_data
#load data
for i in glob.glob("./diffbd/*.txt"):
	f = open(i, "r")
	try:
		x = json.load(f)
	except:
		continue
	target[ind] = discretize(x['latency'])
	if target[ind] > 50:
		ind += 1
		print "outlier!"
		continue
		
	data[ind][0] = x['size']
	data[ind][1] = x['rtt']
	data[ind][2] = i[9:13]
	ind  = ind + 1
for i in glob.glob("./diffbd/*.json"):
	f = open(i,"r")
	x = json.load(f)
	data[ind][0] = x['rtt*size']
	
	target[ind] = discretize(x['latency'])
	if target[ind] > 50:
		ind += 1
		print "outlier!"
		continue
	ind = ind + 1
#fit
gnb = GaussianNB()
y_pred = gnb.fit(data, target).predict(data)

print("overall precision:   %f " % (1 - (float(((target != y_pred).sum()))/float(num_of_data))))
phase = 0
print ("precision and recall on phase %d:" % phase )
print calc(phase)

