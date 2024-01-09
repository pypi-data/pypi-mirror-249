#  -*- coding: utf-8 -*-
"""
Author: Rafael R. L. Benevides
"""


# ---------- ---------- ---------- ---------- ---------- ---------- py
import numpy

from scipy.special.cython_special import spherical_jn, spherical_yn

# ---------- ---------- ---------- ---------- ---------- ---------- cy
cimport numpy as numpyc

from numpy cimport ndarray

# ---------- ---------- ---------- ---------- ---------- ---------- ty


cpdef double complex hl1(int l, double u):
    r"""
    Calculates the :math:`\ell`-degree spherical hankel function of the first 
    kind.
    
    Parameters
    ----------
    l : int
        degree. Must be greater than zero.
        
    u : double
        argument.
        
    Returns
    -------
    out : complex
    
    See also
    --------
    :func:`hl1_derivative`
    :func:`hl2`
    :func:`hl2_derivative`

    """
    return spherical_jn(l, u) + 1j*spherical_yn(l, u)


cpdef double complex hl1_derivative(int l, double u):
    r"""
    Calculates the derivative of the :math:`\ell`-degree spherical hankel 
    function of the first kind.
    
    Parameters
    ----------
    l : int
        degree. Must be greater than zero.
        
    u : double
        argument.
        
    Returns
    -------
    out : complex
    
    See also
    --------
    :func:`hl1`
    :func:`hl2`
    :func:`hl2_derivative`

    """
    return spherical_jn(l, u, True) + 1j*spherical_yn(l, u, True)


cpdef double complex hl2(int l, double u):
    r"""
    Calculates the :math:`\ell`-degree spherical hankel function of the 
    second kind.
    
    Parameters
    ----------
    l : int
        degree. Must be greater than zero.
        
    u : double
        argument.
        
    Returns
    -------
    out : complex
    
    See also
    --------
    :func:`hl1`
    :func:`hl1_derivative`
    :func:`hl2_derivative`

    """
    return spherical_jn(l, u) - 1j*spherical_yn(l, u)


cpdef double complex hl2_derivative(int l, double u):
    r"""
    Calculates the derivative of the :math:`\ell`-degree spherical hankel
    function of the second kind.
    
    Parameters
    ----------
    l : int
        degree. Must be greater than zero.
        
    u : double
        argument.
        
    Returns
    -------
    out : complex
    
    See also
    --------
    :func:`hl1`
    :func:`hl1_derivative`
    :func:`hl2`

    """
    return spherical_jn(l, u, True) - 1j*spherical_yn(l, u, True)
