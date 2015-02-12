#include <ApplicationServices/ApplicationServices.h>

#include <iostream>
#include <map>

using namespace std;


static const char * sPdfTypeNames[] = { "", "null", "boolean", "integer",
"real", "name", "string", "array", "dictionary", "stream" };

static int level = 1;


void DumpObjectProperties( CGPDFObjectRef obj )
{
    int cnt;
    
    CGPDFObjectType type = CGPDFObjectGetType( obj );
    switch( type )
    {
        case kCGPDFObjectTypeBoolean:
        {
            CGPDFBoolean pdfbool;
            if( CGPDFObjectGetValue( obj, kCGPDFObjectTypeBoolean, &pdfbool
) )
            {
                if( pdfbool )
                    cout << " - " << true;
                else
                    cout << " - " << false;
            }
        }
        break;
        
        case kCGPDFObjectTypeInteger:
        {
            CGPDFInteger pdfint;
            if( CGPDFObjectGetValue( obj, kCGPDFObjectTypeInteger, &pdfint )
)
                cout << " - " << pdfint;
        }
        break;
        
        case kCGPDFObjectTypeReal:
        {
            CGPDFReal pdfreal;
            if( CGPDFObjectGetValue( obj, kCGPDFObjectTypeReal, &pdfreal ) )
                cout << " - " << pdfreal;
        }
        break;
        
        case kCGPDFObjectTypeName:
        {
            const char * name;
            if( CGPDFObjectGetValue( obj, kCGPDFObjectTypeName, &name ) )
                cout << " - " << name;
        }
        break;
        
        case kCGPDFObjectTypeString:
        {
            CGPDFStringRef pdfstr;
            if( CGPDFObjectGetValue( obj, kCGPDFObjectTypeString, &pdfstr )
)
                cout << " - " << string( (char *) CGPDFStringGetBytePtr(
pdfstr ), CGPDFStringGetLength( pdfstr ) );
        }
        break;
        
        case kCGPDFObjectTypeArray:
        {
            CGPDFArrayRef array;
            if( CGPDFObjectGetValue( obj, kCGPDFObjectTypeArray, &array ) )
            {
                cnt = CGPDFArrayGetCount( array );
                cout << " - " << "entries: " << cnt;
            }
        }
        break;
        
        case kCGPDFObjectTypeDictionary:
        {
            CGPDFDictionaryRef dict;
            if( CGPDFObjectGetValue( obj, kCGPDFObjectTypeDictionary, &dict
) )
            {
                cnt = CGPDFDictionaryGetCount( dict );
                cout << " - " << "entries: " << cnt;
            }
        }
        break;
    }
    cout << endl << flush;
}


void DumpObject( const char * key, CGPDFObjectRef obj, void * info )
{
    for( int i = 0; i < level; ++i )
        cout << "| ";

    CGPDFObjectType type = CGPDFObjectGetType( obj );
    if( type >= 1 && type < sizeof( sPdfTypeNames ) / sizeof( char *) )
    {
        cout << key << ": " << sPdfTypeNames[type];
        DumpObjectProperties( obj );
    }
    else
        cout << key << ": " << "unrecognized object type " << type << endl
<< flush;
    
    switch( type )
    {
        case kCGPDFObjectTypeDictionary:
        {
            if( strcmp( "Parent", key ) )
            {
                ++level;
                CGPDFDictionaryRef dict;
                if( CGPDFObjectGetValue( obj, kCGPDFObjectTypeDictionary,
&dict ) )
                    CGPDFDictionaryApplyFunction( dict, DumpObject, NULL );
                --level;
            }
        }
        break;

        case kCGPDFObjectTypeArray:
        {
                ++level;
                CGPDFArrayRef array;
                if( CGPDFObjectGetValue( obj, kCGPDFObjectTypeArray, &array
) )
                {
                    int arraycnt = CGPDFArrayGetCount( array );
                    for( int i = 0; i < arraycnt; ++i )
                    {
                        CGPDFObjectRef aryobj;
                        if( CGPDFArrayGetObject( array, i, &aryobj ) )
                        {
                            char tmp[16];
                            sprintf( tmp, "%d", i );
                            DumpObject( tmp, aryobj, NULL );
                        }
                    }
                }
                --level;
        }
        break;
            
        case kCGPDFObjectTypeStream:
        {
            ++level;
            CGPDFStreamRef strm;
            if( CGPDFObjectGetValue( obj, kCGPDFObjectTypeStream, &strm ) )
            {
                CGPDFDictionaryRef dict = CGPDFStreamGetDictionary( strm );
                if( dict )
                    CGPDFDictionaryApplyFunction( dict, DumpObject, NULL );
            }
            --level;
        }
        break;
    }
}


int main (int argc, char * const argv[])
{
    if( argc != 2 )
    {
        cerr << "usage: pdfdir source.pdf" << endl << flush;
        return 1;
    }
    
    CFStringRef path = CFStringCreateWithCString( NULL, argv[1],
kCFStringEncodingUTF8 );
    CFURLRef url = CFURLCreateWithFileSystemPath( NULL, path,
kCFURLPOSIXPathStyle, 0 );
    CGPDFDocumentRef doc = CGPDFDocumentCreateWithURL( url );
    if( !doc )
    {
        cerr << "could not open source pdf file" << endl << flush;
        return 1;
    }
    
    int pgcnt = CGPDFDocumentGetNumberOfPages( doc );
    if( pgcnt <= 0 )
    {
        cerr << "source pdf file has no pages" << endl << flush;
        return 1;
    }
    
    cout << "page count: " << pgcnt << endl << flush;
    for( int i1 = 0; i1 < pgcnt; ++i1 )
    {
        CGPDFPageRef pg = CGPDFDocumentGetPage( doc, i1 + 1 );
        if( !pg )
        {
            cerr << "failed to read page " << i1 + 1 << " of source pdf file" << endl << flush;
            return 1;
        }
        
        CGPDFDictionaryRef dict = CGPDFPageGetDictionary( pg );
        if( !dict )
        {
            cerr << "failed to read dictionary for page " << i1 + 1 << " of source pdf file" << endl << flush;
            return 1;
        }
        
        cout << "page: " << i1 + 1 << endl << flush;
        CGPDFDictionaryApplyFunction( dict, DumpObject, NULL );
    }
    
    return 0;
}
