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
    unordered_map<string, unordered_map<string, float> > M;
    unordered_map<string, string> most_likely_next; // for each key, store the most likely next key that is in the cache
    unordered_map<string, string> least_likely_next; // for each key, store the least likely next key that is in the cache
    unordered_map<string, int> num_times_accessed; // number of times each key has been accessed
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
        update_probabilities(key);
        if (cache.count(key) > 0)
        {
            *val = cache[key];
            last_key = key;
            return true;
        }
        else
        {
            last_key = key;
            return false;
        }
    }
    void update_probabilities(string key) {
        if(num_times_accessed.count(key) <= 0) {
            num_times_accessed.insert(make_pair(key,0));
        }
        num_times_accessed[key] += 1;
        if(M.count(key) <= 0) {
            // add key to M with 1/n probabilities for each column
            int total_num_keys = num_times_accessed.size();
            unordered_map<string,float> key_map;
            for(auto i : num_times_accessed) {
                key_map.insert(make_pair(i.first, 1/total_num_keys));
            }
            M.insert(make_pair(key,key_map));
        }
        if(last_key != ""){
            float new_val = M[key][last_key]*num_times_accessed[last_key]/num_times_accessed[key];
            if(M[last_key].count(key) <= 0) {
                M[last_key].insert(make_pair(key,new_val));
            }
            else {
                M[last_key][key] = new_val;
            }
            // Update most likely and least likely next if this key is in the cache
            if(cache.count(key) > 0) {
                if(M[last_key][key] >= M[last_key][most_likely_next[last_key]]){
                    most_likely_next[last_key] = key;
                }
                if(least_likely_next[last_key] == key) {

                }

            }
        }
    }

    bool remove(string key)
    {
        // remove from cache
        if(cache.count(key) <= 0) {
            return false;
        }
        // check if this key was most likely next or least likely next for any key and update
        for(auto i : most_likely_next) {
            if(i.second == key){
                float max_prob = 0;
                for(auto j : cache) {
                    if(M[i.first].count(j.first) > 0 && M[i.first][j.first] >= max_prob) {
                        most_likely_next[i.first] = j.first;
                        max_prob = M[i.first][j.first];
                    }
                }
            }
        }
        for(auto i : least_likely_next) {
            if(i.second == key){
                float least_prob = 1;
                for(auto j : cache) {
                    if(M[i.first].count(j.first) > 0 && M[i.first][j.first] <= least_prob) {
                        least_likely_next[i.first] = j.first;
                        least_prob = M[i.first][j.first];
                    }
                }
            }
        }
        // should we return the value?
        return true;
    }
    void print_m() {
        cout <<" num times accessed \n";
        for(auto i : num_times_accessed) {
            cout << "key: " << i.first << " value: " << i.second << " , ";

        }
        cout << "\n M \n";
        for(auto i : M) {
            cout << "last key: " << i.first << "\n";
            for(auto j : i.second) {
                cout << "key: " << j.first << " value: " << j.second << " , ";
            }
            cout << "\n";
        }
    }

    bool set(string key, string *val)
    {
        if(cache.count(key) > 0){
            cache[key] = *val;
            update_probabilities(key);
            return true;
        }
        while(cache.size() > capacity) {
            if(M.count(key) >= 0) {
                remove(least_likely_next[last_key]);
            }
        }
        cache.insert(make_pair(key,*val));
        update_probabilities(key);
        return true;
    }
};

int main()
{
    BCE *a = new BCE(26, 3);
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
