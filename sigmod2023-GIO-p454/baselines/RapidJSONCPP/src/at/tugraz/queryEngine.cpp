
#include "FrameReaderQueryEngine.h"
#include <vector>
#include <map>
#include <ItemObject.h>
using namespace rapidjson;
using namespace std;

int main(int argc, char *argv[]) {

    string datasetFileName = argv[1];
    string schemaFileName = argv[2];
    string schemaMapFileName = argv[3];

    FileHandler schemaFileHandler(schemaFileName);

    string schemaString(schemaFileHandler.getLines()[0]);
    string delimiter = ",";
    size_t pos;
    string token;
    vector<ValueType> schema;
    do{
        pos = schemaString.find(delimiter);
        if(pos == string::npos)
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

    // load schema Map
    FileHandler schemaMapFileHandler(schemaMapFileName);

    vector<vector<string>> selectItems;
    vector<int> selectItemsIndex;
    for (char *line: schemaMapFileHandler.getLines()) {
        string selectItem(line);
        pos = selectItem.find(delimiter);
        if(pos == string::npos)
            token = selectItem.substr(0, selectItem.length());
        else
            token = selectItem.substr(0, pos);

        string  colIndexStr = selectItem.substr(pos+1,selectItem.length());
        int colIndex = stoi(colIndexStr);

        // split token by "/"
        string colToken = token.substr(1, token.length());
        vector<string> keysVector;
        do{
            pos = colToken.find("/");
            if(pos == string::npos)
                token = colToken.substr(0, colToken.length());
            else
                token = colToken.substr(0, pos);
            keysVector.push_back(token);
            colToken.erase(0, pos+1);
        } while (pos != string::npos);

        selectItems.push_back(keysVector);
        selectItemsIndex.push_back(colIndex);
    }

    FrameReaderQueryEngine *frameReader = new FrameReaderQueryEngine(schema);
    vector<long> *fI = new vector<long>();
    vector<long> *fJ = new vector<long>();
    vector<ItemObject*> *fV = new vector<ItemObject*>();



    ifstream inStreamRegularFile;
    inStreamRegularFile.open(datasetFileName.c_str(), ofstream::binary | ios::in);
    string line;

    long rowIndex = 0;
    while (getline(inStreamRegularFile, line)) {
        Document d;
        d.Parse(line.c_str());

        size_t jl = fJ->size();
        for (int i = 0; i < selectItems.size() ; ++i) {
            frameReader->executeQueries(fJ, fV, d,selectItems[i], selectItemsIndex[i]);
        }
        jl = fJ->size() - jl;
        for (size_t i = 0; i < jl ; ++i) {
            fI->push_back(rowIndex);
        }
        rowIndex++;
        d.GetAllocator().Clear();
    }
    inStreamRegularFile.close();
    inStreamRegularFile.clear();
    return 0;
}

