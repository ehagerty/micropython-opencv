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

// Fix for https://github.com/sparkfun/micropython-opencv/issues/13
// 
// TLDR; The CoreTLSData object gets allocated once, whenever the first OpenCV
// function that needs it happens to be called. That will only happen from the
// user's code, after the GC has been initialized, meaning it gets allocated on
// the GC heap (see `__wrap_malloc()`). If a soft reset occurs, the GC gets
// reset and overwrites the memory location, but the same memory location is
// still referenced for the CoreTLSData object, resulting in bogus values and
// subsequent `CV_Assert()` calls fail
// 
// The solution here is to create a global variable that subsequently calls
// `getCoreTlsData()` to allocate the CoreTLSData object before the GC has
// been initialized, so it gets allocated on the C heap and persists through
// soft resets. `getCoreTlsData()` is not publicly exposed, but `theRNG()` is
// exposed, which just runs `return getCoreTlsData().rng`
volatile RNG rng = theRNG();

mp_obj_t cv2_core_convertScaleAbs(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    // Define the arguments
    enum { ARG_src, ARG_dst, ARG_alpha, ARG_beta };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_src, MP_ARG_REQUIRED | MP_ARG_OBJ, { .u_obj = MP_OBJ_NULL } },
        { MP_QSTR_dst, MP_ARG_OBJ, { .u_obj = mp_const_none } },
        { MP_QSTR_alpha, MP_ARG_OBJ, { .u_obj = mp_const_none } },
        { MP_QSTR_beta, MP_ARG_OBJ, { .u_obj = mp_const_none } },
    };

    // Parse the arguments
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    // Convert arguments to required types
    Mat src = mp_obj_to_mat(args[ARG_src].u_obj);
    Mat dst = mp_obj_to_mat(args[ARG_dst].u_obj);
    mp_float_t alpha = args[ARG_alpha].u_obj == mp_const_none ? 1.0 : mp_obj_get_float(args[ARG_alpha].u_obj);
    mp_float_t beta = args[ARG_beta].u_obj == mp_const_none ? 0.0 : mp_obj_get_float(args[ARG_beta].u_obj);

    // Call the corresponding OpenCV function
    try {
        convertScaleAbs(src, dst, alpha, beta);
    } catch(Exception& e) {
        mp_raise_msg(&mp_type_Exception, MP_ERROR_TEXT(e.what()));
    }

    // Return the result
    return mat_to_mp_obj(dst);
}

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
