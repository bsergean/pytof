/* vim:set tabstop=4 shiftwidth=4 expandtab: */
#include <stdio.h>
#include <strings.h>

int add(int* ptr) {
    *ptr = *ptr + 1;
}

int main() {
    int i = 0;
    printf("%d %p %d\n", i, &i, sizeof(int));

    add(&i);
    printf("i = %d\n", i);
	
    return 0;
}
