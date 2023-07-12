#include "FileHandler.h"

FileHandler::FileHandler() {}

FileHandler::FileHandler(const string &fileName) : fileName(fileName) {

    //Opening Dataset File and Keeping it Open
    this->inStreamRegularFile.open(fileName.c_str(), ofstream::binary | ios::in);
    string line;

    while (getline(inStreamRegularFile, line)) {
        char *cstr = new char[line.length() + 1];
        strcpy(cstr, line.c_str());
        lines.push_back(cstr);

    }
    inStreamRegularFile.close();
    inStreamRegularFile.clear();
}

const vector<char *> &FileHandler::getLines() const {
    return lines;
}
