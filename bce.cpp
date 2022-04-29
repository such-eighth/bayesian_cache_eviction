#include <iostream>
#include <unordered_map>
#include <string>

using namespace std;

class BCE
{
    int alph_size;   // size of the alphabet
    int capacity;    // max size of the cache
    int used;        // current number of elements in the cache
    string last_key; // the last key to be accessed
    unordered_map<string, unordered_map<string, float>> M;
    unordered_map<string, string> cache;

public:
    BCE(int alph_size, int capacity)
    {
        this->alph_size = alph_size;
        this->capacity = capacity;
        this->used = 0;
        this->last_key = "";
    }

    bool get(string key, string *val)
    {
        if (cache.count(key) > 0)
        {
            *val = cache[key];

            return true;
        }
        else
        {
            return false;
        }
    }

    bool remove(string key)
    {
        cout << "remove";
        return true;
    }

    bool set(string key, string *val)
    {
        cout << "set" + key;
        return true;
    }
};

int main()
{
    BCE *a = new BCE(26, 5);
    return 0;
}
