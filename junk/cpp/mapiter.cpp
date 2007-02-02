#include <map>
#include <string>
#ifndef NO_NAMESPACES
using namespace std;
#endif

const char* get_u3d_tmp_filename()
{
  return "/tmp/tmpU3DFilename.u3d";
}

const char* get_u3d_bmp_tmp_filename()
{
  return "/tmp/tmpU3DFilename.bmp";
}

const char* get_u3d_js_tmp_filename()
{
  return "/tmp/tmpU3DFilename.js";
}

int main()
{
  map<string,string> tmpFiles;
  tmpFiles["bmp"] = get_u3d_bmp_tmp_filename();
  tmpFiles["u3d"] = get_u3d_tmp_filename();
  tmpFiles["js"] = get_u3d_js_tmp_filename();

  // cleaning : remove tmp files.
  for (map<string, string>::const_iterator it = tmpFiles.begin();
       it != tmpFiles.end();  ++it)
    if (access(it->second.c_str(), 0) == 0)
      unlink(it->second.c_str());
  
}
