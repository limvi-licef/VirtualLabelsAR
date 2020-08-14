
/*!
 * \author Dylan MIELOT
 * \date 14/08/2020
 */

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SocialPlatforms;

public class GetCameraPosition : MonoBehaviour
{
    float timeLeft = 1.0f;
    private Camera cam;

    private void Start()
    {
        cam = Camera.main;
    }

    //#############################################################################
    //#############################################################################
    //Save Camera position to file (world and local position)
    void Update()
    {
        timeLeft -= Time.deltaTime;

        if (timeLeft <= 0.0f)
        {
            Vector3 localCamPos = cam.transform.position;
            Vector3 worldCamPos = TransformPoint.InverseTransformPointUnscaled(transform, localCamPos);

            FileModifier.Save("CamPosition/CamLocalPosition.txt", localCamPos.ToString());
            FileModifier.Save("CamPosition/CamWorldPosition.txt", worldCamPos.ToString());
            timeLeft = 1.0f;
        }
    }
}
