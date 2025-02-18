# Drowsiness Detection and Alarming System

## Overview
The drowsiness detection and alarming system is an innovative project leveraging Python and machine learning to combat the critical issue of driver fatigue. This system holds immense potential to significantly reduce the frequent occurrence of road accidents worldwide, thereby enhancing road safety and potentially saving countless lives.

## Key Objectives
The project focuses on two primary tasks:
1. Continuous detection of facial and eye movements of the driver.
2. Activation of alarms to alert the driver upon detecting signs of drowsiness.

## Essential Components
To function effectively, the project relies on three essential Python libraries:
1. **OpenCV**: Enables real-time detection of faces and eyes.
2. **Pygame**: Facilitates the triggering of audible alarms upon detecting drowsiness.
3. **Threading**: Supports efficient management of concurrent tasks, ensuring seamless operation of real-time video processing and independent alarm triggering.

## Workflow
1. **Initialization and Calibration**: The camera initializes and calibrates the system over a 15-second period to compute the average eye blink duration.
2. **Threshold Setting**: Based on calibration results, the system sets a threshold value to trigger alarms.
3. **Real-time Detection**: Once calibrated, the camera continuously monitors for facial presence and eye movements.
4. **Frame Processing**: Each camera frame is analyzed against a pre-trained haar cascade dataset.
5. **Alarm Triggering**: Upon detecting drowsy eyes, identified through sustained matching against the dataset for the specified threshold duration, the system promptly triggers an alarm to alert the driver to wake up.
