#include "FrameReaderAMinerAuthor.h"

FrameReaderAMinerAuthor::FrameReaderAMinerAuthor() {}

FrameReaderAMinerAuthor::FrameReaderAMinerAuthor(const vector<ValueType> &schema) : FrameReader(schema) {}

FrameReaderAMinerAuthor::~FrameReaderAMinerAuthor() {}

void FrameReaderAMinerAuthor::getJSONValues(Document &d, Value *values) {

}

void FrameReaderAMinerAuthor::runQueries(vector<long> *col, vector<ItemObject *> *colValue, Document &d, string queryName) {

    int index = 0;
    if (queryName == "Q1")
        addEntityItems(d, col, colValue, Q1, 1, index);

    else if (queryName == "Q2")
        addEntityItems(d, col, colValue, Q2, 2, index);
    else if (queryName == "Q3")
        addEntityItems(d, col, colValue, Q3, 5, index);
    else if (queryName == "Q4") {
        addEntityItems(d, col, colValue, Q4, 1, index);

        if (d.HasMember("authorAffiliations") && !d["authorAffiliations"].IsNull()) {
            int listSize = d["authorAffiliations"].Size();
            listSize = listSize > 4 ? 4: listSize;
            for (SizeType j = 0; j < listSize; j++)
                addEntityItem(d["authorAffiliations"][j], col, colValue, index);
        }
    }

}

void FrameReaderAMinerAuthor::getJSONValues(vector<long> *col, vector<ItemObject*> *colValue, Document &d) {

}
#include "FrameReaderAMinerAuthor.h"
