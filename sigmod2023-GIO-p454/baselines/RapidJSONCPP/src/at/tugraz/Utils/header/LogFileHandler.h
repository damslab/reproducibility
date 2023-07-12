#ifndef RAPIDJSONCPP_LOGFILEHANDLER_H
#define RAPIDJSONCPP_LOGFILEHANDLER_H

#include <iostream>
#include <fstream>

using namespace std;

class LogFileHandler {
    string fileName;

    ofstream logFile;
public:
    LogFileHandler();

    virtual ~LogFileHandler();

    LogFileHandler(string fileName);

    void addLog(string log);

    void flushLogFile();

};


#endif //RAPIDJSONCPP_LOGFILEHANDLER_H
