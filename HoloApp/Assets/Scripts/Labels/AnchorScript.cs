/*!
 * \author Dylan MIELOT
 * \date 13/08/2020
 */

using Microsoft.MixedReality.Toolkit.Experimental.Utilities;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AnchorScript : MonoBehaviour
{

    public WorldAnchorManager worldAnchorManager;

    /*!
     * \brief This script is no longer used. It create a world anchor to the gameobject attached.
     */
    void Start()
    {
        //AnchorIt();
    }

    //Create WorldAnchor to save label position
    public void AnchorIt()
    {
        worldAnchorManager.AttachAnchor(this.gameObject);
        this.gameObject.GetComponent<Renderer>().material.color = Color.red;
    }

    //Remove Anchor
    public void ReleaseAnchor()
    {
        worldAnchorManager.RemoveAnchor(this.gameObject);
        this.gameObject.GetComponent<Renderer>().material.color = Color.green;
    }
}
