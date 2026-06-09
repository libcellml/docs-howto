cmake_minimum_required(VERSION 3.24)
set(PROJECT_NAME include_libcellml)

project(${PROJECT_NAME} VERSION 0.1.0)

find_package(libCellML REQUIRED)

set(_PART_SRC include_libcellml.cpp)
add_executable(include_libcellml ${_PART_SRC})
target_link_libraries(include_libcellml PUBLIC cellml)
