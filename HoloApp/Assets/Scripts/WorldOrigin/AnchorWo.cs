
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

    /*!
     * \brief Create a World Origin in (0,0,0), and anchor it.
     * 
     * When the app starts the first time, a World Origin is create in (0,0,0) with a world anchor. 
     */
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
