/* ANL:waggle-license */
/* This file is part of the Waggle Platform.  Please see the file
 * LICENSE.waggle.txt for the legal details of the copyright and software
 * license.  For more details on the Waggle project, visit:
 *          http://www.wa8.gl
 */
/* ANL:waggle-license */
/*
 * Grayscale Kernel
 * Input: Image w/ 8-bit 3-channel data
 * Output: Grayscale Image w/ 8-bit 1-channel data
 */

#pragma OPENCL EXTENSION cl_khr_fp64 : enable

__kernel void grayscale_kernel(__global uchar* in,
                               __global uchar* out,
                               const int rows,
                               const int cols)
{
    float value = 0;
    size_t col = get_global_id(0);
    size_t row = get_global_id(1);
    size_t in_pos = row*cols + col*4;
    size_t out_pos = row*cols + col;

    //Sum weighted BGR Channels to get grayscale value
    if(in_pos % 4 == 0)
    {
        value += (double)in[in_pos]*0.299;
        value += (double)in[in_pos + 1]*0.587;
        value += (double)in[in_pos + 2]*0.114;
    }

    out[out_pos] = (uchar)value;
}

