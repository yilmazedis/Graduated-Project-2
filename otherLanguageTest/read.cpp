#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

void fillArray(string filename, vector<int> &vlist);
void emptyArray(string filename, vector<int> &vlist);

int main () {
  
  vector<int> vlist, rlist;
  string inputfile = "output.txt";
  string outputfile = "output.txt";

  // Fill Vector from File
  fillArray(inputfile, vlist);

  /* Calculate Area */
  for (int item : vlist)
  {
    rlist.push_back(item + 5);
  }
  /* Calculate Area */

  // Empty Vector to File
  emptyArray(outputfile, rlist);

  return 0;
}

void emptyArray(string filename, vector<int> &vlist) {

  ofstream myfile (filename);
  
  if (myfile.is_open())
  {
    for (int item : vlist)
    {
      myfile << item << endl;
    }
    
    myfile.close();
  }
  else cout << "Unable to open file";
}

void fillArray(string filename, vector<int> &vlist) {

  string line;
  
  ifstream myfile (filename);
  

  if (myfile.is_open())
  {
    while ( getline (myfile,line) )
    {
      stringstream s2i(line);
      int x = 0; 
      s2i >> x; 
      vlist.push_back(x);
    }
    myfile.close();
  }
  else
    cout << "Unable to open file"; 
}