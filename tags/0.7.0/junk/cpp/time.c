#include <unistd.h>
#include <time.h>

#include <stdio.h>
#include <math.h>

int main()
{
  time_t value;
  char datebuf[100];
  datebuf[0] = 0;

  time_t t = time(0);
  printf("%d\n", t);
  
  struct tm *tm = localtime(&t);
  strftime(datebuf, 99, "localtime: %Y-%m-%d %H:%M:%S", tm);
  puts(datebuf);

  struct tm *tm2 = gmtime(&t);
  strftime(datebuf, 99, "gmttime: %Y-%m-%d %H:%M:%S", tm2);
  puts(datebuf);

  printf("difftime tests\n");
  time_t gmt_t = mktime(tm2);
  printf("%d\n", gmt_t);

  printf("%f\n", (difftime(t, gmt_t) / 3600) );
  printf("%f\n", (difftime(gmt_t, t) / 3600) );
  
  printf("%d\n", (int) (difftime(t, gmt_t) / 3600) );
  printf("%d\n", (int) (difftime(gmt_t, t) / 3600) );
  
  return 0;
}

/*
  // with QT

  // /CreationDate(D:(<CREATION_DATE>-08'00')
  //   20041103225737 = Year-Day-Mounth-Hour-Minute-Seconds
  now.setTimeSpec(Qt::UTC);
  now = QDateTime::currentDateTime(); // Qt::UTC
  qDebug() << now;
  // ("Fri Jan 27 17:43:17 2006")
  // 20060027174343-05'00' // FIXME: there is maybe a bug in the 7.0.7 mounth
  date = now.toString("yyyyMMddhhmmss");
  date += "-00'00'";
  qDebug() << date;
*/

/*
  // with wx
  static void
getPDFFormatedDateTime(vector<int>& time)
{
  // Compute the difference beetween our time and GMT Time.
  // Now
  wxDateTime date = wxDateTime::Now();
  time.push_back(date.GetYear());
  time.push_back(date.GetMonth());
  time.push_back(date.GetDay());
  time.push_back(date.GetHour());
  time.push_back(date.GetMinute());
  time.push_back(date.GetSecond());

  // GMT
  wxDateTime dateGMT = wxDateTime::Now().ToGMT();
  
  wxDateTime dmax, dmin;
  int sign;
  
  if (date.IsLaterThan(dateGMT)) {
    sign = -1;
    dmax = wxDateTime(date.GetHour(), date.GetMinute(), date.GetSecond());
    dmin = wxDateTime(dateGMT.GetHour(), dateGMT.GetMinute(), dateGMT.GetSecond());
  } else {
    sign = +1;
    dmax = wxDateTime(dateGMT.GetHour(), dateGMT.GetMinute(), dateGMT.GetSecond());
    dmin = wxDateTime(date.GetHour(), date.GetMinute(), date.GetSecond());;
  }

  long secs = 0;
  while (dmax.IsLaterThan(dmin))
    {
      dmin += wxTimeSpan(0,0,1);
      secs += 1;
    }

  R3DLOGDEB0(("%d %d %d %d\n",
	      sign,
	      (int)(secs / 3600),
	      (int) fmod( (double) secs, (double) 3600) / 60,
	      (int) fmod( (double) secs, (double) 3600) % 60));

  time.push_back(sign);
  time.push_back((int)(secs / 3600));
  time.push_back((int) fmod( (double) secs, (double) 3600) / 60);
}

*/
