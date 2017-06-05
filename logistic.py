import csv
from math import exp

class LogisticRegression:
    def __init__(self, dataset, train, test, learning_rate=0.1, number_epoch=100):
        self.dataset = dataset
        self.train = self.open_file(train)
        self.test = self.open_file(test)
        self.epoch = number_epoch
        self.learning_rate = learning_rate

    # actually does the regression which is a classification
    def logistic_regression(self):
        predictions = list()
        self.normalize(self.test)
        b = self.optimal_b_coef()
        for row in self.test:
            p = self.predict(row, b)
            predictions.append(p)
        classifications = [round(p) for p in predictions]
        return b, predictions, classifications

    # sigmoid function to avoid math error on 1/(1 + exp(-gamma))
    def sigmoid(self, gamma):
        if gamma < 0:
            return 1 - 1/(1 + exp(gamma))
        else:
            return 1/(1 + exp(-gamma))
    
    # get the prediction value
    def predict(self, x, b):
        gamma = b[0]
        for i in range(len(x)-1):
            gamma += b[i+1]*x[i]
        return self.sigmoid(gamma)

    def optimal_b_coef(self):
        self.normalize(self.train)
        b = [0.0 for i in enumerate(self.train[0])]
        for epoch in range(self.epoch):
            for x in self.train:
                dy = self.predict(x, b)
                b[0] = b[0] + self.learning_rate*(x[-1]-dy)*dy*(1.0 - dy)
                for i in range(len(x)-1):
                    b[i+1] = b[i+1] + self.learning_rate*(x[-1]-dy)*dy*(1.0 - dy)*x[i]
        return b

    # normalizes test set on csv to be between 0 and 1
    def normalize(self, dataset):
        extremes = list()
        for i in range(len(dataset[0])):
            cols = [row[i] for row in dataset]
            extremes.append([min(cols), max(cols)])

        for row in dataset:
            for i in range(len(row)):
                minv = extremes[i][0]
                maxv = extremes[i][1]
                if maxv == minv: maxv += 1 #avoid zero division
                row[i] = (row[i] - minv) / (maxv - minv)

    def open_file(self, filename):
        test_set = list()
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row: test_set.append(row)
        return test_set

    def accuracy(self, actual, predicted):
        correct = 0
        for i, act in enumerate(actual):
            if act == predicted[i]: correct += 1
        return correct, correct/float(len(actual))*100.0

    def run(self):
        for i, el in enumerate(self.train[0]):
            for row in self.train:
                row[i] = float(row[i].strip())
        for i, el in enumerate(self.test[0]):
            for row in self.test:
                row[i] = float(row[i].strip())
        b, predictions, yguess = self.logistic_regression()
        ytrain = [row[-1] for row in self.train]
        ytest  = [row[-1] for row in self.test]
        correct = [0, 0]
        for i, yhat in enumerate(ytest):
            if yhat == yguess[i]: 
                if yhat == 0:
                    correct[0] += 1
                else:
                    correct[1] += 1
        print('Dataset: {0}'.format(self.dataset))
        print('Optimal b vector: {0}'.format(b))
        print('----------------')
        print('Number of No examples in test: {0}'.format(ytest.count(0)))
        print('Number of Yes examples in test: {0}'.format(ytest.count(1)))
        print('----------------')
        print('Number of examples classified as No: {0}'.format(yguess.count(0)))
        print('Number of examples correctly classified as No: {0}'.format(correct[0]))
        print('----------------')
        print('Number of examples classified as Yes: {0}'.format(yguess.count(1)))
        print('Number of examples correctly classified as Yes: {0}'.format(correct[1]))
        print('----------------')
        print('Total Precision: {0:.4f} percent'.format(100*(correct[1]+correct[0]) / (ytest.count(0)+ytest.count(1))))
        print('Yes Precision: {0:.4f} percent'.format(100*correct[1]/yguess.count(1)))
        print('No Precision: {0:.4} percent'.format(100*correct[0]/yguess.count(0)))


lr = LogisticRegression('occupancy','datasets/occupancy_training.csv','datasets/occupancy_test.csv')
lr.run()