#ifndef RAPIDJSONCPP_FILEHANDLER_H
#define RAPIDJSONCPP_FILEHANDLER_H

#include <iostream>
#include <fstream>
#include <vector>
#include <stdio.h>
#include <string.h>

using namespace std;

class FileHandler {

private:

    // Dataset File Name:
    string fileName;

    //Input Stream: For Reading:
    ifstream inStreamRegularFile;

    //Lines of Dataset:
    vector<char *> lines;

public:

    FileHandler();

    FileHandler(const string &fileName);

    const vector<char *> &getLines() const;

};


#endif //RAPIDJSONCPP_FILEHANDLER_H
