#include "FrameReaderAMinerPaper.h"

FrameReaderAMinerPaper::FrameReaderAMinerPaper() {}

FrameReaderAMinerPaper::FrameReaderAMinerPaper(const vector<ValueType> &schema) : FrameReader(schema) {}

FrameReaderAMinerPaper::~FrameReaderAMinerPaper() {}

void FrameReaderAMinerPaper::getJSONValues(Document &d, Value *values) {

}

void
FrameReaderAMinerPaper::runQueries(vector<long> *col, vector<ItemObject *> *colValue, Document &d, string queryName) {
    int index = 0;
    if (queryName == "Q1")
        addEntityItems(d, col, colValue, Q1, 1, index);
    else if (queryName == "Q2")
        addEntityItems(d, col, colValue, Q2, 2, index);
    else if (queryName == "Q3")
        addEntityItems(d, col, colValue, Q3, 5, index);
    else if (queryName == "Q4") {
        addEntityItems(d, col, colValue, Q4, 1, index);

        if (d.HasMember("references") && !d["references"].IsNull()) {
            int listSize = d["references"].Size();
            listSize = listSize > 4 ? 4 : listSize;
            for (SizeType j = 0; j < listSize; j++)
                addEntityItem(d["references"][j], col, colValue, index);
        }
    } else if (queryName == "Q5") {
        if (d.HasMember("authors") && !d["authors"].IsNull()) {
            int listSize1 = d["authors"].Size();
            listSize1 = listSize1 > 4 ? 4 : listSize1;

            for (SizeType i = 0; i < listSize1; i++) {
                if (d["authors"][i].HasMember("index") && !d["authors"][i]["index"].IsNull()) {
                    addEntityItem(d["authors"][i]["index"], col, colValue, index);
                }
            }
        }
    }else if (queryName == "F1"){
        addEntityItems(d, col, colValue, F1, 1, index);
    }else if (queryName == "F2"){
        addEntityItems(d, col, colValue, F2, 2, index);
    }else if (queryName == "F3"){
        addEntityItems(d, col, colValue, F3, 3, index);
    }else if (queryName == "F4"){
        addEntityItems(d, col, colValue, F4, 4, index);
    }else if (queryName == "F5"){
        addEntityItems(d, col, colValue, F5, 5, index);
    }
    else if (queryName == "F6" || queryName == "F7" || queryName == "F8"|| queryName == "F9"|| queryName == "F10"){
        addEntityItems(d, col, colValue, F5, 5, index);
        int tl;
        if (queryName == "F6")
            tl = 1;
        else if (queryName == "F7")
            tl = 2;
        else if (queryName == "F8")
            tl = 3;
        else if (queryName == "F9")
            tl = 4;
        else if (queryName == "F10")
            tl = 5;

        if (d.HasMember("references") && !d["references"].IsNull()) {
            int listSize = d["references"].Size();
            listSize = listSize > tl ? tl: listSize;
            for (SizeType j = 0; j < listSize; j++)
                addEntityItem(d["references"][j], col, colValue, index);
        }
    }
}

    void FrameReaderAMinerPaper::getJSONValues(vector<long> *col, vector<ItemObject *> *colValue, Document &d) {

    }

#include "FrameReaderAMinerPaper.h"
