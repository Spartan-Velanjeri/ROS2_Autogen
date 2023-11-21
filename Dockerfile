FROM ros:humble-ros-base-jammy

# Install ROS2 packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-desktop-full \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create a directory inside the container to serve as the mount point and a ROS2 Workspace
RUN mkdir -p /ros_autogen_runner /ros2_ws/src

# Set the working directory for subsequent commands
WORKDIR /ros_autogen_runner
