#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <pkg_name>"
    exit 1
fi

pkg_name="$1"

if [ -d "$pkg_name" ]; then
    echo "Error: package directory already exists: $pkg_name"
    exit 1
fi

ros2 pkg create "$pkg_name" \
    --build-type ament_python \
    --dependencies rclpy std_msgs geometry_msgs sensor_msgs nav_msgs
