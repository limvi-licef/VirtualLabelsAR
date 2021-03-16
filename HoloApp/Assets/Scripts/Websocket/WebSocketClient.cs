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
    public GameObject Label;
    private WebSocket ws;
    private string message = "";

    /////////////////////////////
    // Connection to the websocket
    ////////////////////////////
    void Start()
    {
        // initialize camera and websocket
        ws = new WebSocket ($"ws://{WebsocketAddress}");
        cam = Camera.main;
        ws.OnMessage += (sender, e) =>
        {
            message = e.Data.ToString();
        };

        // connection
        ws.Connect ();
        Debug.Log($"Connected to {WebsocketAddress}");
    }

    /////////////////////////////
    // Send camera coordinates
    ////////////////////////////
    public void getLabels()
    {
        ws.Send("GetLabels");
    }

    /////////////////////////////
    // Instantiate label with text
    ////////////////////////////
    private void InstantiateLabel(GameObject label, Vector3 position, Quaternion rotation, string CloseTxt, string FarTxt, long identifier)
    {
        var obj = Instantiate(label, position, rotation);
        obj.GetComponent<LabelParameters> ().SetParameters(CloseTxt, FarTxt, identifier);
    }

    /////////////////////////////
    // Use key input to test sending keyword and receiving coordinates
    ////////////////////////////
    void Update()
    {
        if (Input.GetKeyUp(KeyCode.X))
        {
            getLabels();
        }
        
        if (message != "") {
            
            JObject json = JObject.Parse(message);
            Debug.Log("Labels received");

            Vector3 position = new Vector3((float)json["position"][0],(float)json["position"][1],(float)json["position"][2]);
            Vector3 orientation = new Vector3((float)json["orientation"][0],(float)json["orientation"][1],(float)json["orientation"][2]);
            Quaternion rotation = Quaternion.LookRotation(orientation, new Vector3(0,1,0));

            InstantiateLabel(Label, position, rotation, (string)json["close"], (string)json["far"], (long)json["id"]);
            
            message = "";
        }
    }
}