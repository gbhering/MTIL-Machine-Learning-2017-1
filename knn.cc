#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>

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
void normalize(vector<double>& attribute, int type) {
    double max = *max_element(attribute.begin(), attribute.end());
    double min = *min_element(attribute.begin(), attribute.end());

    if (type == 0) {
        for (auto it = attribute.begin(); it < attribute.end(); it++) {
            *it = ((*it) - min) / (max - min);
        }
    }
    else if (type == 1) {
        for (auto it = attribute.begin(); it < attribute.end(); it++) {
            *it = (*it) / max;
        }
    }
}

int main() {
    string line;
    ifstream dataset;
    vector<vector<float>> database;

    //READING INPUT FILE
    dataset.open("datasets/occupancy.csv");
    while (getline(dataset, line)) {
        double value;
        vector<float> dLine;

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
        normalize(temp, 0);
        for (unsigned int j = 0; j < database.size(); j++) {
            database[j][i] = temp[j];
        }
    }

    return 0;
}