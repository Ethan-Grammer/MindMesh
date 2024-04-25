using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class tv : MonoBehaviour
{
    public GameObject light;
    public TcpServer tcp;
    //public Material objectMaterial;
    //public Color newColor; 
    //public Renderer r;
    public bool act;
    //public string S;
    void Update()
    {
       /* if(Input.GetKeyDown(S)){
            if(act){
                light.SetActive(false);
                act = false;
            }
            else{
                light.SetActive(true);
                act = true;
            }
            Debug.Log("pressed");
        } */
    
        if(tcp.tv != act){
            act = tcp.tv;
            light.SetActive(act);
        }
    }
}


