
#include <cassert>
#include <iostream>
using namespace std;

int search(int* array, int size, int value)
{
    if (array[size - 1] <= value)
        return -1;

    int lower = 0; 
    int upper = size - 1; 
    int mid = 0;
    do {
        mid = lower + (upper - lower) / 2;
        if (value > array[mid]) {
            lower = mid + 1;
        } else {
            upper = mid - 1;
        }
        cout << lower << " " << mid << " " << upper << endl;
    } while (array[mid] != value && lower < upper);

    if (array[mid] != value) {
        return -1; 
    }

    cout << "found" << endl;
    
    while (array[++mid] == value) ;
    cout << mid << endl;
    return mid;
}

int main()
{
    int A[] = {1, 2, 2, 3, 3, 4, 5, 6, 9, 12, 13};
    assert(3 == search((int*) &A, 
                       sizeof(A) / sizeof(int), 
                       2)); 

    int B[] = {7, 8, 9, 9, 9, 9};
    assert(1 == search((int*) &B, 
                       sizeof(B) / sizeof(int), 
                       7)); 

    int C[] = {7, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9};
    assert(-1 == search((int*) &C, 
                        sizeof(C) / sizeof(int), 
                        9)); 

    int D[] = {7, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9};

    assert(-1 == search((int*) &D, 
                        sizeof(D) / sizeof(int), 
                        5)); 
}
