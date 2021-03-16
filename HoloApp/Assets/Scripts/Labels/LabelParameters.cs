using System.Collections;
using System;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class LabelParameters : MonoBehaviour
{
    [Header("Settings")]
    [Tooltip("Distance which changes text")]
    public float Distance = 0.7f;
    [Tooltip("Text displayed when you are far from the object, relative to Distance parameter")]
    public string DistantText = "Far from me";
    [Tooltip("Text displayed when you are close to the object, relative to Distance parameter")]
    public string CloseText = "Close to me";
    private long id;

    private Camera cam;
    private GameObject label, contentGo;
    private TextMeshPro content;

    // Initialisation 
    void Start()
    {
        cam = Camera.main;
        label = this.gameObject;
        contentGo = label.transform.GetChild (0).gameObject;
        content = contentGo.GetComponent<TextMeshPro>();
    }

    // Check the distance between the camera and the label
    void Update()
    {
        Vector3 difference = cam.transform.position - label.transform.position;
        if(Mathf.Abs(difference.x) < Distance && Mathf.Abs(difference.z) < Distance && Mathf.Abs(difference.y) < Distance)
        {   
            content.text = CloseText;
        }else {
            content.text = DistantText;
        }
    }

    public void SetParameters(string close, string far, long identifier)
    {
        DistantText = far;
        CloseText = close;
        id = identifier;
    }
}
