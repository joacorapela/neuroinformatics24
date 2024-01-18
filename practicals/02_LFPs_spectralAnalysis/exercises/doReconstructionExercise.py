import utils

# In this Python tutorial we start with a continuous function of time from
# which we draw samples at a uniform sampling rate.  The sampling rate is
# chosen to be higher than the maximum appreciable frequency component
# contained in the original function of time.  We then attempted to
# reconstruct the original continuous function from the sampled data.
import numpy as np
import matplotlib.pyplot as plt

def test_func(t, f0): 
    answer = np.sinc(f0 * t)**2
    return answer
f0 = 2.0
f_Nyquist = 2 * f0

# Here's the original function from which samples will be drawn.
ts0 = np.linspace(-2.5, 2.5, 1000)
func_values_ts0 = test_func(t=ts0, f0=f0)

# sample
Nyquist_factor = 1.0
# Nyquist_factor = 0.8

f_sample = f_Nyquist * Nyquist_factor
ts_sample = np.arange(-2.5, 2.5, 1/f_sample)
func_values_sample = test_func(t=ts_sample, f0=f0)

# Now make some time values and plot the reconstructed signal (black line)
# along with the origonal continuous function (yellow line).
tt = np.linspace(-2.5, 2.5, 1000)
plt.plot(tt, utils.wittakerShannonInterpolator(t=tt, ys=func_values_sample,
                                               fs=f_sample),
         'kx', linewidth=3, label="Reconstructed")
plt.plot(ts0, func_values_ts0, 'yo', linewidth = 2, label="Original")
plt.plot(ts_sample, func_values_sample, 'b*', label="Samples")
plt.legend()
plt.title(f"Nyquist factor {Nyquist_factor}")
plt.xlabel("t")
plt.ylabel("x(t)")

fig_filename_pattern = "figures/example_NiquistFactor{:.2f}.png"
plt.savefig(fig_filename_pattern.format(Nyquist_factor))
plt.show()

breakpoint()
