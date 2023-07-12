//
// Created by saeed on 2/18/22.
//

#ifndef RAPIDJSONCPP_FRAMEREADERQUERYENGINE_H
#define RAPIDJSONCPP_FRAMEREADERQUERYENGINE_H

#include "FrameReader.h"

class FrameReaderQueryEngine : public FrameReader {


public:

    FrameReaderQueryEngine();

    virtual ~FrameReaderQueryEngine();

    explicit FrameReaderQueryEngine(const vector<ValueType> &schema);

    void
    executeQueries(vector<long> *col, vector<ItemObject *> *colValue, Document &d, vector<string> keys, int colIndex);
};


#endif //RAPIDJSONCPP_FRAMEREADERQUERYENGINE_H
