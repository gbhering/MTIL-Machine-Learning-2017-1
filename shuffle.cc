#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <random>
#include <chrono>

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

int main() {
    string line;
    ifstream dataset;
    ofstream training, test;
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

    unsigned seed = chrono::system_clock::now().time_since_epoch().count();
    shuffle (database.begin(), database.end(), default_random_engine(seed));

    //random_shuffle(database.begin(), database.end());

    double proportion = 1.0 / 3.0;
    int testSize = database.size() * proportion;
    int trainingSize = database.size() - testSize;

    training.open("datasets/training.csv");
    for (int i = 0; i < trainingSize; i++) {
        for (unsigned int j = 0; j < database[i].size(); j++) {
            training << database[i][j];
            if (j != database[i].size() - 1) {
                training << ",";
            }
        }
        training << endl;
    }
    training.close();

    test.open("datasets/test.csv");
    for (unsigned int i = trainingSize; i < database.size(); i++) {
        for (unsigned int j = 0; j < database[i].size(); j++) {
            test << database[i][j];
            if (j != database[i].size() - 1) {
                test << ",";
            }
        }
        test << endl;
    }
    test.close();

    return 0;
}