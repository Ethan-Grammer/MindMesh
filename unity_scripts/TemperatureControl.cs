using UnityEngine;

public class TemperatureAndParticleController : MonoBehaviour
{
    public TcpServer tcp;
    private int temp = 60; // Initial temperature
    private bool isACOn = false; // AC state, initially off
    public ParticleSystem ps; // Reference to the Particle System
    private ParticleSystem.MainModule psMain;

    void Start()
    {
        psMain = ps.main; // Get the main module from the particle system
        ps.Stop(); // Ensure the particle system is stopped initially
    }

    void Update()
    {
        // Toggle AC on/off with the '3' key
        if (tcp.ac != isACOn)
        {
            isACOn = !isACOn; // Toggle AC state
            //Debug.Log($"AC is now {(isACOn ? "On" : "Off")}");
            // Control the particle system based on AC state
            if (isACOn)
            {
                ps.Play(); // Start the particle system when AC is turned on
                Debug.Log("Particle system started.");
            }
            else
            {
                ps.Stop(); // Stop the particle system when AC is turned off
                Debug.Log("Particle system stopped.");
            }
        }

        // Process temperature change only if the AC is on
        if (isACOn)
        {
            bool changed = false;
            int tempChange = 0;

            // Increase temperature with the up arrow key
            if (Input.GetKeyDown(KeyCode.UpArrow))
            {
                tempChange = 5;
            }
            // Decrease temperature with the down arrow key
            else if (Input.GetKeyDown(KeyCode.DownArrow))
            {
                tempChange = -5;
            }

            // Apply the temperature change
            if (tempChange != 0)
            {
                temp += tempChange;
                changed = true;
                //AdjustColorBasedOnTemperature(temp); // Adjust color when temperature changes
            }

            if (changed)
            {
                Debug.Log($"Temperature: {temp}");
            }
        }
    }

  /*  void AdjustColorBasedOnTemperature(int temperature)
    {
        float minTemperature = 40;
        float maxTemperature = 80;
        float neutralTemperature = 60;

        Color coldColor = new Color(0.5f, 0.5f, 1f);  
        Color hotColor = new Color(1f, 0.5f, 0.5f);  
        Color neutralColor = Color.white;

        float t;
        if (temperature <= neutralTemperature)
            t = Mathf.InverseLerp(minTemperature, neutralTemperature, temperature);
        else
            t = Mathf.InverseLerp(neutralTemperature, maxTemperature, temperature);

        Color newColor = (temperature < neutralTemperature) ?
            Color.Lerp(coldColor, neutralColor, t) :
            Color.Lerp(neutralColor, hotColor, t);

        psMain.startColor = new ParticleSystem.MinMaxGradient(newColor);
    } */

   /* void OnGUI()
    {
        GUIStyle guiStyle = new GUIStyle();
        guiStyle.fontSize = 24;
        guiStyle.normal.textColor = Color.white;

        // Display the AC status and temperature on the screen
        GUI.Label(new Rect(10, 10, 300, 30), $"AC: {(isACOn ? "On" : "Off")}, Temperature: {temp}", guiStyle);
    } */
}

