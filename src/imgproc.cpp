// C++ headers
#include "opencv2/core.hpp"
#include "opencv2/imgproc.hpp"
#include "convert.h"
#include "numpy.h"

// C headers
extern "C" {
#include "imgproc.h"
#include "ulab/code/ndarray.h"
} // extern "C"

using namespace cv;

mp_obj_t cv2_imgproc_cvtColor(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    // Define the arguments
    enum { ARG_src, ARG_code, ARG_dst };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_src, MP_ARG_REQUIRED | MP_ARG_OBJ, { .u_obj = MP_OBJ_NULL } },
        { MP_QSTR_code, MP_ARG_REQUIRED | MP_ARG_INT, { .u_int = 0 } },
        { MP_QSTR_dst, MP_ARG_OBJ, { .u_obj = mp_const_none } },
    };

    // Parse the arguments
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    // Convert arguments to required types
    Mat src = mp_obj_to_mat(args[ARG_src].u_obj);
    int code = args[ARG_code].u_int;
    Mat dst = mp_obj_to_mat(args[ARG_dst].u_obj);

    // Call the corresponding OpenCV function
    try {
        cvtColor(src, dst, code);
    } catch(Exception& e) {
        mp_raise_msg(&mp_type_Exception, MP_ERROR_TEXT(e.what()));
    }

    // Return the result
    return mat_to_mp_obj(dst);
}
