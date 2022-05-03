#include <iostream>
#include <unordered_map>
#include <string>

using namespace std;

class BCE
{
    int alph_size;   // size of the alphabet
    int capacity;    // max size of the cache
    double gamma;    // hyperparameter
    string last_key; // the last key to be accessed
    unordered_map<string, unordered_map<string, int>> M;
    unordered_map<string, int> freq;
    unordered_map<string, string> cache;

public:
    BCE(int alph_size, int capacity, double gamma)
    {
        this->alph_size = alph_size;
        this->capacity = capacity;
        this->gamma = gamma;
        this->last_key;
    }

    bool get(string key, string *val)
    {
        freq[key]++;
        M[last_key][key]++;
        last_key = key;

        if (cache.count(key) > 0)
        {
            *val = cache[key];
            return true;
        }
        else
            return false;
    }

    bool remove(string key)
    {
        // remove from cache
        if (cache.count(key) == 0)
        {
            return false;
        }
        cache.erase(key);
        return true;
    }
    void print_m()
    {
        cout << "\n M \n";
        for (auto i : M)
        {
            cout << "last key: " << i.first << "\n";
            for (auto j : i.second)
            {
                cout << "key: " << j.first << " value: " << j.second << " , ";
            }
            cout << "\n";
        }
    }

    bool set(string key, string *val)
    {
        if (cache.size() == this->capacity)
        {
            // we currently access key
            double min_score;
            string min_key = "";

            // iterate through each of the keys to find that with min score
            for (auto i = freq.begin(); i != freq.end(); i++)
            {
                double score = this->gamma * i->second;

                if (M[key].count(i->first) != 0)
                    score += (1 - this->gamma) * M[key][i->first] / freq[key];

                if (score < min_score)
                {
                    min_score = score;
                    min_key = i->first;
                }
            }

            bool is_removed = remove(min_key);

            freq[key]++;
            M[last_key][key]++;
            last_key = key;
            cache[key] = *val;
        }
        else
        {
            freq[key]++;
            M[last_key][key]++;
            last_key = key;
            cache[key] = *val;
        }
        return true;
    }
};

int main()
{
    BCE *a = new BCE(26, 3, 0.5);
    string *value = new string("value");
    a->set("a", value);
    a->print_m();
    a->set("b", value);
    a->print_m();
    a->set("c", value);
    a->print_m();
    a->set("d", value);
    a->print_m();

    return 0;
}
