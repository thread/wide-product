import numpy
import scipy.sparse

from . import _wide


def wide_product(a, b):
    a = scipy.sparse.csr_matrix(a).astype('double')
    b = scipy.sparse.csr_matrix(b).astype('double')

    if a.shape[0] != b.shape[0]:
        raise ValueError("Matrices have different numbers of rows")

    height = a.shape[0]

    assert height + 1 == len(a.indptr)
    assert height + 1 == len(b.indptr)

    assert a.indices.dtype == 'int32'
    assert a.indptr.dtype == 'int32'
    assert b.indices.dtype == 'int32'
    assert b.indptr.dtype == 'int32'

    nnzsize = _wide.lib.wide_product_max_nnz(
        _wide.ffi.cast('wp_index*', a.indptr.ctypes.data),
        _wide.ffi.cast('wp_index*', b.indptr.ctypes.data),
        height,
    )

    indptr = numpy.zeros(height + 1, dtype='int32')
    indices = numpy.zeros(nnzsize, dtype='int32')
    data = numpy.zeros(nnzsize, dtype='double')

    actual_nnz = _wide.lib.wide_product(
        height,
        _wide.ffi.cast('wp_number*', a.data.ctypes.data),
        _wide.ffi.cast('wp_index*', a.indices.ctypes.data),
        _wide.ffi.cast('wp_index*', a.indptr.ctypes.data),
        a.shape[1],
        len(a.data),
        _wide.ffi.cast('wp_number*', b.data.ctypes.data),
        _wide.ffi.cast('wp_index*', b.indices.ctypes.data),
        _wide.ffi.cast('wp_index*', b.indptr.ctypes.data),
        b.shape[1],
        len(b.data),
        _wide.ffi.cast('wp_number*', data.ctypes.data),
        _wide.ffi.cast('wp_index*', indices.ctypes.data),
        _wide.ffi.cast('wp_index*', indptr.ctypes.data),
    )

    indices.resize(actual_nnz)
    data.resize(actual_nnz)

    return scipy.sparse.csr_matrix(
        (data, indices, indptr),
        (height, a.shape[1] * b.shape[1]),
    )
