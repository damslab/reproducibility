#ifndef RAPIDJSONCPP_FRAMEREADERAMINERAUTHOR_H
#define RAPIDJSONCPP_FRAMEREADERAMINERAUTHOR_H

#include "FrameReader.h"

class FrameReaderAMinerAuthor : public FrameReader {

private:

    int maxAffiliationsSize = 54;
    int maxResearchInterestsSize = 19;

    const char *authorItems[7] = {"index", "name", "paperCount","citationNumber","hIndex","pIndex", "upIndex"};
    const char *Q1[1] = {"index"};
    const char *Q2[2] = {"name", "paperCount"};
    const char *Q3[5] = {"index", "name", "paperCount","citationNumber","hIndex"};
    const char *Q4[2] = {"name"}; // and extra array values
public:
    FrameReaderAMinerAuthor();

    explicit FrameReaderAMinerAuthor(const vector<ValueType> &schema);

    virtual ~FrameReaderAMinerAuthor();

    void getJSONValues(Document &d, Value *values) override;

    void getJSONValues(vector<long> *col, vector<ItemObject*> *colValue, Document &d) override;

    void runQueries(vector<long> *col, vector<ItemObject*> *colValue, Document &d, string queryName) override;


};


#endif //RAPIDJSONCPP_FRAMEREADERAMINERAUTHOR_H
