#pragma once

class PercolationStats {
public:
    // perform T independent experiments on an N-by-N grid
    PercolationStats(int N, int T);

    double mean() const;
    double stddev();

    // low  endpoint of 95% confidence interval
    double confidenceLo();

    // high endpoint of 95% confidence interval
    double confidenceHi();

private:
    double mMean;
};
