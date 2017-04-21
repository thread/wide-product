wide-product
============

`wide-product` implements a partial, column-wise Khatri-Rao product. It is fast,
and works on sparse matrices.

It can be useful for engineering of cross-features for machine learning.

Definition
----------

For a pair of scalars (~ one by one matrices), the wide product is
multiplication:

.. code:: python

  wide_product ( [[a]], [[b]] ) == [[a * b]]

Where matrices are constructed by *vertical stacking*, the product is row-wise:

.. code:: python

    wide_product ( vstack((A, B)), vstack((C, D)) ) ==
        vstack((wide_product(A, C),
                wide_product(B, D)))

Where matrices are constructed by *horizontal stacking*, the product contains
all the products of the subcomponents up to permutation of columns:

.. code:: python

    wide_product ( hstack((A, B)), hstack((C, D)) ) ==
        hstack((wide_product(A, C),
                wide_product(A, D),
                wide_product(B, C),
                wide_product(B, D)))

Installation
------------

.. code:: bash

  pip install wide-product

Development
-----------

To build the module:

.. code:: bash

  python setup.py build

To test:

.. code:: bash

  PYTHONPATH=$(echo build/lib*):. py.test

To install:

.. code:: bash

  pip install .
