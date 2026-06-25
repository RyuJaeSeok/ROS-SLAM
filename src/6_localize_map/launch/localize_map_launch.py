import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():

    # 1. Burger 모델
    set_model = SetEnvironmentVariable(
        name='TURTLEBOT3_MODEL',
        value='burger'
    )

    # 2. Turtlebot3 Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('turtlebot3_gazebo'),
                'launch',
                'turtlebot3_world.launch.py'
            ])
        )
    )

    # 3. SLAM Toolbox
    slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('slam_toolbox'),
                'launch',
                'online_async_launch.py'
            ])
        )
    )

    # 4. RViz2 실행 (config 포함)
    rviz = ExecuteProcess(
        cmd=[
            'rviz2',
            '-d',
            os.path.expanduser('~/.rviz2/localization_map.rviz')
        ],
        output='screen'
    )

    # 5. 로봇 주행 노드 실행
    corner_escape = ExecuteProcess(
        cmd=[
            'gnome-terminal', '--', 'bash', '-c',
            'source ~/colcon_ws/install/setup.bash; '
            'ros2 run 6_localize_map simple_yaw_oa; '
            'exec bash'
        ],
        output='screen'
    )

    return LaunchDescription([
        set_model,
        gazebo,
        slam_toolbox,
        rviz,
        corner_escape,
    ])