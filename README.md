# MindMesh (Bitcamp 2024)

## Inspiration
With brain-computer interface technology like Neuralink gaining popularity, we sought to offer a non-intrusive alternative, with a focus on accessibility and downright convenience.

We figured that although the technology was interesting, it still had to solve a genuine problem, and we could provide the most value for users who need seamless integration of assistive technology into their everyday lives. 

## What It Does
MindMesh monitors & interprets EEG brainwaves using the Neurosity Crown, allowing users to interface with IoT applications via thought. This includes controlling smart home devices such as lights and televisions just by using your imagination, potentially providing increased accessibility and support for those with visual/physical capabilities. 

## How We Built It
### Neurosity SDK
This allowed us to access raw, real-time EEG data streamed directly from the Crown headset. One of the key data-points we handled was ‘predictions’, a list that provides crucial user data such as the label of the user’s thought, along with a probability and confidence interval.

(simplified example) : 'predictions': [{'label': leftArm, 'probability': 0.867}]

Using this SDK, we developed controllers that perform data cleaning and interpretation. These classes interface with the client application, to determine when a POST request should be sent to the Unity server.

### Unity Server
This is the backbone of the virtual environment, listening for requests from the client applications and determining the corresponding action to be performed in the virtual environment (dimming lights, turning on the A/C, etc.). 

### Light Listener
This separate server application allowed us to communicate with the physical smart light bulb
for our demo, listening for POST requests from the client and then either turning the bulb on/off/brighter/dimmer.

## Challenges We Ran Into
As soon as we had all of the individual parts working, our headset was severely damaged during a demo. This resulted in the loss of training data due to connectivity/syncing issues. 

This meant that we needed to find a different way to interpret partial & messy data, with a level of accuracy high enough to build a functional application. 

## Accomplishments that We're Proud of
It seemed like with every new feature we wanted to add, we needed to figure out some scrappy, slapped-together approach that involved quick and collaborative brainstorming. We were all able to learn something new, ranging from languages to programmable light bulbs.

## What We Learned
We learned that when working on a large-scope project with multiple evolving elements, communication is essential. Oftentimes we’d find out two people were building cannibalizing features, or one person is expecting an input from another component that wasn’t accounted for.

Although we each focused our work on specialized components, we realized that we needed to have a stronger understanding of how the system operated as a whole.

## What's Next for MindMesh
The Neurosity Crown itself provides accurate data at a reasonable speed, but their SDK is relatively underdeveloped. We’re aiming to refactor the open-source SDK, allowing for more developer functionality such as subscription-multithreading, variable polling rates, etc.

Doing so will allow developers to build applications for more IoT devices, promoting a wider range of accessibility applications.
