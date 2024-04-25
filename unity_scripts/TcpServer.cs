using UnityEngine;
using System;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class TcpServer : MonoBehaviour
{
    private TcpListener tcpListener;
    private Thread tcpListenerThread;
    private TcpClient connectedTcpClient;

    public bool lightBool = false; // Example state
    public bool ac = false;
    public bool tv = false;

    void Start()
    {
        tcpListenerThread = new Thread(new ThreadStart(ListenForIncomingRequests));
        tcpListenerThread.IsBackground = true;
        tcpListenerThread.Start();
    }

    private void ListenForIncomingRequests()
{
    try
    {
        tcpListener = new TcpListener(IPAddress.Any, 8080);
        tcpListener.Start();
        Debug.Log("Server is listening on port 8080");
    }
    catch (Exception e)
    {
        Debug.LogError("Failed to start server: " + e.Message);
        return;
    }

    try
    {
        while (true)
        {
            using (connectedTcpClient = tcpListener.AcceptTcpClient())
            {
                using (NetworkStream stream = connectedTcpClient.GetStream())
                {
                    byte[] buffer = new byte[connectedTcpClient.ReceiveBufferSize];
                    int bytesRead = stream.Read(buffer, 0, buffer.Length);
                    string message = Encoding.ASCII.GetString(buffer, 0, bytesRead);
                    Debug.Log("Received: " + message);
                    ProcessMessage(message);
                    if(!lightBool && !ac && !tv){
                        lightBool = true;
                    }
                    else if(lightBool && !tv){
                        tv = true;
                    }
                    else if(lightBool && tv && !ac){
                        ac = true;
                    }
                    else{
                        lightBool = false;
                        ac = false;
                        tv = false;
                    }
                }
            }
        }
    }
    catch (Exception e)
    {
        Debug.LogError("Server run-time error: " + e.Message);
    }
}


    private void ProcessMessage(string message)
    {
        try
        {
            KeyData data = JsonUtility.FromJson<KeyData>(message);
            switch (data.key)
            {
                case "F1_PRESS":
                    Debug.Log("F1 key pressed");
                    // Implement functionality for F1 press
                    ToggleLights(); // Example function
                    break;
                case "F1_HOLD":
                    Debug.Log("F1 key held");
                    // Implement functionality for F1 hold
                    ToggleLights();
                    break;
                case "F2_PRESS":
                    Debug.Log("F2 key pressed");
                    // Implement functionality for F2 press
                    ToggleLights();
                    break;
                case "F2_HOLD":
                    Debug.Log("F2 key held");
                    // Implement functionality for F2 hold
                    ToggleLights();
                    break;
                default:
                    Debug.Log("Unknown command received: " + data.key);
                    break;
            }
        }
        catch (Exception e)
        {
            Debug.Log("Error parsing JSON: " + e.Message);
        }
    }

    private void ToggleLights()
    {
        lightBool = !lightBool;
        Debug.Log("Light toggled: " + lightBool);
    }

    private void OnApplicationQuit()
    {
        if (tcpListenerThread != null)
        {
            tcpListenerThread.Interrupt();
            tcpListenerThread.Abort();
        }
        if (tcpListener != null)
        {
            tcpListener.Stop();
        }
    }

    [Serializable]
    public class KeyData
    {
        public string key;
    }
}
