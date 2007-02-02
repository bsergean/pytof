#include "std-namespaces.h"

#include <vector>

#ifndef NO_NAMESPACES
using namespace std;
#endif

std::pair<int, float> OnSaveAsUI()
{
  pair<int, float> dummy;
  return dummy;
}

int main()
{
  OnSaveAsUI();
}
