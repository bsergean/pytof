#include <assert.h>

#define BEGIN_HEAP_CHECK(function) int  function (#function);
#define END_HEAP_CHECK(function) assert(function.NoLeaks());

#define MAC(str) gl##str()
#define STR(str) #str

const char* toto = STR(tutu);

int main()
{
  BEGIN_HEAP_CHECK(toto)
  
  MAC(Begin);

  END_HEAP_CHECK(toto)
}
