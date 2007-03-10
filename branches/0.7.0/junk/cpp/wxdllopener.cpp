#include "wx/wxprec.h"

#ifdef __BORLANDC__
#pragma hdrstop
#endif

#ifndef WX_PRECOMP
#include "wx/wx.h"
#endif

#include "wx/image.h"
#include "wx/file.h"
#include "wx/mstream.h"
#include "wx/wfstream.h"
#include "wx/quantize.h"

#include "wx/dynlib.h"
#include "wx/dynload.h"

// MyApp
class MyApp: public wxApp
{
public:
    virtual bool OnInit();
};

// main program
IMPLEMENT_APP(MyApp)

//BEGIN_EVENT_TABLE(MyImageFrame, wxFrame)
//  EVT_PAINT(MyImageFrame::OnPaint)
//END_EVENT_TABLE()

bool MyApp::OnInit()
{
  if (argc != 2)
    {
      puts("usage: wxdllopener <filename>");
      exit(0);
    }
  
  wxString dllname(argv[1]);
  printf("opening %s : ", dllname.c_str());

  wxDynamicLibrary *lib = new(wxDynamicLibrary);
  if (!lib->Load(dllname))
      puts("Fail");
  else
      puts("Success");
    
  return FALSE;
}
