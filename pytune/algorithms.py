
import pyaudio
from numpy import argmax, log, mean, diff, copy, arange , nonzero, int16
from numpy.fft import rfft
from scipy.signal import fftconvolve, kaiser, decimate


def parabolic(f, x):
    """Quadratic interpolation for estimating the true position of an
    inter-sample maximum when nearby samples are known.
    
    f is a vector and x is an index for that vector.
    
    Returns (vx, vy), the coordinates of the vertex of a parabola that goes
    through point x and its two neighbors.
    
    Example:
    Defining a vector f with a local maximum at index 3 (= 6), find local
    maximum if points 2, 3, and 4 actually defined a parabola.
    
    In [3]: f = [2, 3, 1, 6, 4, 2, 3, 1]
    
    In [4]: parabolic(f, argmax(f))
    Out[4]: (3.2142857142857144, 6.1607142857142856)
    
    """
    try:
        xv = 1/2. * (f[x-1] - f[x+1]) / (f[x-1] - 2 * f[x] + f[x+1]) + x
        yv = f[x] - 1/4. * (f[x-1] - f[x+1]) * (xv - x)
    except IndexError as ex:
        # TODO: handle or remove try/catch
        print(40 * '#', ex)

    return xv, yv


def freq_from_autocorr(signal, fs):
    """Estimate frequency using autocorrelation
    
    Pros: Best method for finding the true fundamental of any repeating wave, 
    even with strong harmonics or completely missing fundamental
    
    Cons: Not as accurate, doesn't work for inharmonic things like musical 
    instruments, this implementation has trouble with finding the true peak
    
    """
    # Remove DC offset
    signal -= mean(signal, dtype=int16)

    # Calculate autocorrelation (same thing as convolution, but with one input
    # reversed in time), and throw away the negative lags
    corr = fftconvolve(signal, signal[::-1], mode='full')
    corr = corr[len(corr)//2:]
    
    # Find the first low point
    d = diff(corr)
    start = nonzero(d > 0)[0][0]
    
    # Find the next peak after the low point (other than 0 lag).  This bit is 
    # not reliable for long signals, due to the desired peak occurring between 
    # samples, and other peaks appearing higher.
    i_peak = argmax(corr[start:-1]) + start
    i_interp = parabolic(corr, i_peak)[0]
    
    return fs / i_interp


def freq_from_fft(signal, fs):
    """Estimate frequency from peak of FFT
    
    Pros: Accurate, usually even more so than zero crossing counter 
    (1000.000004 Hz for 1000 Hz, for instance).  Due to parabolic 
    interpolation being a very good fit for windowed log FFT peaks?
    https://ccrma.stanford.edu/~jos/sasp/Quadratic_Interpolation_Spectral_Peaks.html
    Accuracy also increases with signal length
    
    Cons: Doesn't find the right value if harmonics are stronger than
    fundamental, which is common.
    
    """
    N = len(signal)
    
    # Compute Fourier transform of windowed signal
    windowed = signal * kaiser(N, 100)
    f = rfft(windowed)
    # Find the peak and interpolate to get a more accurate peak
    i_peak = argmax(abs(f)) # Just use this value for less-accurate result
    i_interp = parabolic(log(abs(f)), i_peak)[0]
    
    # Convert to equivalent frequency
    return fs * i_interp / N # Hz


def freq_from_crossings(signal, fs):
    """Estimate frequency by counting zero crossings
    
    Pros: Fast, accurate (increasing with signal length).  Works well for long 
    low-noise sines, square, triangle, etc.
    
    Cons: Doesn't work if there are multiple zero crossings per cycle, 
    low-frequency baseline shift, noise, etc.
    
    """
    # Find all indices right before a rising-edge zero crossing
    indices = nonzero((signal[1:] >= 0) & (signal[:-1] < 0))[0]
    
    # Naive (Measures 1000.185 Hz for 1000 Hz, for instance)
    #crossings = indices
    
    # More accurate, using linear interpolation to find intersample
    # zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
    crossings = [i - signal[i] / (signal[i+1] - signal[i]) for i in indices]
    
    # Some other interpolation based on neighboring points might be better. Spline, cubic, whatever
    
    return fs / mean(diff(crossings))


def freq_from_hps(signal, fs):
    """Estimate frequency using harmonic product spectrum
    
    Low frequency noise piles up and overwhelms the desired peaks
    """
    N = len(signal)
    signal -= mean(signal) # Remove DC offset
    
    # Compute Fourier transform of windowed signal
    windowed = signal * kaiser(N, 100)
    
    # Get spectrum
    X = log(abs(rfft(windowed)))
    
    # Downsample sum logs of spectra instead of multiplying
    hps = copy(X)
    for h in arange(2, 9): # TODO: choose a smarter upper limit
        dec = decimate(X, h)
        hps[:len(dec)] += dec
    
    # Find the peak and interpolate to get a more accurate peak
    i_peak = argmax(hps[:len(dec)])
    i_interp = parabolic(hps, i_peak)[0]
    
    # Convert to equivalent frequency
    return fs * i_interp / N # Hz


