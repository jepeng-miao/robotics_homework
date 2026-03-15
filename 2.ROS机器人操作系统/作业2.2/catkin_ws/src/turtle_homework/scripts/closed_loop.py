#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math  # 必须导入 math 库，用于数学计算


class TurtleController:
    def __init__(self):
        # 初始化节点，使用 anonymous=True 确保每次运行都有唯一ID，避免冲突
        rospy.init_node('turtle_closed_loop', anonymous=True)
        self.pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/turtle1/pose', Pose, self.pose_callback)

        self.current_pose = Pose()
        self.rate = rospy.Rate(10)  # 10 Hz 的控制频率

    def pose_callback(self, data):
        self.current_pose = data

    def normalize_angle(self, angle):
        """
        角度归一化函数：将角度限制在 [-pi, pi] 范围内
        解决 3.14 -> -3.14 的跳变问题，防止小海龟转大圈
        """
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

    def go_to(self, target_x, target_y):
        """带 PID 控制的移动函数"""
        # PID 参数 (你可以微调这里的数值)
        Kp_linear = 1.2  # 前进速度的比例系数
        Kp_angular = 4.0 # 转弯速度的比例系数 (调大一点让转弯更果断)

        rospy.loginfo(f"前往目标点: ({target_x}, {target_y})")

        while not rospy.is_shutdown():
            # 1. 计算距离
            dx = target_x - self.current_pose.x
            dy = target_y - self.current_pose.y
            distance = math.sqrt(dx**2 + dy**2)

            # 2. 计算角度差
            # 目标航向角
            target_theta = math.atan2(dy, dx)
            # 当前航向角
            current_theta = self.current_pose.theta

            # 关键步骤：归一化角度差，防止跳变
            angle_error = target_theta - current_theta
            angle_error = self.normalize_angle(angle_error)

            # 3. PID 控制逻辑
            # 前进速度：距离越远越快
            linear_vel = Kp_linear * distance
            # 限制最大速度，防止过冲
            if linear_vel > 2.0:
                linear_vel = 2.0

            # 转弯速度：角度差越大越快
            angular_vel = Kp_angular * angle_error

            # 4. 到达判定
            if distance < 0.1:
                rospy.loginfo("到达目标点！")
                break

            # 5. 发布速度指令
            vel_msg = Twist()
            vel_msg.linear.x = linear_vel
            vel_msg.angular.z = angular_vel
            self.pub.publish(vel_msg)

            self.rate.sleep()

    def stop(self):
        """停止小海龟"""
        vel_msg = Twist()
        self.pub.publish(vel_msg)


def run_square():
    # 实例化控制器放在循环外，避免重复初始化节点
    controller = TurtleController()
    time.sleep(1)  # 等待订阅者连接

    # 定义正方形的四个顶点
    points = [
        (2.0, 2.0),
        (6.0, 2.0),
        (6.0, 6.0),
        (2.0, 6.0)
    ]

    try:
        for point in points:
            controller.go_to(point[0], point[1])
    except rospy.ROSInterruptException:
        pass

    # 最后停止
    controller.stop()


if __name__ == '__main__':
    run_square()