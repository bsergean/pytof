#include <stdio.h>
#include "wx/datetime.h"
#include <math.h>

void print_date(const char* prefix, wxDateTime date)
{
  printf("%s: %d:%d:%d-%d:%d:%d\n", prefix,
	 date.GetYear(), date.GetMonth(), date.GetDay(),
	 date.GetHour(), date.GetMinute(), date.GetSecond());
}

int main()
{
  // now
  wxDateTime date = wxDateTime::Now();
  // GMT
  wxDateTime dateGMT = wxDateTime::Now().ToGMT();

  print_date("now", date);
  print_date("gmt", dateGMT);

#if 0
  wxDateTime dmax(23,12,26);
  wxDateTime dmin(21,56,41);
#else

  wxDateTime dmax, dmin;
  char sign;
  
  if (date.IsLaterThan(dateGMT)) {
    sign = '-';
    dmax = wxDateTime(date.GetHour(), date.GetMinute(), date.GetSecond());
    dmin = wxDateTime(dateGMT.GetHour(), dateGMT.GetMinute(), dateGMT.GetSecond());
  } else {
    sign = '+';
    dmax = wxDateTime(dateGMT.GetHour(), dateGMT.GetMinute(), dateGMT.GetSecond());
    dmin = wxDateTime(date.GetHour(), date.GetMinute(), date.GetSecond());;
  }
  
#endif

  long secs = 0;
  while (dmax.IsLaterThan(dmin))
    {
      dmin += wxTimeSpan(0,0,1);
      secs += 1;
    }

  printf("%c%d %d %d\n",
	 sign,
	 (int)(secs / 3600),
	 (int) fmod(secs, 3600) / 60,
	 (int) fmod(secs, 3600) % 60);
  
  return 0;
}
