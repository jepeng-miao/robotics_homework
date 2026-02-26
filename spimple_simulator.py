#!/usr/bin/env python3
"""
author: jepeng
"""

import time
import random

robot_name = "Jepeng H1"
battery = 100.0
position = 0.0
obstacle_pos = random.uniform(1.0,20.0)
is_running = True

print(f"---system start{robot_name}---")
print(f"---obstacle is in {obstacle_pos:.1f}m ---")
def move_forward(current_pose, speed):
    noise = random.uniform(-0.1, 0.1)
    distance = speed + noise
    new_pose = current_pose + distance
    return new_pose

while is_running:
    if battery < 20:
        print("[WARNING] Low Battery! System Shutting Down...")
        is_running = False
        break
    position = move_forward(position, 1.5)
    if(position>=obstacle_pos):
        print("[WARNING] Obstacle! Stop!")
        is_running = False
        break
    battery -= 5.0
    print(f"[Log] Pose: {position:.2f} m | Battery: {battery:.1f}% | Status: Running")
    time.sleep(0.5)

print("system shutdown.")
