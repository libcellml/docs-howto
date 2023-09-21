cmake_minimum_required(VERSION 3.10.2)

set(INPUT_HELP "Please enter the name of the implementation file to solve (with extension, .c, .cpp, or .cxx) using the syntax -DINPUT=your_filename.")
set(INPUT "" CACHE FILEPATH ${INPUT_HELP})

if("${INPUT}" STREQUAL "")
    message(FATAL_ERROR "${INPUT_HELP}")
endif()

get_filename_component(INPUTNAME ${INPUT} NAME_WE)
get_filename_component(INPUTDIR ${INPUT} DIRECTORY)

set(PROJECT_NAME solve_${INPUTNAME})

project(${PROJECT_NAME} VERSION 0.1.0)

set(PROJECT_SRC
    solveGeneratedModel.cpp
    ${INPUT}
)

add_executable(${PROJECT_NAME} ${PROJECT_SRC})
target_include_directories(${PROJECT_NAME} PUBLIC ${INPUTDIR})

message("")
message("1) First, build the executable")
message("2) Then, solve by running: ./${PROJECT_NAME} with the arguments:")
message("  -n  step_total")
message("  -dt step_size")
message("")
