#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cmath>

using namespace std;

double getNumberFromString(string& s) {
    unsigned int i = 1;
    double number;

    while (i < s.size() && s[i] != ',') {
        i++;
    }

    number = stod(s.substr(0,i));
    s.erase(s.begin(), s.begin() + i);
    if (s[0] == ',') {
        s.erase(s.begin());
    }

    return number;
}

// type = 0 for linear
// type = 1 for max value
void normalize(vector<double>& attribute, vector<pair<double,double>>& minMax) {
    double max = *max_element(attribute.begin(), attribute.end());
    double min = *min_element(attribute.begin(), attribute.end());

    minMax.push_back(pair<double,double>(min,max));

    for (auto it = attribute.begin(); it < attribute.end(); it++) {
        *it = ((*it) - min) / (max - min);
    }
}

void normalizeTestCase(vector<double>& attribute, vector<pair<double,double>> minMax) {
    for (unsigned int i = 0; i < attribute.size(); i++) {
        double max = minMax[i].second;
        double min = minMax[i].first;

        attribute[i] = (attribute[i] - min) / (max - min);
    }
}

int main() {
    string line;
    ifstream dataset, testcases;
    vector<vector<double>> database;
    vector<pair<double,double>> minMax;

    //READING INPUT FILE
    dataset.open("datasets/occupancy_training.csv");
    while (getline(dataset, line)) {
        double value;
        vector<double> dLine;

        while (line.size() != 0) {
            value = getNumberFromString(line);
            dLine.push_back(value);
        }

        database.push_back(dLine);
    }
    dataset.close();

    //NORMALIZING THE DATABASE
    for (unsigned int i = 0; i < database[0].size(); i++) {
        vector<double> temp;
        for (unsigned int j = 0; j < database.size(); j++) {
            temp.push_back(database[j][i]);
        }
        normalize(temp, minMax);
        for (unsigned int j = 0; j < database.size(); j++) {
            database[j][i] = temp[j];
        }
    }

    testcases.open("datasets/occupancy_test.csv");
    while (getline(testcases, line)) {
        double value;
        vector<double> dLine;

        while (line.size() != 0) {
            value = getNumberFromString(line);
            dLine.push_back(value);
        }

        normalizeTestCase(dLine, minMax);

        vector<double> distances(database.size(), 0);
        for (unsigned int i = 0; i < database.size(); i++) {
            for (unsigned int j = 0; j < database[i].size() - 1; j++) {
                distances[i] += pow(dLine[j] - database[i][j], 2);
            }
            distances[i] = sqrt(distances[i]);
        }

        int K = 5;
        vector<int> count(2, 0);
        for (int i = 0; i < K; i++) {
            int neighbor = -1;
            double lowest = 100000.0;

            for (unsigned int j = 0; j < distances.size(); j++) {
                if (distances[j] < lowest) {
                    lowest = distances[j];
                    neighbor = j;
                }
            }

            count[database[neighbor][database[neighbor].size()-1]]++;
            distances[neighbor] = 1000000;
        }

        if (count[0] > count[1]) {
            cout << "Predicted: " << 0 << " | Real: " << dLine[dLine.size()-1] << endl;
        }
        else {
            cout << "Predicted: " << 1 << " | Real: " << dLine[dLine.size()-1] << endl;
        }
    }
    testcases.close();

    return 0;
}