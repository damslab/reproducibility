#include "FrameReaderTwitter.h"

FrameReaderTwitter::FrameReaderTwitter() {}

FrameReaderTwitter::FrameReaderTwitter(const vector<ValueType> &schema) : FrameReader(schema) {}

FrameReaderTwitter::~FrameReaderTwitter() {}

void FrameReaderTwitter::getJSONValues(Document &d, Value *values) {

}

void
FrameReaderTwitter::runQueries(vector<long> *col, vector<ItemObject *> *colValue, Document &d, string queryName) {
    int index = 0;
    if (queryName == "Q1")
        addEntityItems(d, col, colValue, Q1, 1, index);
    else if (queryName == "Q2")
        addEntityItems(d, col, colValue, Q2, 2, index);
    else if (queryName == "Q3") {
        addEntityItems(d, col, colValue, Q3, 4, index);
    }

    else if (queryName == "Q4") {
        if (d.HasMember("user") && !d["user"].IsNull() && !d["user"]["id"].IsNull()) {
            addEntityItem(d["user"]["id"], col, colValue, index);
        }
        addEntityItems(d, col, colValue, Q4, 1, index);

    } else if (queryName == "Q5") {
        if (d.HasMember("retweeted_status") && !d["retweeted_status"].IsNull() && !d["retweeted_status"]["user"]["id"].IsNull()) {
             addEntityItem(d["retweeted_status"]["user"]["id"], col, colValue, index);
        }
    }
}

void FrameReaderTwitter::runQueries2(vector<long> *col, vector<ItemObject *> *colValue, Document &d,vector<string> keys, int colIndex) {

    const char * k0=keys[0].c_str();
    int keysSize = keys.size();
    if (keysSize == 1) {
        if (d.HasMember(k0) && !d[k0].IsNull()) {
            colValue->push_back(getActualValue(d[k0], schema[colIndex]));
            col->push_back(colIndex);
        }
    }  else if (keysSize ==2){
        if (d.HasMember(k0) && !d[k0].IsNull()) {
            const char * k1=keys[1].c_str();
            if (d[k0].HasMember(k1) && !d[k0][k1].IsNull()) {
                colValue->push_back(getActualValue(d[k0][k1], schema[colIndex]));
                col->push_back(colIndex);
            }
        }
    }
    else if (keysSize ==3){
        if (d.HasMember(k0) && !d[k0].IsNull()) {
            const char * k1=keys[1].c_str();
            if (d[k0].HasMember(k1) && !d[k0][k1].IsNull()) {
                const char * k2=keys[2].c_str();
                if (d[k0][k1].HasMember(k2) && !d[k0][k1][k2].IsNull()) {
                    colValue->push_back(getActualValue(d[k0][k1][k2], schema[colIndex]));
                    col->push_back(colIndex);
                }
            }
        }
    }

    else if (keysSize ==4){
        if (d.HasMember(k0) && !d[k0].IsNull()) {
            const char * k1=keys[1].c_str();
            if (d[k0].HasMember(k1) && !d[k0][k1].IsNull()) {
                const char * k2=keys[2].c_str();
                if (d[k0][k1].HasMember(k2) && !d[k0][k1][k2].IsNull()) {
                    const char * k3=keys[3].c_str();
                    if (d[k0][k1][k2].HasMember(k3) && !d[k0][k1][k2][k3].IsNull()) {
                        colValue->push_back(getActualValue(d[k0][k1][k2][k3], schema[colIndex]));
                        col->push_back(colIndex);
                    }
                }
            }
        }
    }

    else if (keysSize ==5){
        if (d.HasMember(k0) && !d[k0].IsNull()) {
            const char * k1=keys[1].c_str();
            if (d[k0].HasMember(k1) && !d[k0][k1].IsNull()) {
                const char * k2=keys[2].c_str();
                if (d[k0][k1].HasMember(k2) && !d[k0][k1][k2].IsNull()) {
                    const char * k3=keys[3].c_str();
                    if (d[k0][k1][k2].HasMember(k3) && !d[k0][k1][k2][k3].IsNull()) {
                        const char * k4=keys[4].c_str();
                        if (d[k0][k1][k2][k3].HasMember(k4) && !d[k0][k1][k2][k3][k4].IsNull()) {
                            colValue->push_back(getActualValue(d[k0][k1][k2][k3][k4], schema[colIndex]));
                            col->push_back(colIndex);
                        }

                    }
                }
            }
        }
    }

}

void FrameReaderTwitter::getJSONValues(vector<long> *col, vector<ItemObject *> *colValue, Document &d) {

}

#include "FrameReaderTwitter.h"
