cmake_minimum_required(VERSION 3.24)
set(PROJECT_NAME check_model)

project(${PROJECT_NAME} VERSION 0.1.0)

find_package(libCellML REQUIRED)

set(_PART_SRC ${PROJECT_NAME}.cpp)
add_executable(${PROJECT_NAME} ${_PART_SRC})
target_link_libraries(${PROJECT_NAME} PUBLIC cellml)
