
/*!
 * \author Dylan MIELOT
 * \date 14/08/2020
 */

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public static class TransformPoint
{
    
    /*!
     * \brief transform local coordinates to Camera space coordinates.
     * 
     * \param transform Transform of the gameObject.
     * \param position Coordinates to transform.
     * 
     * \return Vector4 camera space coordinates
     */
    public static Vector3 TransformPointUnscaled(this Transform transform, Vector3 position)
    {
        var localToWorldMatrix = Matrix4x4.TRS(transform.position, transform.rotation, Vector3.one);
        return localToWorldMatrix.MultiplyPoint3x4(position);
    }

    /*!
     * \brief transform Camera space coordinates to local coordinates.
     * 
     * \param transform Transform of the gameObject.
     * \param position Coordinates to transform.
     * 
     * \return Vector4 local coordinates
     */
    public static Vector3 InverseTransformPointUnscaled(this Transform transform, Vector3 position)
    {
        var worldToLocalMatrix = Matrix4x4.TRS(transform.position, transform.rotation, Vector3.one).inverse;
        return worldToLocalMatrix.MultiplyPoint3x4(position);
    }
}