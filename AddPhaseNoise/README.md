# Add Phase Noise
Conversion of add phase noise Matlab script to python
<a href="https://www.mathworks.com/matlabcentral/fileexchange/8844-phase-noise?focused=5065243&tab=function">Matlab Script Source</a>

The phase noise is mixed with the carrier to produce sidebands around the carrier.

The generation process is as follows:
- Interpolate (in log-scale) SSB phase noise power spectrum in M equally spaced points (on the interval [0 Fs/2] including bounds).
- Calculate required frequency shape of the phase noise by X(m) = sqrt(P(m)*dF(m)) 
- Complement it by the symmetrical negative part of the spectrum.
- Generate AWGN of power 1 in the freq domain and multiply it sample-by-sample to the calculated shape 
- Perform  2*M-2 points IFFT to such generated noise