import scipy.constants as const
import numpy as np

class Pulse:

    def __init__(self, grid_size = 4096, t_range = 1E-12):

        self.intialize_grids(grid_size, t_range)
        #self.central_frequency = self.convert_energy(1030E-9, "wavelength", "frequency")
        self.central_frequency = 0

    def add_gaussian_time(self, energy = 1, fwhm = 30E-15, delay = 0, norm = True):
        if norm:
            It = self.gaussian_norm(energy, fwhm/2.355, self.times)
        else:
            It = self.gaussian(energy, fwhm/2.355, self.times)

        self.Et = np.sqrt(It)
        self.Ef = np.fft.fftshift(np.fft.fft(self.Et))

    def gaussian(self, amp, sigma, xvals):
        return np.exp(np.multiply(-0.5, np.power(np.divide(xvals, sigma), 2)))
    
    def gaussian_norm(self, amp, sigma, xvals):
        return np.divide(1, sigma*np.sqrt(2*const.pi)) * self.gaussian(amp, sigma, xvals)

    def set_fwhm(self, val, units = "seconds"):
        self.fwhm = val
        
    def get_fwhm(self):
        return self.fwhm
    
    def set_sample_frequencies(self, wavelengths):
        self.sample_frequencies = np.divide(const.c, wavelengths*1E-9)

    def set_central_frequency(self, frequency):
        self.central_frequency = frequency

    def intialize_grids(self, grid_size, t_range):
        self.times = np.linspace(-0.5*t_range, 0.5*t_range, grid_size)
        self.dt = np.abs(self.times[1] - self.times[0])
        self.Et = np.empty(np.shape(self.times))
        self.frequencies = frequencies = np.fft.fftshift(np.fft.fftfreq(len(self.times), d=self.dt))
        self.Ef = np.empty(np.shape(self.frequencies))

    def from_spectrum(self, sample_frequency_Is):
        I_frequencies = np.interp(self.frequencies, np.flip(self.sample_frequencies - self.central_frequency), np.flip(sample_frequency_Is))
        self.Ef = np.sqrt(I_frequencies - np.min(I_frequencies))
        self.Et = np.fft.fftshift(np.fft.ifft(self.Ef))
        self.It = np.power(np.abs(self.Et), 2)

    def convert_energy(self, value, input_unit, output_unit):
        match input_unit:
            case "frequency":
                pass
            case "angular frequency":
                value = np.divide(value , 2*const.pi)
            case "wavelength":
                value = np.divide(const.c , value)
            case "electronVolts":
                value = np.divide(value, 4.135667696E-15)
            case _:
                raise ValueError("Invalid Unit")

        match output_unit:
            case "frequency":
                return value
            case "angular frequency":
                return np.multiply(value, 2*const.pi)
            case "wavelength":
                return np.multiply(value, const.c)
            case "electronVolts":
                return np.multiply(value, 4.135667696E-15)