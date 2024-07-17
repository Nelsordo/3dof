import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/ubb/Downloads/ros2_ws_final/ros2_ws/install/3dof'
