import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    rviz = LaunchConfiguration('rviz')

    config_folder = get_package_share_directory('elevation_mapping')
    elevation_mapping_config = os.path.join(config_folder, 'config', 'elevation_mapping.yaml')
    grid_map_filters_config = os.path.join(config_folder, 'config', 'grid_map_filters.yaml')
    grid_map_visualization_config = os.path.join(config_folder, 'config', 'grid_map_visualization.yaml')
    grid_map_converter_config = os.path.join(config_folder, 'config', 'grid_map_converter.yaml')
    rviz_config = os.path.join(config_folder, 'rviz', 'elevation_mapping.rviz')

    grid_map_filters_node = Node(
        package='grid_map_demos',
        executable='filters_demo',
        name='grid_map_filters',
        output='screen',
        parameters=[grid_map_filters_config, {'use_sim_time': use_sim_time}]
    )

    grid_map_visualization_node = Node(
        package='grid_map_visualization',
        executable='grid_map_visualization',
        name='grid_map_visualization',
        output='screen',
        parameters=[grid_map_visualization_config, {'use_sim_time': use_sim_time}]
    )

    grid_map_converter_node = Node(
        package='scout_navigation',
        executable='gridmap_converter_node',
        name='gridmap_converter',
        output='screen',
        parameters=[grid_map_converter_config, {'use_sim_time': use_sim_time}]
    )

    elevation_mapping_node = Node(
        package='elevation_mapping',
        executable='elevation_mapping_node',
        output='screen',
        parameters=[elevation_mapping_config, {'use_sim_time': use_sim_time}]
    )

    tf_to_pose_publisher_node = Node(
        package='elevation_mapping',
        executable='tf_to_pose_publisher.py',
        name='tf_to_pose_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': use_sim_time}],
        condition=IfCondition(rviz),
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='True',
            description='Use simulation (Gazebo) clock if true'
        ),
        DeclareLaunchArgument(
            'rviz',
            default_value='True',
            description='Launch RViz with elevation mapping displays'
        ),
        grid_map_filters_node,
        grid_map_visualization_node,
        grid_map_converter_node,
        elevation_mapping_node,
        tf_to_pose_publisher_node,
        rviz_node,
    ])

