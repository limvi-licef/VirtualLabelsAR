using System.Collections;
using System.Collections.Generic;
using System.Text;
using System;
using UnityEngine;
using WebSocketSharp;


public class WebSocketClient : MonoBehaviour
{
    // Settings 
    [Header("Settings")]
    [Tooltip("The address of the websocket server")]
    public string WebsocketAddress = "127.0.0.1";
    Camera cam;
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
            LabelManager.SharedInstance?.UpdateLabelsUsingJSON(messagesFromServer.Dequeue());
        }
          
    }

  
}