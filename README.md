# SafeTrack
## **Team Collaborators:** Nick Lago, Jayden Thomas, John Henry Cooper, Alex Maneri

## **Arm Detection for Tello Control:**
This Python script enables you to control a Tello drone using arm gestures detected through pose estimation. By leveraging computer vision techniques and the Tello drone's SDK, you can perform actions such as takeoff, landing, and altitude control by simply moving your arms.

## **Prerequisites:**
Before running the code, ensure that you have the following prerequisites installed:
Python 3.7 or higher
OpenCV (cv2)
Mediapipe
DJITelloPy
You can install the required packages using 'pip install opencv-python mediapipe djitellopy'

## **Usage:**
Connect your computer to the Tello drone via Wi-Fi.

Run the ArmDetection.py script using the following command:


python ArmDetection.py
A video stream window will open, displaying the Tello drone's camera feed.

Stand in front of the camera with your arms visible.

Raise both of your arms above your shoulders to make the drone take off.

Lower both of your arms to make the drone land.


## **Acknowledgements:**
Special thanks to Professor Barner and Mohammed Baksh for their support throughout the process. Thank you to the developers of these libraries for providing the tools necessary to build this arm detection-based Tello drone control application.

## **References:**
Mediapipe
DJITelloPy
