import numpy as np
import scipy.special
import math

def runOn(training_data, labels, mystery_data):
    w, bias = init(training_data.shape[0])
    w, bias = train(w,bias,training_data,labels)
    mystery_predictions, confidence = predict(w, bias, mystery_data)
    print(mystery_predictions)
    num = 100000
    confidence_rounded = [abs(math.floor(max(1 - data, data)*num)/num) for data in confidence[0]]
    print(confidence_rounded) #not actually confidence, just log representations

def init(shape):
    w = np.random.rand(shape,1)
    bias = np.random.random()
    return w, bias
    
def prop(w, bias, data, labels):
    prob = scipy.special.expit(np.dot(w.T,data)+bias)
    loss = (-1/data.shape[1])*np.sum((labels*np.log(prob)) + ((1-labels)*np.log(1-prob)))
    w_d = (1/data.shape[1])*(np.dot(data,np.subtract(prob,labels).T))
    bias_d = (1/data.shape[1])*(np.sum(prob-labels))
    return loss, w_d, bias_d

def train(w, bias, data, labels):
    lr = 0.3
    runs = 100000
    for i in range(runs):
        loss, w_d, bias_d = prop(w, bias, data, labels)
        w -= w_d * lr
        bias -= bias_d * lr
    return w, bias

def predict(w, bias, data):
    prediction = np.zeros((1,data.shape[1]))
    w = w.reshape(data.shape[0],1)
    prob = scipy.special.expit(np.dot(w.T,data)+bias)
    for i in range(data.shape[1]):
        prediction[0, i] = math.floor(prob[0, i] + 0.5)
    return prediction, prob