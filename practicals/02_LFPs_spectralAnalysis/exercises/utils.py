import numpy as np

def wittakerShannonInterpolator(t, ys, fs):
    Ns = len(ys)
    z = 0
    for i in range(-int((Ns-1)/2), int((Ns-1)/2), 1):
        n = int(i + (Ns-1)/2 + 1)
        z += ys[n]*np.sin(np.pi*fs*(t - i/fs))/(np.pi*fs*(t - i/fs))
    return z
