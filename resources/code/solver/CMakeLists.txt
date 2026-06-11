cmake_minimum_required(VERSION 3.21)

set(INPUT_HELP "Please enter the name of the model file to solve (with extension, .xml, or .cellml) using the syntax -DINPUT_MODEL=your_filename.")
set(INPUT_MODEL "$ENV{INPUT_MODEL}" CACHE FILEPATH ${INPUT_HELP})

if("${INPUT_MODEL}" STREQUAL "")
    message(FATAL_ERROR "${INPUT_HELP}")
endif()

get_filename_component(INPUTNAME ${INPUT_MODEL} NAME_WE)
get_filename_component(INPUTDIR ${INPUT_MODEL} DIRECTORY)

set(PROJECT_NAME solve_${INPUTNAME})

project(${PROJECT_NAME} VERSION 0.1.0)

execute_process(
    COMMAND python "${CMAKE_CURRENT_SOURCE_DIR}/generateModel.py" -m ${INPUT_MODEL} -p C -o ${CMAKE_CURRENT_BINARY_DIR}
    OUTPUT_VARIABLE _OUT
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

string(REPLACE "Generated file: " "" GENERATED_C_MODEL "${_OUT}")
get_filename_component(GENERATED_FILE_NAME "${GENERATED_C_MODEL}" NAME)
string(REPLACE ".c" ".h" GENERATED_HEADER "${GENERATED_FILE_NAME}")

configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/generated_include.h.in
    ${CMAKE_CURRENT_BINARY_DIR}/generated_include.h
    @ONLY
)

set(PROJECT_SRC
    solveGeneratedModel.cpp
    ${GENERATED_C_MODEL}
)

add_executable(${PROJECT_NAME} ${PROJECT_SRC})
target_include_directories(${PROJECT_NAME} PUBLIC "${CMAKE_CURRENT_BINARY_DIR}")
target_compile_features(${PROJECT_NAME} PUBLIC cxx_std_20)

message("")
message("1) First, build the executable")
message("2) Then, solve by running: ./${PROJECT_NAME} with the arguments:")
message("  -n  step_total")
message("  -dt step_size")
message("")
