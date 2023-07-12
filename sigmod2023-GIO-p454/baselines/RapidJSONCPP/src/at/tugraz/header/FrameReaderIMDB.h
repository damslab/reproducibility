#ifndef RAPIDJSONCPP_FRAMEREADERIMDB_H
#define RAPIDJSONCPP_FRAMEREADERIMDB_H


#include "FrameReader.h"

class FrameReaderIMDB : public FrameReader {

private:
    int maxGenresSize = 11;
    int maxRolesSize = 1274;
    int maxDirectorsGenresSize = 20;
    const char *movieItems[4] = {"id", "name", "year", "rank"};
    const char *genreItems[2] = {"moviesId", "genre"};
    const char *roleItems[2] = {"movieId", "role"};
    const char *actorItems[4] = {"id", "firstName", "lastName", "gender"};
    const char *movieDirectorItems[1] = {"movieId"};
    const char *directorsGenresItems[3] = {"directorId", "genre", "prob"};
    const char *directorItems[3] = {"id", "firstName", "lastName"};

public:
    FrameReaderIMDB();

    explicit FrameReaderIMDB(const vector<ValueType> &schema);

    virtual ~FrameReaderIMDB();

    void getJSONValues(Document &d, Value *values) override;

    void getJSONValues(vector<long> *col, vector<ItemObject*> *colValue, Document &d) override;

};


#endif //RAPIDJSONCPP_FRAMEREADERIMDB_H
