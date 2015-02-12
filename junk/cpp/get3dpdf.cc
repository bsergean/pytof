// #include <CGPDFDocument.h>
#include <ApplicationServices/ApplicationServices.h>

#include <iostream>
#include <map>

using namespace std;
// g++ get3dpdf.cc -framework ApplicationServices
//
static void
op_MP (CGPDFScannerRef s, void *info)
{
    const char *name;
 
    if (!CGPDFScannerPopName(s, &name))
        return;
 
    printf("MP /%s\n", name);
}

int main(int argc, char** argv)
{
    CFStringRef path;
    CFURLRef url;
    CGPDFDocumentRef document;
    size_t count;
 
    path = CFStringCreateWithCString (NULL, argv[1],
                         kCFStringEncodingUTF8);
    url = CFURLCreateWithFileSystemPath (NULL, path, // 1
                        kCFURLPOSIXPathStyle, 0);
    CFRelease (path);

    CGPDFDocumentRef myDocument;
    myDocument = CGPDFDocumentCreateWithURL(url);// 1
    if (myDocument == NULL) {// 2
            CFRelease (url);
            return EXIT_FAILURE;
    }

    int k;
    CGPDFPageRef myPage;
    CGPDFScannerRef myScanner;
    CGPDFContentStreamRef myContentStream;

    CGPDFOperatorTableRef myTable;
     
    myTable = CGPDFOperatorTableCreate();

    // CGPDFOperatorTableSetCallback (myTable, "SubType", &op_MP);

    int pageCount = CGPDFDocumentGetNumberOfPages (myDocument);// 1
    for(int i=0; i<pageCount; i++) {
        CGPDFPageRef page = CGPDFDocumentGetPage(myDocument, i+1);

        CGPDFDictionaryRef pageDictionary = CGPDFPageGetDictionary(page);

        CGPDFArrayRef outputArray;
        if(!CGPDFDictionaryGetArray(pageDictionary, "Annots", &outputArray)) {
            return 1;
        }

        int arrayCount = CGPDFArrayGetCount( outputArray );
        if(!arrayCount) {
            continue;
        }

        for( int j = 0; j < arrayCount; ++j ) {
            CGPDFObjectRef aDictObj;
            if(!CGPDFArrayGetObject(outputArray, j, &aDictObj)) {
                return 1;
            }

            CGPDFDictionaryRef annotDict;
            if(!CGPDFObjectGetValue(aDictObj, kCGPDFObjectTypeDictionary, &annotDict)) {
                return 1;
            }

            CGPDFStringRef uriStringRef;
            if(!CGPDFDictionaryGetString(annotDict, "Subtype", &uriStringRef)) {
                cout << " - " << string( (char *) CGPDFStringGetBytePtr(
uriStringRef ), CGPDFStringGetLength( uriStringRef ) );
            }
            
        }
    }
}
