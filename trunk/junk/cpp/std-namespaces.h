#include <vector> // for pair...

#ifndef NO_NAMESPACES
std::pair<int, float> OnSaveAsUI();
#else
using namespace std;
pair<int, float> OnSaveAsUI();
#endif
