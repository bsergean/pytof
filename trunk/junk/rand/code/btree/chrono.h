
/*
 * File: Capture3D/r3d/common/chrono.h
 * Author: Jean-Francois Dockes
 * Purpose: A very simplistic parameter file implementation.
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
 * NOTICE: All information contained herein is, and remains the property of
 * Adobe Systems Incorporated and its suppliers, if any. The intellectual and
 * technical concepts contained herein are proprietary to Adobe Systems
 * Incorporated and its suppliers and may be covered by U.S. and Foreign
 * Patents, patents in process, and are protected by trade secret or
 * copyright law. Dissemination of this information or reproduction of this
 * material is strictly forbidden unless prior written permission is obtained
 * from Adobe Systems Incorporated.
 *
 * ADOBE CONFIDENTIAL NOTICE 
 */

#ifndef _CHRONO_H_
#define _CHRONO_H_
/* @(#$Id: //depot/main/r3d/common/chrono.h#2 $  (C) 2002 OKYZ */

class Chrono {
  long	m_secs;		/* Time in seconds */
  long 	m_nsecs;        /* And nanoseconds (< 10E9) */
 public:
  Chrono();
  long restart();
  // Snapshot current time
  static void refnow();
  // Frozen means give time since the last refnow call (this is to
  // allow for using one actual system call to get values from many
  // chrono objects, like when examining timeouts in a queue
  long millis(int frozen = 0);
  long micros(int frozen = 0);
  float secs(int frozen = 0);
};

#endif /* _CHRONO_H_ */
