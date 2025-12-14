import time

import numpy as np
import pyfftw

from pybeamtools.physics.sliding_fft import (
    STFT_FFTW,
    STFT_FFTW_MANY,
    stft_fftw_1d_builder,
    stft_scipy_1d,
    stft_numpy_strided,
    stft_numpy_strided_v2,
    stft_welch,
    stft_fftw_1d,
)


def test_stft_perf():
    WINDOW = 4096 * 2
    STEP = 4096
    ITERATIONS = 500

    xs = int(352e6 / 1296 / 2)
    xi = pyfftw.empty_aligned(xs, dtype="int32", n=32)
    xi[:] = np.random.randint(-1e6, 1e6, int(352e6 / 1296 / 2), dtype="int32")

    assert xi.flags["C_CONTIGUOUS"]
    assert pyfftw.is_byte_aligned(xi)

    x = pyfftw.empty_aligned(xs, dtype="float32", n=32)
    t1 = time.perf_counter()
    x[:] = xi[:]
    x -= x.mean()
    t2 = time.perf_counter()
    print(f"Mean: {t2 - t1:.5f}")

    xref = x.copy()

    tsum = 0.0
    for i in range(ITERATIONS):
        t1 = time.perf_counter()
        P = stft_welch(x, WINDOW, STEP)
        t2 = time.perf_counter()
        if i > 0:
            tsum += t2 - t1
    print(f"STFT Welch: {tsum:.5f} {P[:4]}")
    assert np.all(x == xref)

    tsum = 0.0
    for i in range(ITERATIONS):
        t1 = time.perf_counter()
        P = stft_scipy_1d(x, WINDOW, STEP)
        t2 = time.perf_counter()
        if i > 0:
            tsum += t2 - t1
    print(f"STFT NUMPY: {tsum:.5f} {P[:4]}")
    assert np.all(x == xref)

    tsum = 0.0
    for i in range(ITERATIONS):
        t1 = time.perf_counter()
        P = stft_numpy_strided(x, WINDOW, STEP)
        t2 = time.perf_counter()
        if i > 0:
            tsum += t2 - t1
    print(f"STFT NUMPY STRIDED: {tsum:.5f} {P[:4]}")
    assert np.all(x == xref)

    tsum = 0.0
    for i in range(ITERATIONS):
        t1 = time.perf_counter()
        P = stft_numpy_strided_v2(x, WINDOW, STEP)
        t2 = time.perf_counter()
        if i > 0:
            tsum += t2 - t1
    print(f"STFT NUMPY STRIDED 2: {tsum:.5f} {P[:4]}")
    assert np.all(x == xref)

    tsum = 0.0
    for i in range(ITERATIONS):
        t1 = time.perf_counter()
        P = stft_fftw_1d(x, WINDOW, STEP)
        t2 = time.perf_counter()
        if i > 0:
            tsum += t2 - t1
    print(f"FFTW1: {tsum:.5f} {P[:4]}")
    assert np.all(x == xref)

    tsum = 0.0
    for i in range(ITERATIONS):
        t1 = time.perf_counter()
        P = stft_fftw_1d_builder(x, WINDOW, STEP)
        t2 = time.perf_counter()
        if i > 0:
            tsum += t2 - t1
    print(f"FFTW2: {tsum:.5f} {P[:4]}")
    assert np.all(x == xref)

    ##

    tsum = 0.0
    f1 = STFT_FFTW(WINDOW, STEP)

    for i in range(ITERATIONS):
        t1 = time.perf_counter()
        P = f1(x)
        t2 = time.perf_counter()
        if i > 0:
            tsum += t2 - t1
    print(f"FFTW3: {tsum:.5f} {P[:4]}")
    assert np.all(x == xref)

    ##

    tsum = 0.0
    nchunks = len(x) // WINDOW
    f1 = STFT_FFTW_MANY(nchunks, WINDOW)
    nchunks2 = (len(x) - STEP) // WINDOW
    f2 = STFT_FFTW_MANY(nchunks2, WINDOW)
    assert nchunks + nchunks2 == 32

    for i in range(ITERATIONS):
        t1 = time.perf_counter()
        x2 = x[: nchunks * WINDOW].reshape(nchunks, WINDOW)
        assert x2.flags["C_CONTIGUOUS"]
        P = f1(x2)

        x3 = x[STEP : STEP + nchunks2 * WINDOW].reshape(nchunks2, WINDOW)
        assert x3.flags["C_CONTIGUOUS"]
        P += f2(x3)

        t2 = time.perf_counter()
        if i > 0:
            tsum += t2 - t1
    print(f"FFTW_MANY: {tsum:.5f} {P[:4]} {nchunks=} {nchunks2=}")
    assert np.all(x == xref)

    tsum = 0.0
    nchunks = len(x) // WINDOW
    f1 = STFT_FFTW_MANY(nchunks, WINDOW)
    nchunks2 = (len(x) - STEP) // WINDOW
    f2 = STFT_FFTW_MANY(nchunks2, WINDOW)
    assert nchunks + nchunks2 == 32

    for i in range(ITERATIONS):
        t1 = time.perf_counter()
        x2 = x[: nchunks * WINDOW].reshape(nchunks, WINDOW)
        assert x2.flags["C_CONTIGUOUS"]
        P = f1(x2)

        x3 = x[STEP : STEP + nchunks2 * WINDOW].reshape(nchunks2, WINDOW)
        assert x3.flags["C_CONTIGUOUS"]
        P += f2(x3)

        t2 = time.perf_counter()
        if i > 0:
            tsum += t2 - t1
    print(f"FFTW_MANY_V2: {tsum:.5f} {P[:4]} {nchunks=} {nchunks2=}")
    assert np.all(x == xref)
