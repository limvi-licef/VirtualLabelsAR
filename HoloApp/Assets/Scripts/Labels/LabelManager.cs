using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Newtonsoft.Json.Linq;

/// <summary>
/// Singleton that manages the label in the scene
/// </summary>
public class LabelManager : MonoBehaviour
{
    [SerializeField]
    private GameObject labelPrefab;


    private static LabelManager sharedInstance;
    public static LabelManager SharedInstance
    {
        get { return sharedInstance; }
    }

    private Dictionary<int, GameObject> labels;


    private void Awake()
    {
        if (sharedInstance != null && sharedInstance != this)
        {
            Destroy(this.gameObject);
        }
        else
        {
            sharedInstance = this;
        }
    }

    // Start is called before the first frame update
    void Start()
    {
        labels = new Dictionary<int, GameObject>();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    /// <summary>
    /// Create a label by parsing the JSON from server and converting information to Unity system.
    /// </summary>
    /// <param name="labelsJSON">JSON from server containing all information to instantiate a label</param>
    public void UpdateLabelsUsingJSON(string labelsJSON)
    {
        if (labelPrefab == null)
        {
            Debug.Log("Label prefab cannot be null.");
            return;
        }
        if (labelsJSON == "")
        {
            Debug.Log("The JSON is empty");
            return;
        }

        Dictionary<int, GameObject> newLabels = new Dictionary<int, GameObject>();

        JArray labelsFromJSON = JArray.Parse(labelsJSON);

        if (labelsFromJSON != null)
        {
            foreach (JObject label in labelsFromJSON)
            {
                if (label == null)
                    return;

                //Get the matrix 4x4 that contains the position and rotation information.
                Matrix4x4 transform = Matrix4x4.zero;
                int i = 0;
                int j = 0;
                foreach (JArray column in label["position"])
                {
                    if (column == null)
                        return;

                    foreach (float value in column)
                    {
                        transform[i, j] = value;
                        i++;
                    }
                    j++;
                    i = 0;

                }

                //Convert coordinate system.
                transform = MathUtilities.ConvertOpenGLToUnitySystem(transform);

                //Get information.
                Vector3 position = transform.ExtractPosition();
                Quaternion rotation = transform.ExtractRotation();
                string textClose = (string)label["info"]["textClose"];
                string textFar = (string)label["info"]["textFar"];
                int id = (int)label["id"];

                if (!labels.ContainsKey(id))
                {
                    if (!newLabels.ContainsKey(id))
                    {
                        //Create new label as it its not in the scene.
                        GameObject labelInstance = InstantiateLabel(labelPrefab, position, rotation, textClose, textFar, id);
                        if (labelInstance != null)
                        {
                            newLabels.Add(id, labelInstance);

                        }
                    }
                    else
                    {
                        Debug.Log("Cannot add this label as a label with the same id is already in the scene.");
                    }

                }
                else
                {
                    //The label is in the scene, so only move the reference from labels to newLabels and update its information.

                    GameObject labelToMove = labels[id];
                    labels.Remove(id);

                    //Update information
                    LabelParameters parameters = labelToMove.GetComponent<LabelParameters>();
                    if(parameters != null)
                    {
                        parameters.SetParameters(textClose, textFar, id);
                    }
                    labelToMove.transform.position = position;
                    labelToMove.transform.rotation = rotation;

                    newLabels.Add(id,labelToMove);
  
                }
               
            }

            //Clean the scene by removing all the labels that are no longer in the scene (the remaining value in labels).
            foreach(GameObject label in labels.Values)
            {
                Destroy(label);
            }

            //Assign toe labels the updated dictionary.
            labels = newLabels;

        }


    }

    /////////////////////////////
    // Instantiate label with text
    ////////////////////////////
    private GameObject InstantiateLabel(GameObject label, Vector3 position, Quaternion rotation, string closeTxt, string farTxt, int identifier)
    {
        if (label == null)
        {
            Debug.Log("Label prefab cannot be null.");
            return null;
        }

        var obj = Instantiate(label, position, rotation);
        if (obj != null)
        {
            obj.GetComponent<LabelParameters>()?.SetParameters(closeTxt, farTxt, identifier);
        }
        return obj;
    }
}
