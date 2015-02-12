#include <stdio.h>
#include <string>
using namespace std;

int main(int argc, char** argv)
{
    string cmd("gzip > ");
    cmd += argv[1];

    FILE* f = popen(cmd.c_str(), "w");
    f.write(
    pclose(f);

    return 0;
}
