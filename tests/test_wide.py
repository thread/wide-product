import hypothesis
import hypothesis.strategies

import numpy
import scipy.sparse

from wide_product import wide_product


FINITE_FLOAT = hypothesis.strategies.floats(
    allow_nan=False,
    allow_infinity=False,
)

DIMENSION = hypothesis.strategies.integers(
    min_value=1,
    max_value=2**30,
)

SENSIBLE_DIMENSION = hypothesis.strategies.integers(
    min_value=1,
    max_value=1000,
)


def get_sparse_matrix(shape, data):
    rows, cols = shape

    element_data = numpy.array(data.draw(hypothesis.strategies.lists(
        FINITE_FLOAT,
        min_size=0,
        max_size=rows * cols,
    )))

    if len(element_data) == 0:
        return scipy.sparse.csr_matrix(shape)

    locations = numpy.array(data.draw(hypothesis.strategies.lists(
        hypothesis.strategies.tuples(
            hypothesis.strategies.integers(0, rows - 1),
            hypothesis.strategies.integers(0, cols - 1),
        ),
        min_size=len(element_data),
        max_size=len(element_data),
        unique=True,
    )), dtype='int32')

    return scipy.sparse.coo_matrix(
        (element_data, (locations[:, 0], locations[:, 1])),
        shape=shape,
    ).tocsr()


@hypothesis.given(
    x=FINITE_FLOAT,
    y=FINITE_FLOAT,
)
def test_scalar_wide_product_equivalent_to_multiplication(x, y):
    product = wide_product([[x]], [[y]])
    assert product.shape == (1, 1)
    assert product[0, 0] == x * y


@hypothesis.given(
    a_width=DIMENSION,
    b_width=DIMENSION,
    height=SENSIBLE_DIMENSION,
)
def test_shapes_of_empty_sparse_matrices_are_correct(a_width, b_width, height):
    a = scipy.sparse.csr_matrix((height, a_width))
    b = scipy.sparse.csr_matrix((height, b_width))

    product = wide_product(a, b).tocsr()

    assert product.shape == (height, a_width * b_width)


@hypothesis.given(
    a_width=SENSIBLE_DIMENSION,
    b_width=SENSIBLE_DIMENSION,
    height_top=SENSIBLE_DIMENSION,
    height_bottom=SENSIBLE_DIMENSION,
    data=hypothesis.strategies.data(),
)
def test_horizontal_stacking(a_width, b_width, height_top, height_bottom, data):
    a_top = get_sparse_matrix((height_top, a_width), data)
    b_top = get_sparse_matrix((height_top, b_width), data)
    a_bottom = get_sparse_matrix((height_bottom, a_width), data)
    b_bottom = get_sparse_matrix((height_bottom, b_width), data)

    top_product = wide_product(a_top, b_top)
    bottom_product = wide_product(a_bottom, b_bottom)
    stacked_product = scipy.sparse.vstack((top_product, bottom_product))

    a = scipy.sparse.vstack((a_top, a_bottom))
    b = scipy.sparse.vstack((b_top, b_bottom))

    full_product = wide_product(a, b)

    x = (full_product != stacked_product).todense().ravel()

    assert not numpy.any(x)
