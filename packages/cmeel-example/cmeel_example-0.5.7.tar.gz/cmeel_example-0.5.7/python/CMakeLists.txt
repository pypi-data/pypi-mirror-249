set(${PY_NAME}_SOURCES module.cpp)

python3_add_library(${PY_NAME} MODULE WITH_SOABI ${${PY_NAME}_SOURCES})
target_link_libraries(${PY_NAME} PUBLIC ${PROJECT_NAME})
target_link_libraries(${PY_NAME} PRIVATE pybind11::pybind11)
set_target_properties(${PY_NAME} PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PY_NAME})
if(UNIX)
  get_relative_rpath(${${PY_NAME}_INSTALL_DIR} ${PY_NAME}_INSTALL_RPATH)
  set_target_properties(${PY_NAME} PROPERTIES INSTALL_RPATH
                                              "${${PY_NAME}_INSTALL_RPATH}")
endif()
install(TARGETS ${PY_NAME} DESTINATION ${${PY_NAME}_INSTALL_DIR})

set(${PY_NAME}_PYTHON __init__.py mult.py)

foreach(python ${${PY_NAME}_PYTHON})
  python_install_on_site(${PY_NAME} ${python})
endforeach()
