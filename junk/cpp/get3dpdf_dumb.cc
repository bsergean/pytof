// #include <CGPDFDocument.h>
#include <ApplicationServices/ApplicationServices.h>

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
     
    CGPDFOperatorTableSetCallback (myTable, "SubType", &op_MP);
    
     
    int numOfPages = CGPDFDocumentGetNumberOfPages (myDocument);// 1
    for (k = 0; k < numOfPages; k++) {
        myPage = CGPDFDocumentGetPage (myDocument, k + 1 );// 2
        myContentStream = CGPDFContentStreamCreateWithPage (myPage);// 3
        myScanner = CGPDFScannerCreate (myContentStream, myTable, NULL);// 4
        CGPDFScannerScan (myScanner);// 5
        CGPDFPageRelease (myPage);// 6
        CGPDFScannerRelease (myScanner);// 7
        CGPDFContentStreamRelease (myContentStream);// 8
     }
     CGPDFOperatorTableRelease(myTable);
}
