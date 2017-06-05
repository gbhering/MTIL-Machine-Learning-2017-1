import csv
from math import exp

class Statistics:
    def __init__(self, ytest, yguess):
        self.ytest = ytest
        self.yguess = yguess
        self.number_of_correct_no, self.number_of_correct_yes = self.get_correct_classification()
        self.number_classified_no, self.number_classified_yes = self.get_classification()
        self.number_of_no = self.get_number_of_no()
        self.number_of_yes = self.get_number_of_yes()

    def get_correct_classification(self):
        correct = [0, 0]
        for i, yhat in enumerate(self.ytest):
            if yhat == self.yguess[i]: 
                if yhat == 0:
                    correct[0] += 1
                else:
                    correct[1] += 1
        number_of_correct_no = correct[0]
        number_of_correct_yes = correct[1]
        return number_of_correct_no, number_of_correct_yes

    def get_classification(self):
        number_classified_no = self.yguess.count(0)
        number_classified_yes = self.yguess.count(1)
        return number_classified_no, number_classified_yes

    def get_number_of_yes(self):
        number_of_yes = self.ytest.count(1)
        return number_of_yes

    def get_number_of_no(self):
        number_of_no = self.ytest.count(0)
        return number_of_no

    def get_precision(self):
        return 100*(self.number_of_correct_yes+self.number_of_correct_no)/(self.number_of_yes+self.number_of_no)

    def get_no_precision(self):
        if self.number_classified_no == 0: return 0
        return 100*self.number_of_correct_no/(self.number_classified_no)

    def get_yes_precision(self):
        if self.number_classified_yes == 0: return 0
        return 100*self.number_of_correct_yes/(self.number_classified_yes)

    def print_statistics(self):
        print('Number of No examples in test: {0}'.format(self.number_of_no))
        print('Number of Yes examples in test: {0}'.format(self.number_of_yes))
        print('----------------')
        print('Number of examples classified as No: {0}'.format(self.number_classified_no))
        print('Number of examples correctly classified as No: {0}'.format(self.number_of_correct_no))
        print('----------------')
        print('Number of examples classified as Yes: {0}'.format(self.number_classified_yes))
        print('Number of examples correctly classified as Yes: {0}'.format(self.number_of_correct_yes))
        print('----------------')
        print('Total Precision: {0:.4f} percent'.format(self.get_precision()))
        print('Yes Precision: {0:.4f} percent'.format(self.get_yes_precision()))
        print('No Precision: {0:.4} percent'.format(self.get_no_precision()))

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

    def run(self):
        for i, el in enumerate(self.train[0]):
            for row in self.train:
                row[i] = float(row[i].strip())
        for i, el in enumerate(self.test[0]):
            for row in self.test:
                row[i] = float(row[i].strip())
        b, predictions, yguess = self.logistic_regression()
        ytest  = [row[-1] for row in self.test]
        stats = Statistics(ytest, yguess)
        print('Dataset: {0}'.format(self.dataset))
        print('Optimal b vector: {0}'.format(b))
        print('----------------')
        stats.print_statistics()


lr = LogisticRegression('occupancy','datasets/occupancy_training.csv','datasets/occupancy_test.csv')
lr.run()