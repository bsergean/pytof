#include <stdio.h>
#include <iostream>
#include <vector>
using namespace std;

int W, H;
vector< vector<char> > image;
vector< pair<int, int> > path;
vector< vector<bool> > visited;

pair<int, int> entry()
{
    for (int j = 0; j < image.size(); j++)
        for (int i = 0; i < image[j].size(); i++)
            if (image[j][i] == 'G')
                return pair<int, int>(i, j);

    return pair<int, int>(-1, -1);
}

vector< pair<int, int> > neighboors(int x, int y)
{
    vector< pair<int, int> > N;

    N.push_back( pair<int, int>(x+1, y) );
    N.push_back( pair<int, int>(x, y+1) );
    N.push_back( pair<int, int>(x-1, y) );
    N.push_back( pair<int, int>(x, y-1) );

    for (vector< pair<int, int> >::iterator it = N.begin();
        it != N.end(); )
    {
        int i = it->first;
        int j = it->second;

        if (i < 0 || i == W || j < 0 || j == H ||
           (image[j][i] != 'W' && 
            image[j][i] != 'G' && 
            image[j][i] != 'R')) {
            it = N.erase(it);
        } else {
            ++it;
        }
    }
    return N;
}

int cnt = 1;
void walk_rec(int i, int j)
{
    if (cnt++ % 100000 == 0) cout << cnt / 100000 << endl;
    // cout << cnt++ << endl;
    // cout << i << " " << j << endl;
    if (visited[j][i]) return;
    visited[j][i] = true;

    path.push_back( pair<int, int>(i, j) );

    if (image[j][i] == 'R') {
        puts("solved !");
        cerr << "L = (";
        for (vector< pair<int, int> >::iterator it = path.begin();
            it != path.end();
            ++it) 
        {
            int x = it->first;
            int y = it->second;
            cerr << "(" << x << ", " << y << "), ";
        }
        cerr << ")" << endl;
        exit(0);
    } else {
        vector< pair<int, int> > N = neighboors(i,j);
        for (vector< pair<int, int> >::iterator it = N.begin();
            it != N.end();
            ++it) 
        {
            int x = it->first;
            int y = it->second;
            walk_rec(x, y);
        }
    }

    path.pop_back();
}

int process(char* input)
{
    FILE* stream = fopen(input, "r"); 
    fscanf(stream, "%d %d", &W, &H);
    fgetc(stream);

    cout << W << " " << H << endl;

    for (int j = 0; j < H; j++) {
        vector<char> line;
        line.reserve(W);
        for (int i = 0; i < W; i++) {
            char c;
            fscanf(stream, "%c", &c);
            line.push_back(c);
        }
        fgetc(stream);
        image.push_back(line);
    }

    // Init visited 
    for (int j = 0; j < H; j++) {
        vector<bool> line;
        line.resize(W);
        for (int i = 0; i < W; i++) {
            line[i] = false;
        }
        visited.push_back(line);
    }

    /*
    for (int j = 0; j < H; j++) {
        for (int i = 0; i < W; i++) {
            cout << image[j][i];
        }
        cout << endl;
    }
    */

    pair<int, int> A = entry();
    walk_rec(A.first, A.second);

    cout << "done";
}

int main(int argc, char** argv)
{
    process(argv[1]);
}

