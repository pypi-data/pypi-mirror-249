#  -*- coding: utf-8 -*-
"""
Author: Rafael R. L. Benevides
"""

# ---------- ---------- ---------- ---------- ---------- ---------- py
import numpy

from scipy.special.cython_special import sph_harm

# ---------- ---------- ---------- ---------- ---------- ---------- cy
cimport numpy as numpyc

from numpy cimport ndarray

from libc.math cimport sin, cos, sqrt, pi
from libc.stdlib cimport abs


# ---------- ---------- ---------- ---------- ---------- ---------- ty


cpdef double complex Ylm(int l, int m, double theta, double phi):
    r"""
    Calculates the spherical harmonic :math:`Y_{\ell}^m\left(\theta,
    \phi\right)`.
    
    .. math::
        Y_{\ell}^{m}\left( \theta, \phi \right)
        =
        \sqrt{
            \frac{2\ell + 1}{4\pi}
            \frac{
                \left( \ell - m \right)!
            }{
                \left( \ell + m \right)!
            }
        }
        P_{\ell}^{m}\left( \cos\theta \right)
        e^{jm\phi}
    
    Parameters
    ----------
    l : int
        degree. Must be greater than zero.

    m: int
        order.

    theta: double
        polar angle in radians

    phi: double
        azimuthal angle in radians

    Returns
    -------
    out : complex
        The :math:`\ell`-degree :math:`m`-order spherical harmonic 
        :math:`Y_{\ell}^m\left(\theta, \phi\right)`
    
    See also
    --------
    :func:`m_times_Ylm_over_sin_theta`
    :func:`dYlm_dtheta`
    
    """

    if abs(m) > l:
        return 0.0 + 0.0j

    return sph_harm(m, l, phi, theta)


cpdef double complex m_times_Ylm_over_sin_theta(int l, int m, double theta,  double phi):
    r"""
    Calculates :math:`\dfrac{mY_{\ell}^m\left(\theta,
    \phi\right)}{\sin\theta}`.
    
    Parameters
    ----------
    l : int
        degree. Must be greater than zero.

    m: int
        order.

    theta: double
        polar angle in radians

    phi: double
        azimuthal angle in radians

    Returns
    -------
    out : complex
        The :math:`\ell`-degree :math:`m`-order first spherical eigenfunction
        :math:`\dfrac{mY_{\ell}^m\left(\theta, \phi\right)}{\sin\theta}`

    See also
    --------
    :func:`dYlm_dtheta`
    :func:`Ylm`

    """
    cdef:
        double complex coeff


    if theta == 0.0:

        if abs(m) != 1:
            return 0j

        coeff = -1.0 / 4.0 * sqrt((2.0*l + 1.0) / pi * l * (l + 1.0))

        return coeff * numpy.exp(1j*m*phi)

    if theta == pi:

        if abs(m) != 1:
            return 0j

        coeff = 1.0 / 4.0 * sqrt((2.0*l + 1.0) / pi * l * (l + 1.0)) * (-1)**l

        return coeff * numpy.exp(1j*m*phi)

    return Ylm(l, m, theta, phi) / sin(theta) * m


cpdef double complex dYlm_dtheta(int l, int m, double theta,  double phi):
    r"""
    Calculates
    :math:`\dfrac{\partial Y_{\ell}^m}{\partial\theta}\left(\theta,\phi\right)`.
    
    Parameters
    ----------
    l : int
        degree. Must be greater than zero.

    m: int
        order.

    theta: double
        polar angle in radians

    phi: double
        azimuthal angle in radians

    Returns
    -------
    out : complex
        The :math:`\ell`-degree :math:`m`-order second spherical eigenfunction
        :math:`\dfrac{\partial Y_{\ell}^m}{\partial\theta}\left(\theta,\phi\right)`

    See also
    --------
    :func:`m_times_Ylm_over_sin_theta`
    :func:`Ylm`

    """
    cdef:
        double sin_theta, cos_theta

        double complex coeff, numerator


    if theta == 0.0:

        if abs(m) != 1:
            return 0j

        coeff = -m / 4.0 * sqrt((2.0 * l + 1.0) / pi * l * (l + 1.0))

        return coeff * numpy.exp(1j * m * phi)

    if theta == pi:

        if abs(m) != 1:
            return 0j

        coeff = -m / 4.0 * sqrt((2.0 * l + 1.0) / pi * l * (l + 1.0)) * (
            -1) ** l

        return coeff * numpy.exp(1j * m * phi)

    sin_theta = sin(theta)
    cos_theta = cos(theta)

    coeff = sqrt((2.0 * l + 1.0) / (2.0 * l - 1.0) * (l - m) * (l + m))

    numerator = l * cos_theta * Ylm(l, m, theta, phi) - coeff * Ylm(l - 1, m, theta, phi)

    return numerator / sin_theta
