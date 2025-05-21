// C++ headers
#include "opencv2/core.hpp"

// C headers
extern "C" {
#include "py/runtime.h"
#include "ulab/code/ndarray.h"
} // extern "C"

using namespace cv;

// Derived from:
// https://github.com/opencv/opencv/blob/aee828ac6ed3e45d7ca359d125349a570ca4e098/modules/python/src2/cv2_numpy.hpp#L7-L21
class NumpyAllocator : public MatAllocator
{
public:
    NumpyAllocator() { stdAllocator = Mat::getStdAllocator(); }
    ~NumpyAllocator() {}

    UMatData* allocate(ndarray_obj_t* o, int dims, const int* sizes, int type, size_t* step) const;
    UMatData* allocate(int dims0, const int* sizes, int type, void* data, size_t* step, AccessFlag flags, UMatUsageFlags usageFlags) const CV_OVERRIDE;
    bool allocate(UMatData* u, AccessFlag accessFlags, UMatUsageFlags usageFlags) const CV_OVERRIDE;
    void deallocate(UMatData* u) const CV_OVERRIDE;

    const MatAllocator* stdAllocator;
};

inline NumpyAllocator& GetNumpyAllocator() {static NumpyAllocator gNumpyAllocator;return gNumpyAllocator;}
