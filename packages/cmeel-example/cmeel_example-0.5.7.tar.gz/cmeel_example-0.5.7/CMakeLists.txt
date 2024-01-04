cmake_minimum_required(VERSION 3.17)

# Project properties
set(PROJECT_ORG cmake-wheel)
set(PROJECT_NAME cmeel-example)
set(PROJECT_DESCRIPTION "This is an example project, to show how to use cmeel")
set(PROJECT_URL https://github.com/${PROJECT_NAMESPACE}/${PROJECT_NAME})

# Project options
option(BUILD_PYTHON_INTERFACE "Build the python binding" ON)
option(SUFFIX_SO_VERSION "Suffix library name with its version" ON)

# Project configuration
set(PROJECT_USE_CMAKE_EXPORT TRUE)
set(CUSTOM_HEADER_DIR cmeel/example)

include(FetchContent)

# Check if the submodule cmake have been initialized
set(JRL_CMAKE_MODULES "${CMAKE_CURRENT_LIST_DIR}/cmake")
if(NOT EXISTS "${CMAKE_SOURCE_DIR}/cmake/base.cmake")
  message(STATUS "JRL cmakemodules not found. Let's fetch it.")
  FetchContent_Declare(
    "jrl-cmakemodules"
    GIT_REPOSITORY "https://github.com/jrl-umi3218/jrl-cmakemodules.git")
  FetchContent_MakeAvailable("jrl-cmakemodules")
  FetchContent_GetProperties("jrl-cmakemodules" SOURCE_DIR JRL_CMAKE_MODULES)
endif()

# JRL-cmakemodule setup
include("${JRL_CMAKE_MODULES}/base.cmake")
include("${JRL_CMAKE_MODULES}/python.cmake")

# Project definition
compute_project_args(PROJECT_ARGS LANGUAGES CXX)
project(${PROJECT_NAME} ${PROJECT_ARGS})
check_minimal_cxx_standard(14 ENFORCE)

# Project dependencies
if(BUILD_PYTHON_INTERFACE)
  set(PYTHON_COMPONENTS Interpreter Development.Module)
  findpython()
  string(REGEX REPLACE "-" "_" PY_NAME ${PROJECT_NAME})
  set(${PY_NAME}_INSTALL_DIR ${PYTHON_SITELIB}/${PY_NAME})
endif()

find_package(pybind11 QUIET)

if(NOT pybind11_FOUND)
  FetchContent_Declare("pybind11"
                       GIT_REPOSITORY "https://github.com/pybind/pybind11.git")
  FetchContent_MakeAvailable("pybind11")
endif()

# Main Library
set(${PROJECT_NAME}_HEADERS include/${HEADER_DIR}/adder.hpp)

set(${PROJECT_NAME}_SOURCES src/adder.cpp)

add_library(${PROJECT_NAME} SHARED ${${PROJECT_NAME}_SOURCES}
                                   ${${PROJECT_NAME}_HEADERS})
target_include_directories(${PROJECT_NAME} PUBLIC $<INSTALL_INTERFACE:include>)

if(SUFFIX_SO_VERSION)
  set_target_properties(${PROJECT_NAME} PROPERTIES SOVERSION ${PROJECT_VERSION})
endif()

# Main Executable
set(${PROJECT_NAME}_EXE cmeel-add)
add_executable(${${PROJECT_NAME}_EXE} src/main.cpp)
target_link_libraries(${${PROJECT_NAME}_EXE} ${PROJECT_NAME})

if(UNIX)
  get_relative_rpath(${CMAKE_INSTALL_BINDIR} ${PROJECT_NAME}_INSTALL_RPATH)
  set_target_properties(
    ${${PROJECT_NAME}_EXE} PROPERTIES INSTALL_RPATH
                                      "${${PROJECT_NAME}_INSTALL_RPATH}")
endif()

# Python Bindings
if(BUILD_PYTHON_INTERFACE)
  add_subdirectory(python)
endif()

# Unit tests
add_subdirectory(tests)

# Installation
install(
  TARGETS ${PROJECT_NAME}
  EXPORT ${TARGETS_EXPORT_NAME}
  DESTINATION ${CMAKE_INSTALL_LIBDIR})
install(TARGETS ${${PROJECT_NAME}_EXE}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
install(FILES package.xml DESTINATION share/${PROJECT_NAME})
