#include <stdint.h>

typedef double wp_number;
typedef uint32_t wp_index;

static wp_index wide_product_row(
    const wp_number* restrict a_data,
    const wp_index* restrict a_indices,
    wp_index a_width,
    wp_index a_nnz,
    const wp_number* restrict b_data,
    const wp_index* restrict b_indices,
    wp_index b_width,
    wp_index b_nnz,
    wp_number* restrict out_data,
    wp_index* restrict out_indices
) {
    wp_number* start_out_data = out_data;

    for (wp_index i = 0; i < a_nnz; ++i) {
        for (wp_index j = 0; j < b_nnz; ++j) {
            wp_index out_index = a_indices[i]*b_width + b_indices[j];
            *out_data++ = a_data[i] * b_data[j];
            *out_indices++ = out_index;
        }
    }

    return out_data - start_out_data;
}

wp_index wide_product(
    wp_index height,
    const wp_number* restrict a_data,
    const wp_index* restrict a_indices,
    const wp_index* restrict a_indptr,
    wp_index a_width,
    wp_index a_nnz,
    const wp_number* restrict b_data,
    const wp_index* restrict b_indices,
    const wp_index* restrict b_indptr,
    wp_index b_width,
    wp_index b_nnz,
    wp_number* restrict out_data,
    wp_index* restrict out_indices,
    wp_index* restrict out_indptr
) {
    wp_index off = 0;
    for (wp_index x = 0; x < height; ++x) {
        *out_indptr++ = off;

        off += wide_product_row(
            a_data + a_indptr[x],
            a_indices + a_indptr[x],
            a_width,
            a_indptr[x + 1] - a_indptr[x],
            b_data + b_indptr[x],
            b_indices + b_indptr[x],
            b_width,
            b_indptr[x + 1] - b_indptr[x],
            out_data + off,
            out_indices + off
        );
    }
    *out_indptr = off;
    return off;
}

wp_index wide_product_max_nnz(
    const wp_index* restrict a_indptr,
    const wp_index* restrict b_indptr,
    wp_index height
) {
    wp_index max_nnz = 0;
    for (wp_index i = 0; i < height; ++i) {
        wp_index nnz_a = a_indptr[i + 1] - a_indptr[i];
        wp_index nnz_b = b_indptr[i + 1] - b_indptr[i];
        max_nnz += nnz_a * nnz_b;
    }
    return max_nnz;
}
