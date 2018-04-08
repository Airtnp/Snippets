# https://github.com/solivr/cython_opencvMat

import numpy as np
cimport numpy as np  # for np.ndarray
from libc.string cimport memcpy
from nparr_cvmat cimport *
from cpython cimport Py_INCREF


# inspired and adapted from http://makerwannabe.blogspot.ch/2013/09/calling-opencv-functions-via-cython.html

cdef Mat np2Mat3D(np.ndarray ary):
    assert ary.ndim==3 and ary.shape[2]==3, "ASSERT::3channel RGB only!!"
    ary = np.dstack((ary[...,2], ary[...,1], ary[...,0])) #RGB -> BGR

    cdef np.ndarray[np.uint8_t, ndim=3, mode ='c'] np_buff = np.ascontiguousarray(ary, dtype=np.uint8)
    cdef unsigned int* im_buff = <unsigned int*> np_buff.data
    cdef int r = ary.shape[0]
    cdef int c = ary.shape[1]
    cdef Mat m
    m.create(r, c, CV_8UC3)
    memcpy(m.data, im_buff, r*c*3)
    return m

cdef Mat np2Mat2D(np.ndarray ary):
    assert ary.ndim==2 , "ASSERT::1 channel grayscale only!!"

    cdef np.ndarray[np.uint8_t, ndim=2, mode ='c'] np_buff = np.ascontiguousarray(ary, dtype=np.uint8)
    cdef unsigned int* im_buff = <unsigned int*> np_buff.data
    cdef int r = ary.shape[0]
    cdef int c = ary.shape[1]
    cdef Mat m
    m.create(r, c, CV_8UC1)
    memcpy(m.data, im_buff, r*c)
    return m


cdef Mat np2Mat(np.ndarray ary):
    if ary.ndim == 2:
        return np2Mat2D(ary)
    elif ary.ndim == 3:
        return np2Mat3D(ary)


cdef object Mat2np(Mat m):
    # Create buffer to transfer data from m.data
    cdef Py_buffer buf_info
    # Define the size / len of data
    cdef size_t xlen = m.rows*m.cols*m.channels()*sizeof(CV_8UC3)
    # Fill buffer
    # PyBuffer_FillInfo(&buf_info, NULL, m.data, xlen, 1, PyBUF_FULL_RO)
    PyBuffer_FillInfo(&buf_info, NULL, m.data, xlen, 0, PyBUF_FULL_RO)
    # Get Pyobject from buffer data
    Pydata = PyMemoryView_FromBuffer(&buf_info)
    Py_INCREF(<object>Pydata)
    # Create ndarray with data
    shape_array = (m.rows, m.cols, m.channels())
    ary = np.ndarray(shape=shape_array, buffer=Pydata, order='c', dtype=np.uint8)

    # BGR -> RGB
    ary = np.dstack((ary[...,2], ary[...,1], ary[...,0]))
    # Convert to numpy array
    pyarr = np.asarray(ary)
    return pyarr


cdef class PyMat:
    cdef Mat mat

    def __cinit__(self, np_mat):
        self.mat = np2Mat(np_mat)

    def get_mat(self):
        return Mat2np(self.mat)