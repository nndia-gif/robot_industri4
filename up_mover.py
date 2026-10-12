import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MoverNode(Node):
    def __init__(self):
        super().__init__('mover_node')

        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.start_time = None

    def timer_callback(self):
        current_time = self.get_clock().now()

        if current_time.nanoseconds == 0:
            return
            
        if self.start_time is None:
            self.start_time = current_time
            self.get_logger().info('Menunggu 2 detik agar koneksi ROS 2 stabil...')

        msg = Twist()
        elapsed_time = (current_time - self.start_time).nanoseconds / 1e9

        t0 = 2.0                          
        
        t1 = t0 + 5.0                     
        t2 = t1 + math.pi                 
        t3 = t2 + 3.0                     
        t4 = t3 + math.pi                 
        t5 = t4 + 5.0                     
        t6 = t5 + math.pi                 
        t7 = t6 + 3.0                     
        t8 = t7 + math.pi                 
        if elapsed_time < t0:
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        elif elapsed_time < t1:
            msg.linear.x = 0.5
            msg.angular.z = 0.0
            self.get_logger().info('Sisi 1: Gerak Maju Kedepan...')

        elif elapsed_time < t2:
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.get_logger().info('Belok 1...')

        elif elapsed_time < t3:
            msg.linear.x = 0.5
            msg.angular.z = 0.0
            self.get_logger().info('Sisi 2: Gerak Maju Kekiri...')

        elif elapsed_time < t4:
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.get_logger().info('Belok 2...')

        elif elapsed_time < t5:
            msg.linear.x = 0.5
            msg.angular.z = 0.0
            self.get_logger().info('Sisi 3: Gerak Maju Kebawah...')

        elif elapsed_time < t6:
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.get_logger().info('Belok 3...')

        elif elapsed_time < t7:
            msg.linear.x = 0.5
            msg.angular.z = 0.0
            self.get_logger().info('Sisi 4: Gerak Maju Kekanan (Kembali ke titik awal)...')

        elif elapsed_time < t8:
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.get_logger().info('Belok 4: Menyesuaikan arah Yaw ke 0...')

        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.get_logger().info('Berhenti.')
            self.publisher_.publish(msg)
            self.timer.cancel()
            rclpy.shutdown()
            return

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = MoverNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()
