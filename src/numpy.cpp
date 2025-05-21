// C++ headers
#include "numpy.h"
#include "convert.h"

// Derived from:
// https://github.com/opencv/opencv/blob/aee828ac6ed3e45d7ca359d125349a570ca4e098/modules/python/src2/cv2_numpy.cpp#L11-L22
UMatData* NumpyAllocator::allocate(ndarray_obj_t* ndarray, int dims, const int* sizes, int type, size_t* step) const
{
    UMatData* u = new UMatData(this);
    u->data = (uchar*) ndarray->array;
    u->origdata = (uchar*) ndarray->origin;
    for( int i = 0; i < dims - 1; i++ )
        step[i] = ndarray->strides[ULAB_MAX_DIMS - ndarray->ndim + i];
    step[dims-1] = CV_ELEM_SIZE(type);
    u->size = sizes[0]*step[0];
    u->userdata = ndarray;
    return u;
}

UMatData* NumpyAllocator::allocate(int dims0, const int* sizes, int type, void* data, size_t* step, AccessFlag flags, UMatUsageFlags usageFlags) const
{
    if( data != 0 )
    {
        return stdAllocator->allocate(dims0, sizes, type, data, step, flags, usageFlags);
    }

    int depth = CV_MAT_DEPTH(type);
    int cn = CV_MAT_CN(type);
    int typenum = mat_depth_to_ndarray_type(depth);
    int i, dims = dims0;
    size_t _sizes[ULAB_MAX_DIMS];
    if( cn > 1 )
    {
        _sizes[ULAB_MAX_DIMS - 1] = cn;
        dims++;
    }
    for( i = 0; i < dims0; i++ )
        _sizes[ULAB_MAX_DIMS - dims + i] = sizes[i];
    ndarray_obj_t* ndarray = ndarray_new_dense_ndarray(dims, _sizes, typenum);
    return allocate(ndarray, dims0, sizes, type, step);
}

bool NumpyAllocator::allocate(UMatData* u, AccessFlag accessFlags, UMatUsageFlags usageFlags) const
{
    return stdAllocator->allocate(u, accessFlags, usageFlags);
}

void NumpyAllocator::deallocate(UMatData* u) const
{
    if(!u)
        return;
    CV_Assert(u->urefcount >= 0);
    CV_Assert(u->refcount >= 0);
    if(u->refcount == 0)
    {
        delete u;
    }
}
