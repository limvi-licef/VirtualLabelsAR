
/*! 
 *  \author Dylan Mielot
 *  \date 12/08/2020
 */

using Microsoft.MixedReality.Toolkit;
using Microsoft.MixedReality.Toolkit.SpatialAwareness;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SpatialMappingManual : MonoBehaviour
{
    /*!
     * \brief Set spatial mapping visible using voice recognizer ("Mapping On" keyword)
     */
    public void SetVisible()
    {
        var observer = CoreServices.GetSpatialAwarenessSystemDataProvider<IMixedRealitySpatialAwarenessMeshObserver>();

        if (observer.DisplayOption != SpatialAwarenessMeshDisplayOptions.Visible)
        {
            observer.DisplayOption = SpatialAwarenessMeshDisplayOptions.Visible;
        }
    }

    /*!
     * \brief Set spatial mapping not visible using voice recognizer ("Mapping Off" keyword)
     */
    public void SetNotVisible()
    {
        var observer = CoreServices.GetSpatialAwarenessSystemDataProvider<IMixedRealitySpatialAwarenessMeshObserver>();

        if (observer.DisplayOption != SpatialAwarenessMeshDisplayOptions.None)
        {
            observer.DisplayOption = SpatialAwarenessMeshDisplayOptions.None;
        }
    }
}
