# Coordinating Timing and Data Fusion in an Emergency Vehicle Detection Use Case  

This use case demonstrates the implementation of an **Emergency Vehicle Detection (EVD)** system using **Lingua Franca**, with support from the [`edgeai-python`](https://github.com/lf-pkgs/edgeai-python) library. The system combines **Audio Classification** and **Object Detection** models to identify fire trucks approaching an intersection. 

When the outputs of these models are fused and confirm the presence of a fire truck, the system triggers an **actuation** to prioritize the emergency vehicle by:  

1. **Changing the traffic light** to green on the lane where the emergency vehicle is approaching (if it is currently red), or  
2. **Extending the green light duration** to ensure the emergency vehicle passes through the intersection smoothly.  

This use case addresses the **Traffic Signal Preemption** challenge, where traffic signals dynamically adapt to provide priority for emergency vehicles, ensuring their swift and safe passage through intersections.  
