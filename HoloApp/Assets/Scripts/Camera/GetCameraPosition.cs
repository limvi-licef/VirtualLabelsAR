
/*!
 * \author Dylan MIELOT
 * \date 14/08/2020
 */

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SocialPlatforms;


// THIS SCRIPT IS NO LONGER USED

public class GetCameraPosition : MonoBehaviour
{
    float timeLeft = 1.0f;
    private Camera cam;

    private void Start()
    {
        cam = Camera.main;
    }

    /*!
     * \brief Save camero position to file
     * 
     * Camera position in camera space is saved in CamLocalPosition.txt. Camera position in WorldOrigin space is saved in CamWorldPosition.txt.
     */
    void Update()
    {
        timeLeft -= Time.deltaTime;

        if (timeLeft <= 0.0f)
        {
            Vector3 localCamPos = cam.transform.position;
            Vector3 worldCamPos = TransformPoint.InverseTransformPointUnscaled(transform, localCamPos); //!< Transform point from Camera space to WorldOrigin space.

            //save coordinates
            FileModifier.Save("CamPosition/CamLocalPosition.txt", localCamPos.ToString());
            FileModifier.Save("CamPosition/CamWorldPosition.txt", worldCamPos.ToString());
            timeLeft = 1.0f;
        }
    }
}
