#include <sys/stat.h>

#include <fstream>
#include <iostream>
#include <vector>
using namespace std;

bool readFile(vector<char>& bytes, char* fileName)
{
    ifstream stream;
    stream.open(fileName, ifstream::in);

    struct stat st;
    stat(fileName, &st);
    cout << st.st_size << endl;
    bytes.reserve(st.st_size);
    stream.read(&bytes[0], st.st_size);
    stream.close();

    return true;
}

int main(int argc, char** argv)
{
    vector<char> bytes;
    readFile(bytes, argv[1]);
    cout << bytes.size() << endl;

    return 0;
}
