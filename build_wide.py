import cffi
import os.path

source_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'wide_product',
)

ffibuilder = cffi.FFI()

ffibuilder.set_source(
    'wide_product._wide',
    r"""
    #include "wide.c"
    """,
    extra_compile_args=[
        '-Werror',
        '-fno-unwind-tables',
        '-fomit-frame-pointer',
    ],
    include_dirs=[source_path],
)

ffibuilder.cdef(
    r"""
    typedef uint32_t wp_index;
    typedef double wp_number;

    wp_index wide_product(
        wp_index height,
        const wp_number* a_data,
        const wp_index* a_indices,
        const wp_index* a_indptr,
        wp_index a_width,
        wp_index a_nnz,
        const wp_number* b_data,
        const wp_index* b_indices,
        const wp_index* b_indptr,
        wp_index b_width,
        wp_index b_nnz,
        wp_number* out_data,
        wp_index* out_indices,
        wp_index* out_indptr
    );

    wp_index wide_product_max_nnz(
        const wp_index* a_indptr,
        const wp_index* b_indptr,
        wp_index height
    );
    """,
)

if __name__ == '__main__':
    ffibuilder.compile(verbose=True)
