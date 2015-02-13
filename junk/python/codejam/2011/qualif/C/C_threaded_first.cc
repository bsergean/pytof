/*
g++ -O3 C.cc && ./a.out < input_real > out && diff out output_real_ok && echo OK
 */
#include <pthread.h>
//#include <stdio.h>
//#include <stdlib.h>

#include <iostream>
#include <vector>
#include <string>
#include <list>
#include <deque>
using namespace std;
typedef unsigned int uint;

int compute(deque<uint>& candies)
{
    uint L = candies.size();
    int winner = -1;
    for (uint z = 0; z < L; ++z) {
        for (uint i = 0; i < (L-1); ++i) {
            uint A = 0;
            uint realA = 0;
            uint B = 0;
            uint realB = 0;
            uint j = 0;

            deque<uint>::const_iterator it  = candies.begin();
            deque<uint>::const_iterator end = candies.end();

            for (; it != end; ++it) {
                uint elem = *it;
                if (j <= i) {
                    A ^= elem;
                    realA += elem;
                    j += 1;
                } else {
                    B ^= elem;
                    realB += elem;
                }
            }

            if (A == B) {
                int candidate = (int) std::max(realA, realB);
                if (candidate > winner) {
                    winner = candidate;
                }
            }
        }
        uint back = candies.back();
        candies.pop_back();
        candies.push_front(back);
    }

    return winner;
}

vector<int> answers;
pthread_mutex_t mutex;

struct WorkerDatas
{
    deque<uint> candies;
    uint answerIndex;
};

void *worker(void* _workerDatas)
{
	WorkerDatas* wd = (WorkerDatas*) _workerDatas;

    int answer = compute(wd->candies);

	pthread_mutex_lock (&mutex);
	answers[wd->answerIndex] = answer;
	pthread_mutex_unlock (&mutex);

	pthread_exit(NULL);
    return NULL;
}

int main()
{
    uint T;
    cin >> T;

    vector<deque<uint> > candyBag;
    candyBag.resize(T);
    answers.resize(T);

    for (uint c = 0; c < T; ++c) {
        uint N;
        cin >> N;

        deque<uint> candies;
        for (uint i = 0; i < N; ++i) {
            uint candy;
            cin >> candy;
            candies.push_back(candy);
        }

        candyBag[c] = candies;
    }

    // Work
    pthread_t threads[T];
    void *status;
    int rc;

    pthread_mutex_init(&mutex, NULL);

    for (uint t = 0; t < T; t++) {
        // printf("In main: creating thread %d\n", t);
        WorkerDatas* wd = new WorkerDatas;
        wd->candies = candyBag[t];
        wd->answerIndex = t;

        rc = pthread_create(&threads[t], NULL, worker, (void *) wd);
        if (rc){
            printf("ERROR; return code "
                   "from pthread_create() is %d\n", rc);
            exit(-1);
        }
    }

    // Join
    for (uint t = 0; t < T; t++) {
        rc = pthread_join(threads[t], &status);
        if (rc){
            printf("ERROR; return code "
                   "from pthread_join() is %d\n", rc);
            exit(-1);
        }
    }

    pthread_mutex_destroy(&mutex);

    // Report
    for (uint c = 0; c < T; ++c) {

        cout << "Case #" << c+1 << ": ";
        int ret = answers[c];
        if (ret == -1) cout << "NO";
        else cout << ret;
        cout << endl;
    }

    pthread_exit(NULL);
}
