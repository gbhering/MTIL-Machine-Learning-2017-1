#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <sstream>
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

int main(int argc, char **argv) {
    string line;
    ifstream dataset, testcases;
    vector<vector<double>> database;
    vector<pair<double,double>> minMax;

    // Expects dataset name as argument
    // Optional k as argument
    if(argc <= 1){
        cout << "Error: missing dataset name. Correct usage: "
             << endl << argv[0] << " dataset_name [k]"
             << endl << "Terminating..." << endl;
        return 0;
    }
    
    // Default value for K
    int K = 3;

    // K specified
    if(argc == 3){
        stringstream ss;
        ss << argv[2];
        ss >> K;
    }

    string dataset_name = argv[1];

    //READING INPUT FILE
    dataset.open("datasets/" + dataset_name + "_training.csv");
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

    vector<int> correctYes(2, 0);
    vector<int> correctNo(2, 0);

    testcases.open("datasets/" + dataset_name + "_test.csv");
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
                //cout << dLine[j] << " " << database[i][j] << endl;
            }
            distances[i] = sqrt(distances[i]);
            //cout << "Distance to example " << i+1 << " is " << distances[i] << "." << endl;
        }

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
            if (dLine[dLine.size()-1] == 0) {
                correctNo[1]++;
            }
            else {
                correctNo[0]++;
            }
        }
        else {
            if (dLine[dLine.size()-1] == 1) {
                correctYes[1]++;
            }
            else {
                correctYes[0]++;
            }
        }
    }
    testcases.close();

    cout << "Dataset: " << dataset_name << endl;
    cout << "K: " << K << endl;
    cout << "----------------" << endl;
    cout << "Number of No examples in test: " << correctNo[1] + correctYes[0] << "." << endl;
    cout << "Number of Yes examples in test: " << correctNo[0] + correctYes[1] << "." << endl;
    cout << "----------------" << endl;
    cout << "Number of examples classified as No: " << correctNo[0] + correctNo[1] << "." << endl;
    cout << "Number of examples correctly classified as No: " << correctNo[1] << "." << endl;
    cout << "----------------" << endl;
    cout << "Number of examples classified as Yes: " << correctYes[0] + correctYes[1] << "." << endl;
    cout << "Number of examples correctly classified as Yes: " << correctYes[1] << "." << endl;
    cout << "----------------" << endl;
    cout << "Total Precision: " << 100.0 * (correctNo[1] + correctYes[1]) / (correctNo[1] + correctYes[0] + correctNo[0] + correctYes[1]) << " percent" << endl;
    cout << "Yes Precision: " << 100.0 * (correctYes[1]) / (correctYes[0] + correctYes[1]) << " percent" << endl;
    cout << "No Precision: " << 100.0 * (correctNo[1]) / (correctNo[1] + correctNo[0]) << " percent" << endl;

    return 0;
}