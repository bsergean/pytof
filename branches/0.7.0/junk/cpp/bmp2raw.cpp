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

#include "numtochar.h"

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
  if (argc != 2)
    {
      puts("usage: bmp2raw <filename>");
      exit(0);
    }

  // Load bmp into a wxImage
  wxString filename(argv[1]);
  wxImage image;
  image.LoadFile(filename);

  // output it to another bmp
  wxString rawfilename;
  rawfilename.Printf("%s_raw.bmp", filename.c_str());
  FILE* bmpFD = fopen(rawfilename.c_str(), "w");
  if (bmpFD == 0) {
    fprintf(stderr, "error while trying to open %s\n", filename.c_str());
    return FALSE;
  }
  
  // output a bmp header
  // Note: we store 32 bits values: no need for padding lines
  // -> problem for 24 bits... ?
  int NbPixels = image.GetWidth() * image.GetHeight();

  // Note: cant use struct for headers because of alignment issues !
  // The actually used size is 54 (40+14)
  unsigned char buf[100];
  memset(buf, 0, sizeof(buf));

  unsigned char *cp = buf;
  *cp++ = 'B';
  *cp++ = 'M';
  cp += inttoichar4(cp, 14 + 40 + NbPixels *4);		//bfsize
  cp += inttoichar2(cp, 0);				//rsvd1
  cp += inttoichar2(cp, 0);				//rsvd2
  cp += inttoichar4(cp, 14+40);				//offbits

  cp += inttoichar4(cp, 40); 				//biSize: WIN_NEW
  cp += inttoichar4(cp, image.GetWidth() );		//width
  cp += inttoichar4(cp, image.GetHeight());		//height
  cp += inttoichar2(cp, 1);				//planes
  cp += inttoichar2(cp, 24);				//bitcount
  cp += inttoichar4(cp, 0);			        //compression
  cp += inttoichar4(cp, NbPixels);			//sizeimage
  cp += inttoichar4(cp, 10);				//xpelsrmeter
  cp += inttoichar4(cp, 10);				//ypelspermeter
  cp += inttoichar4(cp, 0);				//clrUsed
  cp += inttoichar4(cp, 0);				//cldImportant

  // Write headers
  size_t header_size = (size_t)(cp - buf);
  
#define WRITE_BMP_HEADER
#ifdef WRITE_BMP_HEADER
  if (fwrite(buf, 1, cp - buf, bmpFD) != header_size) 
    {
      fclose(bmpFD);
      return false;
    }
#endif

  // output raw datas :
  unsigned char* sp = image.GetData();
  for (int i = 0; i < NbPixels;i++) {
    putc((int)sp[0], bmpFD);
    putc((int)sp[1], bmpFD);
    putc((int)sp[2], bmpFD);
    sp += 3;
  }

  fclose(bmpFD);  
  
  // Load it to check everything went well.
  image.LoadFile(rawfilename);
  (new MyImageFrame((wxFrame *)NULL, wxBitmap(image)))->Show();
  
  return TRUE;
}
