#ifndef _NUMTOCHAR_H_
#define _NUMTOCHAR_H_
/* @(#$Id: //depot/main/r3d/common/numtochar.h#5 $  (C) 2002 J.F.Dockes */

/*
 * Small inline routines to convert between char bufs representing 
 * ints or floats in either motorola or intel format and machine values
 * 
 * These could maybe be made much faster but beware that the char bufs
 * are not supposed to be aligned in any way
 */


/* LOW_BYTE_FIRST is only used for floating point conversions. Ints are
 * done with arithmetic, architecture-independant code  */

/* All windows machines are little-endian. Unix machines use autoconf
   to find out about this */
#if defined(WIN32) && !defined(LOW_BYTE_FIRST)
#  define LOW_BYTE_FIRST 1
#endif /* WIN32 */

/* Be semi-compatible with historical crap. We used to define LOW_BYTE_FIRST 
   (with no value) or nothing. We now WANT something to be defined, but set
   LOW_BYTE_FIRST to 1 if it's just defined */

#ifdef LOW_BYTE_FIRST
#  if LOW_BYTE_FIRST != 0
#    undef LOW_BYTE_FIRST
#    define LOW_BYTE_FIRST 1
#  endif
#endif

/* autoconf default is to define WORDS_BIGENDIAN when appropriate */
#ifdef WORDS_BIGENDIAN
#  define LOW_BYTE_FIRST 0
#endif /* WORDS_BIGENDIAN */

#if !defined(LOW_BYTE_FIRST) || (LOW_BYTE_FIRST != 0 && LOW_BYTE_FIRST != 1)
#  error Must define LOW_BYTE_FIRST to 0 or 1
#endif

 /***********************
 * Routines converting charbufs representing ints in motorola format 
 * (TCP/IP, SCSI, etc...). Because of the way we do it, the routines
 * are independant of the cpu arch */
inline unsigned int char4toint(const unsigned char *f)
{
    return(
	   ((unsigned int)(f[3])) +
	   ((unsigned int)(f[2]) << 8) +
	   ((unsigned int)(f[1]) << 16) +
	   ((unsigned int)(f[0]) << 24));
}
inline unsigned int char2toint(const unsigned char *f)
{
    return(
	   (unsigned int)(f[1]) + 
	   ((unsigned int)(f[0]) << 8));
}
inline int inttochar4(unsigned char *cdb, unsigned int addr)
{
    cdb[0] =(unsigned char) ((addr & 0xff000000) >> 24);
    cdb[1] =(unsigned char) ( (addr & 0x00ff0000) >> 16);
    cdb[2] =(unsigned char) ( (addr & 0x0000ff00) >> 8);
    cdb[3] =(unsigned char) (  addr & 0x000000ff);
    return 4;
}
inline int inttochar2(unsigned char *cdb, unsigned int cnt)
{
    cdb[0] =(unsigned char) ( (cnt & 0x0000ff00) >> 8);
    cdb[1] =(unsigned char) (  cnt & 0x000000ff);
    return 2;
}

/***************************************
 * Routines for char bufs in Intel format  Because of the way we do it,
 * the routines are independant of the cpu arch */
inline unsigned int ichar4toint(const unsigned char *f)
{
    return(
	   ((unsigned int)(f[0])) +
	   ((unsigned int)(f[1]) << 8) +
	   ((unsigned int)(f[2]) << 16) +
	   ((unsigned int)(f[3]) << 24));
}
inline unsigned int ichar2toint(const unsigned char *f)
{
    return(
	   (unsigned int)(f[0]) + 
	   ((unsigned int)(f[1]) << 8));
}
inline int inttoichar4(unsigned char *cdb, unsigned int addr)
{
    cdb[3] =(unsigned char) ( (addr & 0xff000000) >> 24);
    cdb[2] =(unsigned char) ( (addr & 0x00ff0000) >> 16);
    cdb[1] =(unsigned char) ( (addr & 0x0000ff00) >> 8);
    cdb[0] =(unsigned char) (  addr & 0x000000ff);
    return 4;
}
inline int inttoichar2(unsigned char *cdb, unsigned int cnt)
{
    cdb[1] =(unsigned char) ( (cnt & 0x0000ff00) >> 8);
    cdb[0] =(unsigned char) (  cnt & 0x000000ff);
    return 2;
}

/** Bcd to int conversions **/
inline unsigned int bcdtoint(unsigned char c)
{
  return 10 * ((c & 0xf0) >> 4) + (c & 0xf);
}

inline unsigned char inttobcd(unsigned int i)
{
  return (unsigned char)((((i / 10) % 10) << 4) | (i % 10));
}


/**************** 
 * From charbufs in intel order to floating point values: */

/* Note that we don't try to optimize with casting around because the charbuf 
 * maybe unaligned */
inline float ichar4tofloat(const unsigned char *c)
{
  float f;
#if LOW_BYTE_FIRST != 0
  ((unsigned char *)&f)[0] = c[0];
  ((unsigned char *)&f)[1] = c[1];
  ((unsigned char *)&f)[2] = c[2];
  ((unsigned char *)&f)[3] = c[3];
#else 
  ((unsigned char *)&f)[0] = c[3];
  ((unsigned char *)&f)[1] = c[2];
  ((unsigned char *)&f)[2] = c[1];
  ((unsigned char *)&f)[3] = c[0];
#endif
  return f;
}

inline double ichar8todouble(const unsigned char *c)
{
  double d;
#if LOW_BYTE_FIRST != 0
  ((unsigned char *)&d)[0] = c[0];
  ((unsigned char *)&d)[1] = c[1];
  ((unsigned char *)&d)[2] = c[2];
  ((unsigned char *)&d)[3] = c[3];
  ((unsigned char *)&d)[4] = c[4];
  ((unsigned char *)&d)[5] = c[5];
  ((unsigned char *)&d)[6] = c[6];
  ((unsigned char *)&d)[7] = c[7];
#else 
  ((unsigned char *)&d)[0] = c[7];
  ((unsigned char *)&d)[1] = c[6];
  ((unsigned char *)&d)[2] = c[5];
  ((unsigned char *)&d)[3] = c[4];
  ((unsigned char *)&d)[4] = c[3];
  ((unsigned char *)&d)[5] = c[2];
  ((unsigned char *)&d)[6] = c[1];
  ((unsigned char *)&d)[7] = c[0];
#endif
  return d;
}

inline int floattoichar4(unsigned char *c, const float *f)
{
#if LOW_BYTE_FIRST != 0
  c[0] = ((unsigned char *)f)[0];
  c[1] = ((unsigned char *)f)[1];
  c[2] = ((unsigned char *)f)[2];
  c[3] = ((unsigned char *)f)[3];
#else 
  c[3] = ((unsigned char *)f)[0];
  c[2] = ((unsigned char *)f)[1];
  c[1] = ((unsigned char *)f)[2];
  c[0] = ((unsigned char *)f)[3];
#endif
  return 4;
}

inline int doubletoichar8(unsigned char *c, const double *d)
{
#if LOW_BYTE_FIRST != 0
  c[0] = ((unsigned char *)d)[0];
  c[1] = ((unsigned char *)d)[1];
  c[2] = ((unsigned char *)d)[2];
  c[3] = ((unsigned char *)d)[3];
  c[4] = ((unsigned char *)d)[4];
  c[5] = ((unsigned char *)d)[5];
  c[6] = ((unsigned char *)d)[6];
  c[7] = ((unsigned char *)d)[7];
#else 
  c[7] = ((unsigned char *)d)[0];
  c[6] = ((unsigned char *)d)[1];
  c[5] = ((unsigned char *)d)[2];
  c[4] = ((unsigned char *)d)[3];
  c[3] = ((unsigned char *)d)[4];
  c[2] = ((unsigned char *)d)[5];
  c[1] = ((unsigned char *)d)[6];
  c[0] = ((unsigned char *)d)[7];
#endif
  return 8;
}

/**************** 
 * From charbufs in sparc order to floating point values: */

/* Note that we don't try to optimize with casting around because the charbuf 
 * maybe unaligned */

inline float char4tofloat(const unsigned char *c)
{
  float f;
#if LOW_BYTE_FIRST != 0
  ((unsigned char *)&f)[0] = c[3];
  ((unsigned char *)&f)[1] = c[2];
  ((unsigned char *)&f)[2] = c[1];
  ((unsigned char *)&f)[3] = c[0];
#else 
  ((unsigned char *)&f)[0] = c[0];
  ((unsigned char *)&f)[1] = c[1];
  ((unsigned char *)&f)[2] = c[2];
  ((unsigned char *)&f)[3] = c[3];
#endif
  return f;
}

inline double char8todouble(const unsigned char *c)
{
  double d;
#if LOW_BYTE_FIRST != 0
  ((unsigned char *)&d)[0] = c[7];
  ((unsigned char *)&d)[1] = c[6];
  ((unsigned char *)&d)[2] = c[5];
  ((unsigned char *)&d)[3] = c[4];
  ((unsigned char *)&d)[4] = c[3];
  ((unsigned char *)&d)[5] = c[2];
  ((unsigned char *)&d)[6] = c[1];
  ((unsigned char *)&d)[7] = c[0];
#else 
  ((unsigned char *)&d)[0] = c[0];
  ((unsigned char *)&d)[1] = c[1];
  ((unsigned char *)&d)[2] = c[2];
  ((unsigned char *)&d)[3] = c[3];
  ((unsigned char *)&d)[4] = c[4];
  ((unsigned char *)&d)[5] = c[5];
  ((unsigned char *)&d)[6] = c[6];
  ((unsigned char *)&d)[7] = c[7];
#endif
  return d;
}

inline int floattochar4(unsigned char *c, const float *f)
{
#if LOW_BYTE_FIRST != 0
  c[3] = ((unsigned char *)f)[0];
  c[2] = ((unsigned char *)f)[1];
  c[1] = ((unsigned char *)f)[2];
  c[0] = ((unsigned char *)f)[3];
#else 
  c[0] = ((unsigned char *)f)[0];
  c[1] = ((unsigned char *)f)[1];
  c[2] = ((unsigned char *)f)[2];
  c[3] = ((unsigned char *)f)[3];
#endif
  return 4;
}

inline int doubletochar8(unsigned char *c, const double *d)
{
#if LOW_BYTE_FIRST != 0
  c[7] = ((unsigned char *)d)[0];
  c[6] = ((unsigned char *)d)[1];
  c[5] = ((unsigned char *)d)[2];
  c[4] = ((unsigned char *)d)[3];
  c[3] = ((unsigned char *)d)[4];
  c[2] = ((unsigned char *)d)[5];
  c[1] = ((unsigned char *)d)[6];
  c[0] = ((unsigned char *)d)[7];
#else 
  c[0] = ((unsigned char *)d)[0];
  c[1] = ((unsigned char *)d)[1];
  c[2] = ((unsigned char *)d)[2];
  c[3] = ((unsigned char *)d)[3];
  c[4] = ((unsigned char *)d)[4];
  c[5] = ((unsigned char *)d)[5];
  c[6] = ((unsigned char *)d)[6];
  c[7] = ((unsigned char *)d)[7];
#endif
  return 8;
}

#endif /* _NUMTOCHAR_H_ */
