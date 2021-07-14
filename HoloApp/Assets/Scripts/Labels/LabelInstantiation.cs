

/*! 
 *  \author Dylan Mielot
 *  \date 12/08/2020
 */

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/*!
 * \brief Instantiate label
 * 
 * Instantiate a label using speechInputManager with "Create label" keyword.
 * 
 * TODO: use LabelManager to create a label and manage id conflict with labels added from Desktop App on server.
 */
public class LabelInstantiation : MonoBehaviour
{
    public GameObject label;
    public float distance = 1.0f;

    public void Label_Instantiation()
    {
        var cam = Camera.main;
        Instantiate(label, cam.transform.position + cam.transform.forward * distance, cam.transform.rotation);
    }
}

