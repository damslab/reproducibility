
#ifndef RAPIDJSONCPP_ITEMVALUE_H
#define RAPIDJSONCPP_ITEMVALUE_H

#include "ItemObject.h"

template<typename T>
class ItemValue : public ItemObject{
public:
    ItemValue(T var) : var(var) {}

    virtual ~ItemValue() {}

    void print() override {
        cout<< var<<endl;
    }

    T var;
};


#endif //RAPIDJSONCPP_ITEMVALUE_H
