from csv import reader
from math import exp

class LogisticRegression:
    def __init__(self, filename, learning_rate=0.1, number_epoch=50):
        self.dataset = self.open_file(filename)
        self.epoch = number_epoch
        self.learning_rate = learning_rate

    # actually does the regression which is a classification
    def logistic_regression(self):
        predictions = list()
        self.normalize()
        b = self.get_coef_vector()
        for row in self.dataset:
            p = self.predict(row, b)
            predictions.append(p)
        classifications = [round(p) for p in predictions]
        return predictions, classifications

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

    # get the b vector from the tutorial
    def get_coef_vector(self):
        b = [0.0 for i in enumerate(self.dataset[0])]
        for epoch in range(self.epoch):
            for x in self.dataset:
                dy = self.predict(x, b)
                b[0] = b[0] + self.learning_rate*(x[-1]-dy)*dy*(1.0 - dy)
                for i in range(len(x)-1):
                    b[i+1] = b[i+1] + self.learning_rate*(x[-1]-dy)*dy*(1.0 - dy)*x[i]
        return b

    # normalizes test set on csv to be between 0 and 1
    def normalize(self):
        extremes = list()
        for i in range(len(self.dataset[0])):
            cols = [row[i] for row in self.dataset]
            extremes.append([min(cols), max(cols)])

        for row in self.dataset:
            for i in range(len(row)):
                minv = extremes[i][0]
                maxv = extremes[i][1]
                if maxv == minv: maxv += 1 #avoid zero division
                row[i] = (row[i] - minv) / (maxv - minv)

    def open_file(self, filename):
        test_set = list()
        with open(filename, 'r') as file:
            csv_reader = reader(file)
            for row in csv_reader:
                if row: test_set.append(row)
        return test_set

    def accuracy(self, actual, predicted):
        correct = 0
        for i, act in enumerate(actual):
            if act == predicted[i]: correct += 1
        return correct, correct/float(len(actual))*100.0

    def run(self):
        for i, el in enumerate(self.dataset[0]):
            for row in self.dataset:
                row[i] = float(row[i].strip())
        predictions, classification = self.logistic_regression()
        actual = [row[-1] for row in self.dataset]
        cclass, accuracy = self.accuracy(actual, classification)
        print('Classification: {0}'.format(classification))
        print('(Correct: {0}, Incorrect: {1})'.format(cclass, len(classification)-cclass))
        print('Accuracy: {0}%'.format(accuracy))

lr = LogisticRegression('notas.csv')
lr.run()