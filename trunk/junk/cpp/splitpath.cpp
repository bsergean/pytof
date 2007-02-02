#include <stdio.h>
#include "wx/string.h"
#include "wx/filename.h"

int main()
{
  wxString tmp("/tmp/caca.pipi");
  FILE* f = fopen(tmp.c_str(), "w");

  wxString Volume, path, name, ext;
  wxFileName::SplitPath(tmp, &Volume, &path, &name, &ext);

  printf("filename without extension : %s\n", name.c_str());
  
  return 0;
}
