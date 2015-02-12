#include <fstream>
#include <iostream>
#include <boost/iostreams/filtering_streambuf.hpp>
#include <boost/iostreams/copy.hpp>
#include <boost/iostreams/filter/gzip.hpp>

int main(int argc, char** argv) 
{
    using namespace std;
    using namespace boost::iostreams;

    ifstream file(argv[1], ios_base::in | ios_base::binary);
    filtering_streambuf<input> in;
    in.push(gzip_decompressor());
    in.push(file);
    copy(in, cout);
}
