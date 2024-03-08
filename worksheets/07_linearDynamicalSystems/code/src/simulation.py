import numpy as np


def simulateLDS(N, A, Q, H, R, mu0, P0):
    M = A.shape[0]
    P = H.shape[0]
    # sample state noise
    w = np.random.multivariate_normal(np.zeros(M), Q, N).T
    # sample measurement noise
    v = np.random.multivariate_normal(np.zeros(P), R, N).T
    # sample initial state
    x0 = np.random.multivariate_normal(mu0, P0, 1).flatten()
    # sample states
    x = np.empty(shape=(M, N))
    y = np.empty(shape=(P, N))
    x[:, 0] = x0
    for n in range(1, N):
        x[:, n] = A @ x[:, n-1] + w[:, n]
    y = H @ x + v
    return x0, x, y
