#!/usr/bin/env bash
set -eo pipefail

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Select TurtleBot3 model:"
select model in burger waffle waffle_pi quit; do
    case "$model" in
        burger|waffle|waffle_pi)
            export TURTLEBOT3_MODEL="$model"
            break
            ;;
        quit)
            echo "Canceled."
            exit 0
            ;;
        *)
            echo "Invalid selection. Choose 1, 2, 3, or 4."
            ;;
    esac
done

if [ -f /opt/ros/humble/setup.bash ]; then
    source /opt/ros/humble/setup.bash
elif [ -f /opt/ros/foxy/setup.bash ]; then
    source /opt/ros/foxy/setup.bash
elif [ -f /opt/ros/jazzy/setup.bash ]; then
    source /opt/ros/jazzy/setup.bash
fi

if [ -f "$WORKSPACE_DIR/install/setup.bash" ]; then
    source "$WORKSPACE_DIR/install/setup.bash"
fi

echo "Launching turtlebot3_world with TURTLEBOT3_MODEL=$TURTLEBOT3_MODEL"
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
