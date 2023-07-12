#ifndef RAPIDJSONCPP_FRAMEREADER_H
#define RAPIDJSONCPP_FRAMEREADER_H

#include <DataReader.h>
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
#include <iostream>
#include "FileHandler.h"
#include "Types.h"
#include <stdio.h>
#include <string.h>
#include "LogFileHandler.h"
#include <chrono>
#include <ItemObject.h>
#include <ItemValue.h>

using namespace std;
class FrameReader {

protected:

    vector<ValueType> schema;

    int ncols;

    void addEntityItems(Value &d, Value *values, const char **items, int itemSize, int &index);

    void addEntityItems(Value &d, vector<long> *col, vector<ItemObject *> *colValue, const char **items, int itemSize, int &index);

    void addEntityItem(Value &d, vector<long> *col, vector<ItemObject *> *colValue, int &index);



public:

    FrameReader();

    explicit FrameReader(const vector<ValueType> &schema);

    virtual ~FrameReader();

    virtual void getJSONValues(Document &d, Value *values);

    virtual void runQueries(vector<long> *col, vector<ItemObject *> *colValue, Document &d, string queryName);

    ItemObject* getActualValue(Value &value, ValueType vt);

    virtual void getJSONValues(vector<long> *col, vector<ItemObject*> *colValue,Document &d);
};

#endif //RAPIDJSONCPP_FRAMEREADER_H
