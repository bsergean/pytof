
/*
 * File: Capture3D/r3d/common/chrono.cpp
 * Author: Jean-Francois Dockes
 * Purpose: Measure and display time intervals
 * History: 
 */

/*
 * ADOBE CONFIDENTIAL NOTICE
 *
 * Copyright 2002 - 2004 OKYZ S.A.
 * All Rights Reserved.
 *
 * Copyright 2005 - 2006 Adobe Systems Incorporated
 * All Rights Reserved.
 *
 * NOTICE: All information contained herein is, and remains the property
 * of Adobe Systems Incorporated and its suppliers, if any. The
 * intellectual and technical concepts contained herein are proprietary to
 * Adobe Systems Incorporated and its suppliers and may be covered by U.S.
 * and Foreign Patents, patents in process, and are protected by trade
 * secret or copyright law. Dissemination of this information or
 * reproduction of this material is strictly forbidden unless prior
 * written permission is obtained from Adobe Systems Incorporated.
 *
 * ADOBE CONFIDENTIAL NOTICE 
 */
#ifdef HAVE_CONFIG_H
#include "uxconfig.h"
#endif

//#ifdef R3D_UNIX
#ifndef WIN32

#ifndef TEST_CHRONO

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#ifndef _WINDOWS
#include <sys/time.h>
#endif
#include "chrono.h"
   
////////////////////
// Internal redefinition of system time interface to help with dependancies
struct m_timespec {
  time_t tv_sec;
  long   tv_nsec;
}; 

#ifndef CLOCK_REALTIME
#define CLOCK_REALTIME 1
#endif

#define MILLIS(TV) ( (long)(((TV).tv_sec - m_secs) * 1000 + \
  ((TV).tv_nsec - m_nsecs) / 1000000))

#define MICROS(TV) ( (long)(((TV).tv_sec - m_secs) * 1000000 + \
  ((TV).tv_nsec - m_nsecs) / 1000))
  
// We use gettimeofday instead of clock_gettime for now and get only
// uS resolution, because clock_gettime is more configuration trouble
// than it's worth
static void gettime(int, struct m_timespec *ts)
{
  struct timeval tv;
  gettimeofday(&tv, 0);
  ts->tv_sec = tv.tv_sec;
  ts->tv_nsec = tv.tv_usec * 1000;
}
///// End system interface

static m_timespec frozen_tv;
void Chrono::refnow()
{
  gettime(CLOCK_REALTIME, &frozen_tv);
}

Chrono::Chrono()
{
  restart();
}

// Reset and return value before rest in milliseconds
long Chrono::restart()
{
  struct m_timespec tv;
  gettime(CLOCK_REALTIME, &tv);
  long ret = MILLIS(tv);
  m_secs = tv.tv_sec;
  m_nsecs = tv.tv_nsec;
  return ret;
}

// Get current timer value, milliseconds
long Chrono::millis(int frozen)
{
  if (frozen) {
    return MILLIS(frozen_tv);
  } else {
    struct m_timespec tv;
    gettime(CLOCK_REALTIME, &tv);
    return MILLIS(tv);
  }
}

//
long Chrono::micros(int frozen)
{
  if (frozen) {
    return MICROS(frozen_tv);
  } else {
    struct m_timespec tv;
    gettime(CLOCK_REALTIME, &tv);
    return MICROS(tv);
  }
}

float Chrono::secs(int frozen)
{
  struct m_timespec tv;
  gettime(CLOCK_REALTIME, &tv);
  float secs = (float)(frozen?frozen_tv.tv_sec:tv.tv_sec - m_secs);
  float nsecs = (float)(frozen?frozen_tv.tv_nsec:tv.tv_nsec - m_nsecs); 
  //fprintf(stderr, "secs %.2f nsecs %.2f\n", secs, nsecs);
  return secs + nsecs * 1e-9;
}

//#endif /*_WINDOWS*/
#else 
///////////////////// test driver


#include <stdio.h>
#include <signal.h>
#include <unistd.h>

#include "chrono.h"

static char *thisprog;

static void
Usage(void)
{
    fprintf(stderr, "Usage : %s \n", thisprog);
    exit(1);
}
Chrono achrono;
Chrono rchrono;

void
showsecs(long msecs)
{
    fprintf(stderr, "%3.5f S", ((float)msecs) / 1000.0);
}

void
sigint(int sig)
{
    signal(SIGINT, sigint);
    signal(SIGQUIT, sigint);
    fprintf(stderr, "Absolute: ");
    showsecs(achrono.millis());
    fprintf(stderr, ". Relative: ");
    showsecs(rchrono.restart());
    fprintf(stderr, ".\n");
    if (sig == SIGQUIT)
      exit(0);
}
main(int argc, char **argv)
{
    
    thisprog = argv[0];
    argc--; argv++;

    if (argc != 0)
      Usage();

    for (int i = 0;i < 5000000;i++);
    fprintf(stderr, "Start secs: %.2g\n", (double)achrono.secs());


    fprintf(stderr, "Type ^C for intermediate result, ^\\ to stop\n");
    signal(SIGINT, sigint);
    signal(SIGQUIT, sigint);
    achrono.restart();
    rchrono.restart();
    while (1)
      pause();
}

#endif /*TEST_CHRONO*/

#endif // WIN32
