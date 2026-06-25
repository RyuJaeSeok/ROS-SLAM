import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable
from launch.actions import DeclareLaunchArgument
from launch.actions import ExecuteProcess
from launch.actions import IncludeLaunchDescription
from launch.actions import SetEnvironmentVariable
from launch.actions import TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    package_share = get_package_share_directory('6_localize_map')
    turtlebot3_share = get_package_share_directory('turtlebot3_gazebo')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')
    nav2_bringup_share = get_package_share_directory('nav2_bringup')

    launch_file_dir = os.path.join(turtlebot3_share, 'launch')
    # world = os.path.join(package_share, 'worlds', 'custom_world.world')
    # map_yaml = os.path.join(package_share, 'map', 'custom_world.yaml')
    world = os.path.join(package_share, 'worlds', 'narrow_world_w_obstacles.world')
    map_yaml = os.path.join(package_share, 'map', 'narrow_map.yaml')

    burger_model = os.path.join(package_share, 'models', 'turtlebot3_burger', 'model.sdf')
    ekf_config = os.path.join(package_share, 'config', 'ekf.yaml')
    nav2_params = os.path.join(package_share, 'config', 'nav2_params.yaml')
    rviz_default_config = os.path.join(package_share, 'config', 'custom_nav2.rviz')
    burger_bridge = os.path.join(package_share, 'config', 'burger_bridge.yaml')

    model = LaunchConfiguration('model')
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_nav2 = LaunchConfiguration('use_nav2')
    use_rviz = LaunchConfiguration('use_rviz')
    use_ekf = LaunchConfiguration('use_ekf')
    set_initial_pose = LaunchConfiguration('set_initial_pose')
    rviz_config = LaunchConfiguration('rviz_config')
    autostart = LaunchConfiguration('autostart')
    x_pose = LaunchConfiguration('x_pose')
    y_pose = LaunchConfiguration('y_pose')
    yaw = LaunchConfiguration('yaw')

    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': ['-r -s -v2 ', world],
            'on_exit_shutdown': 'true',
        }.items(),
    )

    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': '-g -v2 ',
            'on_exit_shutdown': 'true',
        }.items(),
    )

    robot_state_publisher = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
    )

    spawn_turtlebot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', model,
            '-file', burger_model,
            '-x', x_pose,
            '-y', y_pose,
            '-z', '0.01',
        ],
        output='screen',
    )

    gazebo_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={burger_bridge}',
        ],
        output='screen',
    )

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_share, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': map_yaml,
            'use_sim_time': use_sim_time,
            'autostart': autostart,
            'params_file': nav2_params,
        }.items(),
        condition=IfCondition(use_nav2),
    )

    rviz = ExecuteProcess(
        cmd=['rviz2', '-d', rviz_config],
        output='screen',
        condition=IfCondition(use_rviz),
    )

    robot_localization = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[ekf_config],
        condition=IfCondition(use_ekf),
    )

    initial_pose = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='6_localize_map',
                executable='initial_pose_pub',
                output='screen',
                parameters=[{
                    'use_sim_time': use_sim_time,
                    'x': x_pose,
                    'y': y_pose,
                    'yaw': yaw,
                }],
            ),
        ],
        condition=IfCondition(set_initial_pose),
    )

    return LaunchDescription([
        DeclareLaunchArgument('model', default_value='burger'),
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('use_nav2', default_value='true'),
        DeclareLaunchArgument('use_rviz', default_value='true'),
        DeclareLaunchArgument('use_ekf', default_value='false'),
        DeclareLaunchArgument('set_initial_pose', default_value='true'),
        DeclareLaunchArgument(
            'rviz_config',
            default_value=rviz_default_config,
        ),
        DeclareLaunchArgument('autostart', default_value='true'),
        DeclareLaunchArgument('x_pose', default_value='-2.0'),
        DeclareLaunchArgument('y_pose', default_value='-0.5'),
        DeclareLaunchArgument('yaw', default_value='0.0'),
        SetEnvironmentVariable('TURTLEBOT3_MODEL', model),
        AppendEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            os.path.join(turtlebot3_share, 'models'),
        ),
        gzserver,
        gzclient,
        robot_state_publisher,
        spawn_turtlebot,
        gazebo_bridge,
        robot_localization,
        nav2,
        rviz,
        initial_pose,
    ])
