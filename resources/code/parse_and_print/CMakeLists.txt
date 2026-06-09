cmake_minimum_required(VERSION 3.24)
set(PROJECT_NAME parse_and_print)

project(${PROJECT_NAME} VERSION 0.1.0)

find_package(libCellML REQUIRED)

set(_PART_SRC parse_and_print.cpp)
add_executable(parse_and_print ${_PART_SRC})
target_link_libraries(parse_and_print PUBLIC cellml)
