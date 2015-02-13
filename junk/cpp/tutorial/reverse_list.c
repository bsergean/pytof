/* vim:set tabstop=4 shiftwidth=4 expandtab: */
#include <stdio.h>
#include <strings.h>

typedef struct list;
typedef struct list {
    list* next;
    char value;
};

void reverse(char s[]) {
    int i, j;
    puts(s);
    
    for (i = 0, j = strlen(s) - 1; 
         i < j; 
         ++i, --j) {
         #if 0
        printf("s[i] = %c\n", s[i]);
        printf("s[j] = %c\n", s[j]);
        puts("");
        continue;
        #endif
        
        int tmp = s[j];
        s[j] = s[i];
        s[i] = tmp;
    }
    puts(s);
}

int main() {
    char foo[] = "0123456789";
    char bar[] = "0123456789A";
    char baz[]  = "0";
    char bam[]  = "";

    reverse(foo);
    reverse(bar);
    reverse(baz);
    reverse(bam);
}
