
/*! 
 *  \author Dylan Mielot
 *  \date 12/08/2020
 */

using Microsoft.MixedReality.Toolkit;
using System.Collections;
using System.Collections.Generic;
using System.Reflection.Emit;
using UnityEngine;
using UnityEngine.UI;

public class Position : MonoBehaviour
{
    public TextMesh camWorldTxt; //!< TextMesh used to display informations
    public GameObject WorldOrigin;
    private Camera cam;

    /*!
     * \brief Allow to display informations in front of the camera
     */
    void Start()
    {
        WorldOrigin = GameObject.Find("WorldOrigin");
        cam = Camera.main;
    }

    // Update is called once per frame
    void Update()
    {
        //Transform Local to World coordinates(WorldOrigin)
        Vector3 worldPos = TransformPoint.InverseTransformPointUnscaled(WorldOrigin.transform, cam.transform.position);
        
        camWorldTxt.text = worldPos.ToString();
    }
}
