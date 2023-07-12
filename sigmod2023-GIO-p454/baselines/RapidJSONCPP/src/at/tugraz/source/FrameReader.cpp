#include "FrameReader.h"

FrameReader::FrameReader() {}

FrameReader::~FrameReader() {}

FrameReader::FrameReader(const vector<ValueType> &schema) : schema(schema), ncols(schema.size()) {}

void FrameReader::getJSONValues(Document &d, Value *values) {}

void FrameReader::runQueries(vector<long> *col, vector<ItemObject *> *colValue, Document &d, string queryName) {}

void FrameReader::getJSONValues(vector<long> *col, vector<ItemObject*> *colValue, Document &d) {}

void FrameReader::addEntityItems(Value &d, Value *values, const char **items, int itemSize, int &index) {
    for (int i = 0; i < itemSize; ++i) {
        if (d.HasMember(items[i])) {
            values[index] = d[items[i]];
        } else
            values[index] = NULL;
        index++;
    }
}

void FrameReader::addEntityItems(Value &d, vector<long> *col, vector<ItemObject*> *colValue, const char **items, int itemSize, int &index) {
    for (int i = 0; i < itemSize; ++i) {
        if (index < ncols && d.HasMember(items[i])) {
            colValue->push_back(getActualValue(d[items[i]], schema[index]));
            col->push_back(index);
        }
        index++;
    }
}

void FrameReader::addEntityItem(Value &d, vector<long> *col, vector<ItemObject*> *colValue, int &index) {
     if (index < ncols) {
            colValue->push_back(getActualValue(d, schema[index]));
            col->push_back(index);
        }
     index++;
}

ItemObject* FrameReader::getActualValue(Value &value, ValueType vt) {
    ItemObject* io;
    switch (vt) {
        case INT32: {
            io = new ItemValue<int>(value.GetInt());
        //    int v = value.GetInt();
        //    cout<<v;
            break;
        }
        case INT64: {
            io = new ItemValue<long>(value.GetInt64());
       //     long v = value.GetInt64();
        //    cout<<v<<endl;
            break;
        }
        case FP32: {
            io = new ItemValue<float>(value.GetFloat());
        //    float v = value.GetFloat();
        //    cout<<v;
            break;
        }
        case FP64: {
            io = new ItemValue<double>(value.GetDouble());
         //   double v = value.GetDouble();
          //  cout<<v;
            break;
        }
        case STRING: {
            if (value.IsString()) {
                io = new ItemValue<string>(value.GetString());
            } else
                io = nullptr;
          //  string v = value.GetString();
          //  cout<<v;
            break;
        }
        case BOOLEAN: {
            io = new ItemValue<bool>(value.GetBool());
           // bool v = value.GetBool();
            break;
        }
        default : {
            io = nullptr;
            break;
        }
    }
    return io;
}


