import numpy as np

class SpectrumBuffer():

    def __init__(self, n_pixels, size = 1, ):
        
        self.n_pixels = n_pixels
        self.buffer = np.empty((n_pixels, size))
        self.buffer.fill(np.nan)

        self.iterator = 0

    def mean(self):
        return np.nanmean(self.buffer, 1)
    
    def resize(self, size):
        if size <= self.buffer.shape[1]:
            self.buffer = self.buffer[:, 0:size]
        else:
            arr_to_append = np.empty((self.n_pixels, size - self.buffer.shape[1]))
            arr_to_append.fill(np.nan)
            self.buffer = np.append(self.buffer, arr_to_append, axis=1)
            
        self._update_iterator()

    def append_spectrum(self, spectrum):
        self.buffer[:, self.iterator] = spectrum
        self._update_iterator()

    def _update_iterator(self):
        self.iterator += 1
        if self.iterator >= self.buffer.shape[1]:
            self.iterator = 0

