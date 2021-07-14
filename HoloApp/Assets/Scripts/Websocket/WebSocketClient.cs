using System.Collections;
using System.Collections.Generic;
using System.Text;
using System;
using UnityEngine;
using WebSocketSharp;
using Newtonsoft.Json.Linq;

public class WebSocketClient : MonoBehaviour
{
    // Settings 
    [Header("Settings")]
    [Tooltip("The address of the websocket server")]
    public string WebsocketAddress = "127.0.0.1";
    Camera cam;
    public GameObject labelPrefab;
    private WebSocket ws;
    private Queue<string> messagesFromServer;

    /////////////////////////////
    // Connection to the websocket
    ////////////////////////////
    void Start()
    {
        messagesFromServer = new Queue<string>();

        // initialize camera and websocket
        ws = new WebSocket ($"ws://{WebsocketAddress}");
        cam = Camera.main;
        ws.OnMessage += (sender, e) =>
        {
            string message = e.Data.ToString();
            messagesFromServer.Enqueue(message);
        };

        // connection
        ws.ConnectAsync();
        Debug.Log($"Connected to {WebsocketAddress}");
    }

    /////////////////////////////
    // Send camera coordinates
    ////////////////////////////
    public void getLabels()
    {
        ws.Send("GetLabels");
    }



    void Update()
    {

        //Use X key on PC platform to send a message to the server requesting labels.
        if (Input.GetKeyUp(KeyCode.X))
        {
            getLabels();
        }
        
        //if (message != "") {

        //Pooling server message and creating a label if a message is received.
        if(messagesFromServer.Count != 0)
        {
            CreateLabel(messagesFromServer.Dequeue());
        }
          
    }

    /// <summary>
    /// Create a label by parsing the JSON from server and converting information to Unity system.
    /// </summary>
    /// <param name="labelsJSON">JSON from server containing all information to instantiate a label</param>
    public void CreateLabel(string labelsJSON)
    {
        if (labelPrefab == null)
        {
            Debug.Log("Label prefab cannot be null.");
            return;
        }
        if(labelsJSON == "")
        {
            Debug.Log("The JSON is empty");
            return;
        }

        JArray labels = JArray.Parse(labelsJSON);

        if(labels != null)
        {
            foreach (JObject label in labels)
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

                //Get position and rotation.
                Vector3 position = transform.ExtractPosition();
                Debug.Log((string)label["info"]["textClose"] + "pos:" + position);
                Quaternion rotation = transform.ExtractRotation();
                Debug.Log((string)label["info"]["textClose"] + "rot" + rotation.eulerAngles);

                InstantiateLabel(labelPrefab, position, rotation, (string)label["info"]["textClose"], (string)label["info"]["textFar"], (string)label["id"]);
            }
        }

       
    }

    /////////////////////////////
    // Instantiate label with text
    ////////////////////////////
    private void InstantiateLabel(GameObject label, Vector3 position, Quaternion rotation, string CloseTxt, string FarTxt, string identifier)
    {
        if (label == null)
        {
            Debug.Log("Label prefab cannot be null.");
            return;
        }

        var obj = Instantiate(label, position, rotation);
        if (obj != null)
        {
            obj.GetComponent<LabelParameters>()?.SetParameters(CloseTxt, FarTxt, identifier);
        }
    }
}