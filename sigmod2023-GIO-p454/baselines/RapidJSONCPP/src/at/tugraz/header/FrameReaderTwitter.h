
#ifndef RAPIDJSONCPP_FRAMEREADERTWITTER_H
#define RAPIDJSONCPP_FRAMEREADERTWITTER_H

#include "FrameReader.h"

class FrameReaderTwitter : public FrameReader{
private:

    int maxAffiliationsSize = 54;
    int maxResearchInterestsSize = 19;
    const char *paperItems[5] = {"index", "title", "year", "publicationVenue", "paperAbstract"};
    const char *Q1[1] = {"id"};
    const char *Q2[2] = {"id", "text"};
    const char *Q3[4] = {"id", "text", "created_at","in_reply_to_screen_name"};
    const char *Q4[2] = {"id"}; //user.id
    const char *Q5[2] = {"id"};//retweet.user.id
public:
    FrameReaderTwitter();

    explicit FrameReaderTwitter(const vector<ValueType> &schema);

    virtual ~FrameReaderTwitter();

    void getJSONValues(Document &d, Value *values) override;

    void getJSONValues(vector<long> *col, vector<ItemObject*> *colValue, Document &d) override;

    void runQueries(vector<long> *col, vector<ItemObject*> *colValue, Document &d, string queryName) override;

    void runQueries2(vector<long> *col, vector<ItemObject*> *colValue, Document &d,vector<string> keys, int colIndex);


};


#endif //RAPIDJSONCPP_FRAMEREADERTWITTER_H
