add_unit_test(add add.cpp)
target_link_libraries(add ${PROJECT_NAME})

add_test(NAME exe-fail COMMAND ${CMAKE_BINARY_DIR}/${${PROJECT_NAME}_EXE} 3 4)

if(BUILD_PYTHON_INTERFACE)
  add_subdirectory(python)
endif()
