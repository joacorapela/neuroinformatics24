
import numpy as np


class OnlineKalmanFilter:
    """
    Class implementing the online Kalman filter algorithm for the following
    linear dynamical system:

    .. math::
       x_n &= A\ x_{n-1} + w_n,\ \\textrm{where}\ w_n\sim\mathcal{N}(w_n|0, Q)\, \\textrm{and}\ x_n\in\Re^M

       y_n &= H\ x_{n-1} + v_n,\ \\textrm{where}\ v_n\sim\mathcal{N}(v_n|0, R)\, \\textrm{and}\ y_n\in\Re^N

       x_0&\in\mathcal{N}(x_0|m_0, V_0)

    Example use:

    .. code-block:: python

        online_kf = OnlineKalmanFilter(A, Q, mu0, Q0, H, R)
        x_pred, P_pred = online_kf.predict()

        for y in ys:
            x_filt, P_filt = online_kf.update(y)
            x_pred, P_pred = online_kf.predict()

    Note 1:
        invocation so `predict()` and `update(y)` should alternate. That is,
        each invocation to `update(y)` should be preceded by an invocation to
        `predict()`, and each invocation to `predict()` (except the first one)
        should be preceded by an invoation to `update(y)`.

    Note 2:
        observations :math:`y_n` should be sampled uniformly.
    """
    def __init__(self, A, Q, mu0, Q0, H, R):
        self._A = A
        self._Q = Q
        self._mu0 = mu0
        self._Q0 = Q0
        self._H = H
        self._R = R

        self._x = mu0
        self._P = Q0

        M = len(mu0)
        self.I = np.eye(M)

    def predict(self):
        """Caclulates the predicted mean and covariance.

        :return: (mean, covariance): tuple containing the predicted mean vector and covariance matrix.

        """
        # When calling this method self.x contains the filtered mean at time
        # t-1 (i.e., \mu_{t-1|t-1}). This function needs to set self.x to the
        # predicted mean at time t (i.e., \mu_{t|t-1}). The same holds for the
        # filtered and predicted covariance, P_{t-1|t-1} and P_{t|t-1},
        # respectievly. See slide 25 from
        # https://github.com/joacorapela/neuroinformatics24/blob/master/lectures/07_linearDynamicalSystems/LDS_SWCNeuroinf2024.pdf

        self.x = ...
        self.P = ...
        return self.x, self.P

    def update(self, y):
        """Caclulates the filtered mean and covariance.

        :param y: observation :math:`\in\Re^M`
        :return: (state, covariance): tuple containing the filtered mean vector and covariance matrix.

        """
        # When calling this method self.x contains the predicted mean at time
        # t (i.e., \mu_{t|t-1}). This function needs to set self.x to the
        # filtered mean at time t (i.e., \mu_{t|t}). The same holds for the
        # predicted and filtered covariance, P_{t|t-1} and P_{t|t},
        # respectievly. See slide 25 from
        # https://github.com/joacorapela/neuroinformatics24/blob/master/lectures/07_linearDynamicalSystems/LDS_SWCNeuroinf2024.pdf

        if y.ndim == 1:
            y = np.expand_dims(y, axis=1)
        if not np.isnan(y).any():
            pred_obs = self.H @ self.x
            residual = y - pred_obs
            # S is the inverted term (...)^{-1} in the expression of K_t at
            # https://github.com/joacorapela/neuroinformatics24/blob/master/lectures/07_linearDynamicalSystems/LDS_SWCNeuroinf2024.pdf
            # We first compute a possibly non-simetric version of this term.
            Stmp = self.H @ self.P @ self.H.T + self.R
            # Next we enforce S to be symmetirc
            S = (Stmp + Stmp.T) / 2
            Sinv = np.linalg.inv(S)
            K = self.P @ self.H.T @ Sinv
            self.x = ...
            self.P = ...
        return self.x, self.P

    @property
    def A(self):
        return self._A

    @A.setter
    def A(self, A):
        self._A = A

    @property
    def Q(self):
        return self._Q

    @Q.setter
    def Q(self, Q):
        self._Q = Q

    @property
    def mu0(self):
        return self._mu0

    @mu0.setter
    def mu0(self, mu0):
        self._mu0 = mu0

    @property
    def Q0(self):
        return self._Q0

    @Q0.setter
    def Q0(self, Q0):
        self._Q0 = Q0

    @property
    def H(self):
        return self._H

    @H.setter
    def H(self, H):
        self._H = H

    @property
    def R(self):
        return self._R

    @R.setter
    def R(self, R):
        self._R = R

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def P(self):
        return self._P

    @P.setter
    def P(self, P):
        self._P = P
