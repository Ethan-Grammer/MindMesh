using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LightController : MonoBehaviour
{
    public TcpServer tcp;
    public GameObject light;
    private bool act;
    //public string S;
    void Update()
    {
        if(tcp.lightBool != act){
            act = tcp.lightBool;
            light.SetActive(act);
        }
    }
}


