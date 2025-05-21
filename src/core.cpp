// C++ headers
#include "opencv2/core.hpp"
#include "convert.h"
#include "numpy.h"

// C headers
extern "C" {
#include "core.h"
#include "ulab/code/ndarray.h"
} // extern "C"

using namespace cv;

mp_obj_t cv2_core_inRange(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    // Define the arguments
    enum { ARG_src, ARG_lower, ARG_upper, ARG_dst };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_src, MP_ARG_REQUIRED | MP_ARG_OBJ, { .u_obj = MP_OBJ_NULL } },
        { MP_QSTR_lower, MP_ARG_REQUIRED | MP_ARG_OBJ, { .u_obj = MP_OBJ_NULL } },
        { MP_QSTR_upper, MP_ARG_REQUIRED | MP_ARG_OBJ, { .u_obj = MP_OBJ_NULL } },
        { MP_QSTR_dst, MP_ARG_OBJ, { .u_obj = mp_const_none } },
    };

    // Parse the arguments
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    // Convert arguments to required types
    Mat src = mp_obj_to_mat(args[ARG_src].u_obj);
    Mat lower = mp_obj_to_mat(args[ARG_lower].u_obj);
    Mat upper = mp_obj_to_mat(args[ARG_upper].u_obj);
    Mat dst = mp_obj_to_mat(args[ARG_dst].u_obj);

    // Call the corresponding OpenCV function
    try {
        inRange(src, lower, upper, dst);
    } catch(Exception& e) {
        mp_raise_msg(&mp_type_Exception, MP_ERROR_TEXT(e.what()));
    }

    // Return the result
    return mat_to_mp_obj(dst);
}

mp_obj_t cv2_core_max(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    // Define the arguments
    enum { ARG_src1, ARG_src2, ARG_dst };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_src1, MP_ARG_REQUIRED | MP_ARG_OBJ, { .u_obj = MP_OBJ_NULL } },
        { MP_QSTR_src2, MP_ARG_REQUIRED | MP_ARG_OBJ, { .u_obj = MP_OBJ_NULL } },
        { MP_QSTR_dst, MP_ARG_OBJ, { .u_obj = mp_const_none } },
    };

    // Parse the arguments
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    // Convert arguments to required types
    Mat src1 = mp_obj_to_mat(args[ARG_src1].u_obj);
    Mat src2 = mp_obj_to_mat(args[ARG_src2].u_obj);
    Mat dst = mp_obj_to_mat(args[ARG_dst].u_obj);

    // Call the corresponding OpenCV function
    try {
        max(src1, src2, dst);
    } catch(Exception& e) {
        mp_raise_msg(&mp_type_Exception, MP_ERROR_TEXT(e.what()));
    }
    
    // Return the result
    return mat_to_mp_obj(dst);
}

mp_obj_t cv2_core_min(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    // Define the arguments
    enum { ARG_src1, ARG_src2, ARG_dst };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_src1, MP_ARG_REQUIRED | MP_ARG_OBJ, { .u_obj = MP_OBJ_NULL } },
        { MP_QSTR_src2, MP_ARG_REQUIRED | MP_ARG_OBJ, { .u_obj = MP_OBJ_NULL } },
        { MP_QSTR_dst, MP_ARG_OBJ, { .u_obj = mp_const_none } },
    };

    // Parse the arguments
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    // Convert arguments to required types
    Mat src1 = mp_obj_to_mat(args[ARG_src1].u_obj);
    Mat src2 = mp_obj_to_mat(args[ARG_src2].u_obj);
    Mat dst = mp_obj_to_mat(args[ARG_dst].u_obj);

    // Call the corresponding OpenCV function
    try {
        min(src1, src2, dst);
    } catch(Exception& e) {
        mp_raise_msg(&mp_type_Exception, MP_ERROR_TEXT(e.what()));
    }

    // Return the result
    return mat_to_mp_obj(dst);
}
