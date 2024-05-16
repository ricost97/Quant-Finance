#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <Eigen/Dense>

using namespace std;
using namespace Eigen;

vector<vector<double>> parseCSV(const string& filename) {
    vector<vector<double>> data;
    ifstream file(filename);
    string line;

    while (getline(file, line)) {
        vector<double> row;
        stringstream lineStream(line);
        string cell;

        while (getline(lineStream, cell, ',')) {
            row.push_back(stod(cell));
        }
        data.push_back(row);
    }
    file.close();
    return data;
}

void linearRegression(const vector<vector<double>>& data, const string& outputFilename) {
    int n = data.size();
    VectorXd y(n);
    MatrixXd X(n, 2);

    for (int i = 0; i < n; ++i) {
        X(i, 0) = 1;               // Intercept term
        X(i, 1) = data[i][0];      // Independent variable (e.g., time or date)
        y(i) = data[i][1];         // Dependent variable (e.g., stock price)
    }

    VectorXd beta = (X.transpose() * X).inverse() * X.transpose() * y;
    cout << "Regression coefficients: " << beta.transpose() << endl;

    // Save coefficients to file
    ofstream outFile(outputFilename);
    outFile << beta[0] << "," << beta[1];
    outFile.close();
}

int main() {
    string filename = "AAPL_history.csv";
    string outputFilename = "regression_coefficients.csv";
    auto data = parseCSV(filename);
    linearRegression(data, outputFilename);
    return 0;
}
