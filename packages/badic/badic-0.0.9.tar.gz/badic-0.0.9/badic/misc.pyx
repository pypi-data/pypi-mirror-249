# coding=utf8
"""
Miscellanious


AUTHORS:

- Paul Mercat (2013)- I2M AMU Aix-Marseille Universite - initial version

REFERENCES:

"""

# *****************************************************************************
#       Copyright (C) 2014 Paul Mercat <paul.mercat@univ-amu.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
# *****************************************************************************
from __future__ import division, print_function, absolute_import

from libc.stdlib cimport malloc, free

from cpython cimport bool as c_bool
from cysignals.signals cimport sig_on, sig_off, sig_check

cdef extern from "miscellanious.h":
    void CETn(double x, double *v, int nv, double tau, int niter, double **pr, int nd, double *res)

def iterate_CET (x, v, tau, V, niter=10000):
    r"""
     - x real -- starting angle

     - v list -- direction defining the CET

     - tau real -- tau

     - niter int (default: ``10000``) number of iterations
    """
    cdef double *xm = <double *>malloc(sizeof(double)*V.nrows())
    cdef double *l = <double *>malloc(sizeof(double)*len(v))
    cdef double **proj = <double **>malloc(sizeof(double*)*len(v))
    cdef int i,j
    #print("v={}".format(v))
    for i in range(len(v)):
        l[i] = v[i]
        proj[i] = <double *>malloc(sizeof(double)*V.nrows())
        for j in range(V.nrows()):
            proj[i][j] = V[j,i]
    CETn(x, l, len(v), tau, niter, proj, V.nrows(), xm)
    for i in range(len(v)):
        free(proj[i])
    free(proj)
    free(l)
    res = []
    for i in range(V.nrows()):
        res.append(xm[i])
    free(xm)
    return res
    
    
    
    
    
