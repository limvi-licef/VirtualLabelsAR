
/*! 
 *  \author Dylan Mielot
 *  \date 12/08/2020
 */

using Microsoft.MixedReality.Toolkit.Experimental.Utilities;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AnchorWo : MonoBehaviour
{
    public WorldAnchorManager worldAnchorManager;
    private bool isDefine = false;

    // Create the WorldOrigin when the Hololens start the first time
    void Start()
    {
        if(!isDefine)
        {
            gameObject.transform.position = new Vector3(0, 0, 0);
            gameObject.transform.rotation = Camera.main.transform.rotation;
            worldAnchorManager.AttachAnchor(this.gameObject);
            gameObject.GetComponent<Renderer>().material.color = Color.red;
            isDefine = true;
        }
    }
}
