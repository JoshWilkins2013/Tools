import matplotlib.pyplot as plt
import numpy as np
import math
import sys


def add_phase_noise(Sin, Fs, phase_noise_freq, phase_noise_power, VALIDATION_ON=0):

    # Oscillator Phase Noise Model
    #  INPUT:
    #    Sin - input COMPLEX signal
    #    Fs  - sampling frequency ( in Hz ) of Sin
    #    phase_noise_freq  - frequencies at which SSB Phase Noise is defined (offset from carrier in Hz) - RowVector
    #    phase_noise_power - SSB Phase Noise power ( in dBc/Hz ) - RowVector
    #    VALIDATION_ON  - 1 - perform validation, 0 - don't perform validation
    #  OUTPUT:
    #    Sout - output COMPLEX phase noised signal

    if max(phase_noise_freq) >= Fs/2:
        raise ValueError('Maximal frequency offset should be less than Fs/2')
    if len(phase_noise_freq) != len(phase_noise_power):
        raise ValueError('phase_noise_freq and phase_noise_power should be the same length')

    # Add 0 dBc/Hz at DC
    if 0 not in phase_noise_freq:
        phase_noise_freq.append(0)
        phase_noise_power.append(0)

    # Calculate input length
    N = int(np.prod(np.shape(Sin)))

    # M is the frequency resolution
    if N % 2: # N Odd
         M = (N+1)/2 + 1
    else:     # N Even
         M = N/2 + 1

    # Equally spaced partitioning of the half spectrum
    F = np.linspace(0, Fs/2, M)  # Frequency Grid
    dF = [F[-1] - F[-2]] * M     # Delta F (Multiplied by M to create 1xM array)

    # Perform interpolation of phase_noise_power in log-scale
    logP = [0] * M
    intrvlNum = len(phase_noise_freq)
    phase_noise_freq.sort()
    phase_noise_power.sort(reverse=True)
    for i in range(0, intrvlNum):
        leftBound = phase_noise_freq[i]
        t1 = phase_noise_power[i]
        if i == intrvlNum-1: # If at end of list
            rightBound = Fs/2
            t2 = phase_noise_power[-1]
            inside = (list(F).index(x) for x in F if leftBound <= x <= rightBound)
        else:
            rightBound = phase_noise_freq[i+1]
            t2 = phase_noise_power[i+1]
            inside = (list(F).index(x) for x in F if leftBound <= x < rightBound)

        realmin = sys.float_info.epsilon

        for x in list(inside):
            logP[x] = t1 + (np.log10(F[x] + realmin) - np.log10(leftBound + realmin)) / (np.log10(rightBound + realmin) - np.log10(leftBound + realmin)) * (t2 - t1)

    P = 10**np.array((np.real(np.array(logP)) / 10))  # Interpolated P ( half spectrum [0 Fs/2] ) [ dBc/Hz ]

    if not VALIDATION_ON:
        awgn_P1 = (math.sqrt(0.5)*(np.random.randn(1, M) + 1j*np.random.randn(1, M)))[0]  # Creates random complex row vector, length M
    else:
        awgn_P1 = math.sqrt(0.5)*np.array(([1+1j]*M))
    
    # Shape the noise on the positive spectrum [0, Fs/2] including bounds ( M points )
    X = (2*M-2) * np.sqrt(dF * P) * awgn_P1
    Z = np.flipud(np.conj(X[1:-1]))
    X = list(X) + list(Z)

    X[0] = 0  # Remove DC

    # Perform IFFT
    x = np.fft.ifft(np.array(X))

    # Calculate phase noise
    phase_noise = np.exp(1j * np.real(x[0:N]))

    if VALIDATION_ON:
        labels = [ 'Input SSB phase noise power', 'Interpolated SSB phase noise power',
                   'Positive spectrum of the generated phase noise exp', 'Positive spectrum of the approximation ( 1+j*x )' ]
        plt.figure()
        plt.semilogx(phase_noise_freq[1:], phase_noise_power[1:], 'o-', label=labels[0])  # Input SSB phase noise power
        plt.semilogx(F[1:], 10*np.log10(P[1:]), 'r*-', label=labels[1])  # Interpolated SSB phase noise power

        X1 = np.fft.fft(phase_noise)
        plt.semilogx(F[1:], 10*np.log10((np.array((abs(X1[0:M])/max(abs(X1[0:M]))))**2) / dF[0])[1:], 'ks-', label=labels[2])  # generated phase noise exp(j*x)

        X2 = np.fft.fft(1 + 1j*np.real(x[0:N]))
        plt.semilogx(F[1:], 10*np.log10((np.array((abs(X2[0:M])/max(abs(X2[0:M]))))**2) / dF[0])[1:], 'm>-', label=labels[3])  # approximation ( 1+j*x )

        plt.grid(True)
        plt.xlabel('Frequency Exponent [10^x, Hz]')
        plt.ylabel('dBc/Hz')
        plt.legend(loc='upper right')
        plt.show()
        return F[1:], P[1:]  # Frequencies(F) at which the interpolated phase noise power (P) was generated
    else:
        phaseNoise = np.array(Sin) * np.array(np.reshape(phase_noise, np.shape(Sin)))
        return F[1:], P[1:], phaseNoise  # Frequencies(F) at which the interpolated phase noise power (P) and random phase noise (phaseNoise) were generated
