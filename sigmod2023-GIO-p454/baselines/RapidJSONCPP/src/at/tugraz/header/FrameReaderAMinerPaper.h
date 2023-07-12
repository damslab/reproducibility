#ifndef RAPIDJSONCPP_FRAMEREADERAMINERPAPER_H
#define RAPIDJSONCPP_FRAMEREADERAMINERPAPER_H

#include "FrameReader.h"

class FrameReaderAMinerPaper: public FrameReader{
private:

    int maxAffiliationsSize = 54;
    int maxResearchInterestsSize = 19;
    const char *paperItems[5] = {"index", "title", "year", "publicationVenue", "paperAbstract"};
    const char *Q1[1] = {"index"};
    const char *Q2[2] = {"title", "year"};
    const char *Q3[5] = {"index", "title", "year","publicationVenue","paperAbstract"};
    const char *Q4[2] = {"index"}; // and extra array values: reference_1, reference_2, reference_3, reference_4
    //const char *Q5[2] = {"index"};//author.index_1, author.index_2, author.index_3, author.index_4
    const char *F1[1] = {"index"};
    const char *F2[2] = {"index", "title"};
    const char *F3[3] = {"index", "title", "year"};
    const char *F4[4] = {"index","title", "year", "publicationVenue"};
    const char *F5[5] = {"index","title", "year", "publicationVenue", "paperAbstract"};
public:
    FrameReaderAMinerPaper();

    explicit FrameReaderAMinerPaper(const vector<ValueType> &schema);

    virtual ~FrameReaderAMinerPaper();

    void getJSONValues(Document &d, Value *values) override;

    void getJSONValues(vector<long> *col, vector<ItemObject*> *colValue, Document &d) override;

    void runQueries(vector<long> *col, vector<ItemObject*> *colValue, Document &d, string queryName) override;

};


#endif //RAPIDJSONCPP_FRAMEREADERAMINERPAPER_H
