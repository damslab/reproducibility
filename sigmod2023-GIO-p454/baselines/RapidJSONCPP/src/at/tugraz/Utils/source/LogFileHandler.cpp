#include "LogFileHandler.h"

LogFileHandler::LogFileHandler() {}

LogFileHandler::~LogFileHandler() {

}

LogFileHandler::LogFileHandler(string fileName) {
    logFile.open(fileName, ios::out | ios::app);
}

void LogFileHandler::addLog(string log) {
    logFile << log << "\n";
}

void LogFileHandler::flushLogFile() {
    logFile.close();
}