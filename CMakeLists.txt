cmake_minimum_required(VERSION 3.20)
project(drainy)

find_package(ament_cmake REQUIRED)
find_package(drainy_common REQUIRED)
find_package(drainy_controller REQUIRED)
find_package(drainy_explorer REQUIRED)
find_package(drainy_localizer REQUIRED)
find_package(drainy_maps_manager REQUIRED)
find_package(drainy_planner REQUIRED)

install(DIRECTORY config launch
        DESTINATION share/${PROJECT_NAME})

ament_export_dependencies(
  drainy_common
  drainy_controller
  drainy_explorer
  drainy_localizer
  drainy_maps_manager
  drainy_planner
)

ament_package()