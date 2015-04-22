//
//  main.cpp
//  xcode_coding_practice
//
//  Created by Benjamin Sergeant on 4/18/15.
//  Copyright (c) 2015 Benjamin Sergeant. All rights reserved.
//

#include <iostream>

int
knuthLarge(int N)
{
    int h = 1;
    int max = (N - 1) / 3;
    while (true) {
        if ((h+1) >= max) break;
        h += 3;
    }
    
    return h;
}

int
main(int argc, const char * argv[])
{
    // insert code here...
    int N = 17;
    std::cout << N << " " << knuthLarge(N) << std::endl;
    return 0;
}