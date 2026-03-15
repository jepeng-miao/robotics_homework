#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
import time

def move_in_square_open():
    # 1. 初始化节点
    rospy.init_node('turtle_open_loop', anonymous=True)
    # 2. 创建发布者，发布到 /turtle1/cmd_vel 话题
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    rate = rospy.Rate(10) # 10 Hz

    # 定义速度
    linear_speed = 2.0
    angular_speed = 1.57 # 90度约等于 1.57 rad

    # 3. 循环4次画正方形
    for _ in range(4):
        # --- 步骤A: 直线前进 ---
        vel_msg = Twist()
        vel_msg.linear.x = linear_speed
        vel_msg.angular.z = 0.0

        # 设定持续时间（例如走2米，速度2m/s，需要1秒）
        t0 = rospy.Time.now().to_sec()
        duration = 1.0
        while rospy.Time.now().to_sec() - t0 < duration:
            pub.publish(vel_msg)
            rate.sleep()

        # --- 步骤B: 原地左转 ---
        vel_msg.linear.x = 0.0
        vel_msg.angular.z = angular_speed

        # 转弯时间（转90度，速度1.57 rad/s，需要1秒）
        t0 = rospy.Time.now().to_sec()
        duration = 1.0
        while rospy.Time.now().to_sec() - t0 < duration:
            pub.publish(vel_msg)
            rate.sleep()

    # 停止
    pub.publish(Twist())

if __name__ == '__main__':
    try:
        move_in_square_open()
    except rospy.ROSInterruptException:
        pass