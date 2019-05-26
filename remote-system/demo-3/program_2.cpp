#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
using namespace std;
void fillArray(vector<int> &vlist){string line;ifstream myfile("outputs");if(myfile.is_open()){while(getline(myfile,line)){stringstream s2i(line);int x=0;s2i>>x;vlist.push_back(x);}myfile.close();}}void emptyArray(string filename, vector<int> &vlist);
void emptyArray(vector<int> &vlist){ofstream myfile ("outputs");if(myfile.is_open()){for(int item:vlist){myfile<<item<<endl;}myfile.close();}}
int main () {
  vector<int> vlist, rlist;

  fillArray(vlist);
  for (int item : vlist)
  {
    rlist.push_back(item + 5);
  }
  emptyArray(rlist);
  return 0;}