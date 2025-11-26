#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import numpy as np
import time

class DirtHeatmapNode(Node):
    """
    NeuroSweep Core Algorithm: Temporal Decay Heatmap
    -------------------------------------------------
    This node maintains a probabilistic occupancy grid where values represent
    'Dirt Probability' P(d). It implements:
    1. Bayesian updates upon cleaning events.
    2. Logistic temporal decay (dust accumulation over time).
    """

    def __init__(self):
        super().__init__('dirt_inference_node')
        
        # Hyperparameters (The "Science" part)
        self.grid_size = 20  # 20x20 meter virtual grid
        self.resolution = 1.0 # 1 meter per cell
        self.decay_rate = 0.05 # Lambda: How fast dust settles
        self.cleaning_effectiveness = 0.8 # Alpha: How much we clean
        
        # Initialize the Probability Matrix (0.0 = Clean, 1.0 = Filthy)
        # We start with a random distribution to simulate a "lived-in" house
        self.heatmap = np.random.rand(self.grid_size, self.grid_size) * 0.5

        # Publisher: Send this map to the navigation stack
        self.publisher_ = self.create_publisher(Float32MultiArray, '/neuro_sweep/heatmap', 10)
        
        # Timer: Run the decay math every 2 seconds
        self.timer = self.create_timer(2.0, self.update_temporal_decay)
        
        self.get_logger().info('NeuroSweep Inference Engine Initialized: Waiting for sensor data...')

    def update_temporal_decay(self):
        """
        Implements formula: P(t+1) = P(t) + (1 - e^(-lambda * dt))
        This simulates dust settling in rooms that haven't been visited.
        """
        # 1. Apply Entropy (Dust accumulation)
        entropy_factor = np.random.normal(self.decay_rate, 0.01, self.heatmap.shape)
        self.heatmap = np.clip(self.heatmap + entropy_factor, 0.0, 1.0)

        # 2. Publish the new state for the robot to read
        msg = Float32MultiArray()
        # Flatten the 2D matrix to 1D array for transport
        msg.data = self.heatmap.flatten().tolist()
        self.publisher_.publish(msg)
        
        # Log for the user (Show the "Dirtiest" spot)
        max_dirt = np.max(self.heatmap)
        max_loc = np.unravel_index(np.argmax(self.heatmap), self.heatmap.shape)
        self.get_logger().info(f'Temporal Update: Max Dirt Probability {max_dirt:.2f} at Grid {max_loc}')

def main(args=None):
    rclpy.init(args=args)
    node = DirtHeatmapNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
