import numba
import numpy as np
import pyfftw
from numba.np.arraymath import get_accumulator
from scipy import fft, signal

pyfftw.config.NUM_THREADS = 1

# @numba.vectorize([numba.float64(numbaCTYPE), numba.float32(numba.complex64)])
# def abs2(x):
#     return x.real ** 2 + x.imag ** 2

FTYPE = np.float32#'float32'
CTYPE = np.complex64#'complex64'


def cabs2(x):
    return x.real ** 2 + x.imag ** 2


@numba.jit(['float32[:](complex64[:,::1])', 'float64[:](complex128[:,::1])'], nopython=True, nogil=True,
           fastmath=True)
def cabs2_2d(x):
    r = x.real ** 2 + x.imag ** 2
    return r.sum(axis=0)


@numba.jit(['float32[:,:](float32[:,:])'], nopython=True, nogil=True, fastmath=True)
def demean_2d_f32(x):
    x2 = x - (x.sum(axis=1)[:, None] / x.shape[1])
    return x2.astype(FTYPE)


@numba.jit(['float32[:](float32[:])'], nopython=True, nogil=True, fastmath=True)
def demean_1d_f32(x: np.ndarray):
    # c = np.float32(0)
    # for v in np.nditer(x):
    #     c += v.item()
    # return x - c / x.size
    s = x.mean()
    x2 = x - s
    return x2.astype(FTYPE)



def stft_welch(x, window, step):
    fs = 352e6 / 1296
    # x -= x.mean()
    f, P = signal.welch(x, fs=fs, nperseg=window, noverlap=step,
                        return_onesided=True, window=np.ones(window), scaling='spectrum')
    return P


def stft_scipy_1d(x, window, step):
    n_steps = (len(x) - window) // step + 1
    P = np.zeros(window // 2 + 1, dtype=CTYPE)
    for i in range(n_steps):
        offset = i * step
        x_window = x[offset:offset + window]
        b = fft.rfft(x_window, workers=1)
        # np.multiply(s, np.conjugate(s), out=s)
        P += np.conjugate(b) * b
    return np.abs(P)


def stft_numpy_strided(x, window, step):
    result = np.lib.stride_tricks.sliding_window_view(x, window, axis=0)[::window - step].T
    # print(f'result: {result.ctypes.data} {result.shape} {result.strides}')
    result = np.fft.rfft(result, axis=0)
    # result = np.lib.stride_tricks.sliding_window_view(x, window, axis=0)[::window - step]
    # result = np.fft.fft(result, axis=1)
    result = cabs2(result)
    return result.sum(axis=1).astype(FTYPE)


def stft_numpy_strided_v2(x, window, step):
    result = np.lib.stride_tricks.sliding_window_view(x, window, axis=0)[::window - step].T
    P = pyfftw.zeros_aligned(window // 2 + 1, dtype='float64')
    # print(f'result: {result.ctypes.data} {result.shape} {result.strides}')
    for i in range(result.shape[1]):
        b = np.fft.rfft(result[:, i])
        P += cabs2(b)
    return P.astype(FTYPE)


def stft_fftw_1d(x, window: int, step: int):
    assert pyfftw.is_byte_aligned(x), f'x is not byte aligned: {x.ctypes.data} {pyfftw.simd_alignment}'
    n_steps = (len(x) - window) // step + 1
    a = pyfftw.empty_aligned(window, dtype=FTYPE)
    b = pyfftw.empty_aligned(window // 2 + 1, dtype=CTYPE)
    P = pyfftw.zeros_aligned(window // 2 + 1, dtype=FTYPE)
    fft_object = pyfftw.FFTW(a, b, threads=1, direction='FFTW_FORWARD', flags=('FFTW_PATIENT',))
    # print(f'x: {x.ctypes.data} {x.shape} {x.strides} {n_steps}')
    for i in range(n_steps):
        offset = i * step
        # a[:] = x[offset:offset + window]
        fft_object(x[offset:offset + window])
        P += cabs2(b)
    return P


def stft_fftw_1d_builder(x, window, step):
    assert pyfftw.is_byte_aligned(x)
    n_steps = (len(x) - window) // step + 1
    a = pyfftw.empty_aligned(window, dtype=FTYPE)
    P = pyfftw.zeros_aligned(window // 2 + 1, dtype=FTYPE)
    fft_object = pyfftw.builders.rfft(a, threads=1, planner_effort='FFTW_PATIENT', avoid_copy=True,
                                      overwrite_input=False)
    for i in range(n_steps):
        offset = i * step
        a[:] = x[offset:offset + window]
        b = fft_object(a)
        P += cabs2(b)
    return P


class STFT_FFTW:
    def __init__(self, window: int, step: int):
        self.window = window
        self.step = step
        self.Nfft = window // 2 + 1
        self.a = pyfftw.empty_aligned(window, dtype=FTYPE)
        self.b = pyfftw.empty_aligned(self.Nfft, dtype=CTYPE)
        self.fft_object = pyfftw.FFTW(self.a, self.b, direction='FFTW_FORWARD', flags=('FFTW_PATIENT',),
                                      threads=1)

    def __call__(self, x):
        assert pyfftw.is_byte_aligned(x)
        assert x.ndim == 1
        n_steps = (len(x) - self.window) // self.step + 1
        P = pyfftw.zeros_aligned(self.Nfft, dtype=FTYPE)
        for i in range(n_steps):
            offset = i * self.step
            # self.a[:] = x[offset:offset + self.window]
            xd = x[offset:offset + self.window]
            self.fft_object(demean_1d_f32(xd))
            # np.multiply(self.b, np.conjugate(self.b), out=self.b)
            P += cabs2(self.b)  # abs2(self.b)  # self.b
        return P


class STFT_FFTW_MANY:
    def __init__(self, n_channels, N):
        self.N = N
        self.n_channels = n_channels
        self.a = pyfftw.empty_aligned((n_channels, N), dtype=FTYPE)
        self.Nfft = N // 2 + 1
        self.b = pyfftw.empty_aligned((n_channels, self.Nfft), dtype=CTYPE)
        self.fft_object = fo = pyfftw.FFTW(self.a, self.b, axes=(1,), direction='FFTW_FORWARD', flags=('FFTW_PATIENT',),
                                           threads=1)
        # print(fo, fo.input_strides, fo.output_strides, fo.input_alignment, fo.output_alignment)

    def __call__(self, x):
        assert pyfftw.is_byte_aligned(x)
        assert x.ndim == 2
        n_channels, N = x.shape
        assert n_channels == self.n_channels
        assert N == self.N
        x = demean_2d_f32(x)
        self.fft_object(x)
        # s = cabs2(self.b).sum(axis=0)
        s = cabs2_2d(self.b)
        return s


class STFT_FFTW_MANY_V2:
    def __init__(self, n_channels, N):
        self.N = N
        self.n_channels = n_channels
        self.a = pyfftw.empty_aligned((n_channels, N), dtype=FTYPE)
        self.Nfft = N // 2 + 1
        self.b = pyfftw.empty_aligned((n_channels, self.Nfft), dtype=CTYPE)
        self.fft_object = fo = pyfftw.FFTW(self.a, self.b, axes=(1,), direction='FFTW_FORWARD',
                                           flags=('FFTW_PATIENT', 'FFTW_DESTROY_INPUT'),
                                           threads=1)
        # print(fo, fo.input_strides, fo.output_strides, fo.input_alignment, fo.output_alignment)

    def __call__(self, x):
        assert pyfftw.is_byte_aligned(x)
        assert x.ndim == 2
        n_channels, N = x.shape
        assert n_channels == self.n_channels
        assert N == self.N
        self.a[:] = x[:]
        self.fft_object(self.a)
        s = cabs2_2d(self.b)
        # s = cabs2(self.b).sum(axis=0)
        return s

# class STFT_FFTW_MANY_V2:
#     def __init__(self, n_channels, N):
#         self.N = N
#         self.n_channels = n_channels
#         self.a = pyfftw.empty_aligned((N, n_channels), dtype=FTYPE, n=32)
#         self.Nfft = N // 2 + 1
#         self.b = pyfftw.empty_aligned((self.Nfft, n_channels), dtype=CTYPE, n=32)
#         self.fft_object = fo = pyfftw.FFTW(self.a, self.b, axes=(0,), direction='FFTW_FORWARD', flags=('FFTW_PATIENT',),
#                                            threads=1)
#         # print(fo, fo.input_strides, fo.output_strides, fo.input_alignment, fo.output_alignment)
#
#     def __call__(self, x):
#         assert pyfftw.is_byte_aligned(x)
#         assert x.ndim == 2
#         n_channels, N = x.shape
#         assert n_channels == self.n_channels
#         assert N == self.N
#         #self.a[:] = x[:]
#         self.fft_object(x)
#         s = cabs2(self.b).sum(axis=1)
#         return s

# def stft_fftw_many(x: np.ndarray):
#     assert pyfftw.is_byte_aligned(x)
#     assert x.ndim == 2
#     n_channels, N = x.shape
#     Nfft = N // 2 + 1
#     a = pyfftw.empty_aligned((n_channels, N), dtype='float64')
#     b = pyfftw.empty_aligned((n_channels, Nfft), dtype=CTYPE')
#     # P = pyfftw.empty_aligned((n_channels, Nfft), dtype=CTYPE')
#
#     fft_object = pyfftw.FFTW(x, b, axes=(1,), direction='FFTW_FORWARD', flags=('FFTW_PATIENT',),
#                              threads=1)
#     a[:] = x[:]
#     fft_object()
#     np.multiply(b, np.conjugate(b), out=b)
#     s = np.abs(b).sum(axis=0)
#     return s
