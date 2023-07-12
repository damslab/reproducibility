#include "FrameReaderIMDB.h"

FrameReaderIMDB::FrameReaderIMDB() {}

FrameReaderIMDB::FrameReaderIMDB(const vector<ValueType> &schema) : FrameReader(schema) {}

FrameReaderIMDB::~FrameReaderIMDB() {}

void FrameReaderIMDB::getJSONValues(Document &d, Value *values) {
    int index = 0;
    addEntityItems(d, values, movieItems, 4, index);
    const char *namech = "genres";
    int listSize = 0;
    if (d.HasMember(namech) && !d[namech].IsNull()) {
        listSize = d[namech].Size();
        for (SizeType i = 0; i < listSize; i++)
            addEntityItems(d[namech][i], values, genreItems, 2, index);
    }

    int remindSize = (maxGenresSize - listSize) * 2;
    for (int i = index; i < index + remindSize; i++)
        values[i] = NULL;
    index += remindSize;

    namech = "roles";
    listSize = 0;
    if (d.HasMember(namech) && !d[namech].IsNull()) {
        listSize = d[namech].Size();
        for (SizeType i = 0; i < listSize; i++) {
            addEntityItems(d[namech][i], values, roleItems, 2, index);
            if (d[namech][i].HasMember("actor") && !d[namech][i]["actor"].IsNull()) {
                addEntityItems(d[namech][i]["actor"], values, actorItems, 4, index);
            }
        }
    }
    remindSize = (maxRolesSize - listSize) * 6;
    for (int i = index; i < index + remindSize; i++)
        values[i] = NULL;
    index += remindSize;
    namech = "directors";

    if (d.HasMember(namech) && !d[namech].IsNull()) {
        for (SizeType i = 0; i < d[namech].Size(); i++) {
            addEntityItems(d[namech][i], values, movieDirectorItems, 1, index);
            addEntityItems(d[namech][i]["directors"], values, directorItems, 3, index);
            listSize = 0;
            if (d[namech][i]["directors"].HasMember("directorsGenres") &&
                !d[namech][i]["directors"]["directorsGenres"].IsNull()) {
                listSize = d[namech][i]["directors"]["directorsGenres"].Size();
                for (SizeType j = 0; j < listSize; j++) {
                    addEntityItems(d[namech][i]["directors"]["directorsGenres"][j], values, directorsGenresItems, 3,
                                   index);
                }
            }
            remindSize = (maxDirectorsGenresSize - listSize) * 3;
            for (int k = index; k < index + remindSize; k++) {
                values[k] = NULL;
            }
            index += remindSize;
        }
    }
}

void FrameReaderIMDB::getJSONValues(vector<long> *col, vector<ItemObject*> *colValue, Document &d) {
    int index = 0;
    addEntityItems(d, col, colValue, movieItems, 4, index);
    const char *namech = "genres";
    int listSize = 0;
    if (d.HasMember(namech) && !d[namech].IsNull()) {
        listSize = d[namech].Size();
        for (SizeType i = 0; i < listSize; i++)
            addEntityItems(d[namech][i], col, colValue, genreItems, 2, index);
    }

    int remindSize = (maxGenresSize - listSize) * 2;
    index += remindSize;
    if (index>=ncols)
        return;

    namech = "roles";
    listSize = 0;
    if (d.HasMember(namech) && !d[namech].IsNull()) {
        listSize = d[namech].Size();
        for (SizeType i = 0; i < listSize; i++) {
            addEntityItems(d[namech][i], col, colValue, roleItems, 2, index);
            if (d[namech][i].HasMember("actor") && !d[namech][i]["actor"].IsNull())
                addEntityItems(d[namech][i]["actor"], col, colValue, actorItems, 4, index);
        }
    }
    remindSize = (maxRolesSize - listSize) * 6;
    index += remindSize;
    if (index>=ncols)
        return;

    namech = "directors";
    if (d.HasMember(namech) && !d[namech].IsNull()) {
        for (SizeType i = 0; i < d[namech].Size(); i++) {
            addEntityItems(d[namech][i], col, colValue, movieDirectorItems, 1, index);
            addEntityItems(d[namech][i]["directors"], col, colValue, directorItems, 3, index);
            listSize = 0;
            if (d[namech][i]["directors"].HasMember("directorsGenres") &&
                !d[namech][i]["directors"]["directorsGenres"].IsNull()) {
                listSize = d[namech][i]["directors"]["directorsGenres"].Size();
                for (SizeType j = 0; j < listSize; j++)
                    addEntityItems(d[namech][i]["directors"]["directorsGenres"][j], col, colValue, directorsGenresItems, 3,index);

            }
            remindSize = (maxDirectorsGenresSize - listSize) * 3;
            index += remindSize;
            if (index>=ncols)
                return;
        }
    }
}
