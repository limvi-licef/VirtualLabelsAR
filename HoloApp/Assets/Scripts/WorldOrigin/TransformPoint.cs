
/*!
 * \author Dylan MIELOT
 * \date 14/08/2020
 */

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public static class TransformPoint
{
    //######################################################################################################
    //######################################################################################################
    //transform local coordinates to world coordinates (WorldOrigin gameObject to Camera)
    public static Vector3 TransformPointUnscaled(this Transform transform, Vector3 position)
    {
        var localToWorldMatrix = Matrix4x4.TRS(transform.position, transform.rotation, Vector3.one);
        return localToWorldMatrix.MultiplyPoint3x4(position);
    }

    //######################################################################################################
    //######################################################################################################
    //transform world coordinates to local coordinates (Camera to WorldOrigin gameObject)
    public static Vector3 InverseTransformPointUnscaled(this Transform transform, Vector3 position)
    {
        var worldToLocalMatrix = Matrix4x4.TRS(transform.position, transform.rotation, Vector3.one).inverse;
        return worldToLocalMatrix.MultiplyPoint3x4(position);
    }
}