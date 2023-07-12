
#include "FrameReaderTwitter.h"
#include <vector>
#include <ItemObject.h>

using namespace rapidjson;
using namespace std;

int main(int argc, char *argv[]) {

    string datasetFileName = argv[1];
    string schemaFileName = argv[2];
    string query = argv[3];

    FileHandler schemaFileHandler(schemaFileName);
    //LogFileHandler logFileHandler(LOG_HOME);

    string schemaString(schemaFileHandler.getLines()[0]);
    string delimiter = ",";
    size_t pos;
    string token;
    vector<ValueType> schema;
    do {
        pos = schemaString.find(delimiter);
        if (pos == string::npos)
            token = schemaString.substr(0, schemaString.length());
        else
            token = schemaString.substr(0, pos);
        ValueType vt;
        if (token == "INT32")
            vt = INT32;
        else if (token == "INT64")
            vt = INT64;
        else if (token == "FP32")
            vt = FP32;
        else if (token == "FP64")
            vt = FP64;
        else if (token == "STRING")
            vt = STRING;
        else if (token == "BOOLEAN")
            vt = BOOLEAN;
        schema.push_back(vt);
        schemaString.erase(0, pos + delimiter.length());
    } while (pos != string::npos);

    auto tmpTime = chrono::steady_clock::now();
    FrameReader *frameReader = new FrameReaderTwitter(schema);

    //FileHandler dataFileHandler(datasetFileName);

    vector<long> *fI = new vector<long>();
    vector<long> *fJ = new vector<long>();
    vector<ItemObject *> *fV = new vector<ItemObject *>();


    ifstream inStreamRegularFile;
    inStreamRegularFile.open(datasetFileName.c_str(), ofstream::binary | ios::in);
    string line;

    long rowIndex = 0;
    while (getline(inStreamRegularFile, line)) {
        Document d;
        d.Parse(line.c_str());
        size_t jl = fJ->size();
        frameReader->runQueries(fJ, fV, d, query);
        jl = fJ->size() - jl;
        for (size_t i = 0; i < jl; ++i) {
            fI->push_back(rowIndex);
        }
        rowIndex++;
        d.GetAllocator().Clear();
    }
    inStreamRegularFile.close();
    inStreamRegularFile.clear();
    return 0;
}

