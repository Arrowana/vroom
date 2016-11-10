import pytest
import trackdrawer

def test_generate_parallel():
    n = 10
    curve = [[i, 0] for i in range(n)]
    distance = 1
    parallel = trackdrawer.generate_parallel(curve, distance)
    print(parallel)
    assert parallel == [[i, 1] for i in range(n-1)]


