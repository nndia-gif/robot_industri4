import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class PoseEstimator(Node):
    def __init__(self):
        super().__init__('pose_estimator')

        self.subscription = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)

        self.v = 0.0
        self.omega = 0.0

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.last_update = self.get_clock().now()
        self.last_command_time = self.get_clock().now()
        self.last_print_time = self.get_clock().now()

        self.timer = self.create_timer(0.02, self.update_pose)

        self.get_logger().info('Pose estimator aktif. Posisi awal diasumsikan X=0, Y=0, Yaw=0.')

    def cmd_vel_callback(self, msg):
        self.v = msg.linear.x
        self.omega = msg.angular.z
        self.last_command_time = self.get_clock().now()

    def update_pose(self):
        now = self.get_clock().now()
        
        dt = (now - self.last_update).nanoseconds / 1e9
        self.last_update = now

        dt = min(dt, 0.1)

        time_since_cmd = (now - self.last_command_time).nanoseconds / 1e9
        if time_since_cmd > 0.5:
            v = 0.0
            omega = 0.0
        else:
            v = self.v
            omega = self.omega

        if abs(omega) < 1e-9:
            self.x += v * math.cos(self.theta) * dt
            self.y += v * math.sin(self.theta) * dt
        else:
            delta_theta = omega * dt
            self.x += (v / omega) * (math.sin(self.theta + delta_theta) - math.sin(self.theta))
            self.y += (v / omega) * (math.cos(self.theta) - math.cos(self.theta + delta_theta))
            self.theta += delta_theta

        time_since_print = (now - self.last_print_time).nanoseconds / 1e9
        if time_since_print >= 0.5:
            yaw_deg = math.degrees(self.theta)
            # Modulo 360 agar sudut 360 derajat terbaca sebagai 0.0
            yaw_deg = yaw_deg % 360.0 
            
            self.get_logger().info(
                f'ESTIMASI | X = {self.x:.2f} m | Y = {self.y:.2f} m | Yaw = {yaw_deg:.1f} deg | v = {v:.2f} m/s | omega = {omega:.2f} rad/s'
            )
            self.last_print_time = now

def main(args=None):
    rclpy.init(args=args)
    node = PoseEstimator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
