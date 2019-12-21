import numpy as np
import nn

a = np.loadtxt('A', usecols=range(5))
b = np.loadtxt('B', usecols=range(5))
mystery = np.loadtxt('mystery', usecols=range(5))

mysteryArray = list()
aArray = list()
bArray = list()
for i in range(5):
    mysteryArray.append(np.reshape(mystery[5*i:5*(i+1)], (1, 25)))
    aArray.append(np.reshape(a[5*i:5*(i+1)], (1, 25)))
    bArray.append(np.reshape(b[5*i:5*(i+1)], (1, 25)))

training_data = aArray[0]
for i in range(1,5):
    #print(training_data.shape, aArray[i].shape)
    training_data = np.concatenate((training_data, aArray[i]))
for i in range(5):
    training_data = np.concatenate((training_data, bArray[i]))

test_mystery = mysteryArray[0]
for i in range(1,5):
    test_mystery = np.concatenate((test_mystery, mysteryArray[i]))

training_data = training_data.T
training_labels = np.array([0,0,0,0,0,1,1,1,1,1])
test_mystery = test_mystery.T

nn.runOn(training_data, training_labels, test_mystery)