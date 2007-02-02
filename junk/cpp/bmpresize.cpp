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

// MyApp
class MyApp: public wxApp
{
public:
    virtual bool OnInit();
};

class MyImageFrame : public wxFrame
{
public:
  MyImageFrame(wxFrame *parent, const wxBitmap& bitmap)
    : wxFrame(parent, -1, _T("Double click to save"),
	      wxDefaultPosition, wxDefaultSize,
	      wxCAPTION | wxSYSTEM_MENU),
      m_bitmap(bitmap)
  {
    SetClientSize(bitmap.GetWidth(), bitmap.GetHeight());
  }

  void OnPaint(wxPaintEvent& WXUNUSED(event))
  {
    wxPaintDC dc( this );
    //TRUE for masked images
    dc.DrawBitmap( m_bitmap, 0, 0, TRUE );
  }
  
private:
    wxBitmap m_bitmap;

    DECLARE_EVENT_TABLE()
};
  
// main program
IMPLEMENT_APP(MyApp)

BEGIN_EVENT_TABLE(MyImageFrame, wxFrame)
  EVT_PAINT(MyImageFrame::OnPaint)
END_EVENT_TABLE()

bool MyApp::OnInit()
{
  if (argc != 4)
    {
      puts("usage: bmpresize <width> <height> <filename>");
      exit(0);
    }
  
  wxString filename(argv[3]);
  wxImage image;
  image.LoadFile(filename);

  // render orig image
  (new MyImageFrame((wxFrame *)NULL, wxBitmap(image)))->Show();

  // then Scale it
  int w_scale = atoi(argv[1]);
  int h_scale = atoi(argv[2]);

  // render scaled image
  wxBitmap ScaledBitmap(image.Scale(w_scale, h_scale));
  (new MyImageFrame((wxFrame *)NULL, ScaledBitmap))->Show();

  // save it
  wxString scaledfilename;
  scaledfilename.Printf("%s%dx%d.bmp", filename.c_str(), w_scale, h_scale);

  ScaledBitmap.SaveFile(scaledfilename, wxBITMAP_TYPE_BMP);
  
  return TRUE;
}
