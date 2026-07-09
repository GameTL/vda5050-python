find_package(ament_cmake_python REQUIRED)
find_package(Python3 COMPONENTS Development REQUIRED)
find_package(pybind11 REQUIRED)

pybind11_add_module(_core
  src/rmf_migration.cpp
)

target_link_libraries(_core
  PRIVATE
    Python3::Python
    vda5050_core::client
)

target_include_directories(_core
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

install(
  TARGETS _core
  DESTINATION lib/python${Python3_VERSION_MAJOR}.${Python3_VERSION_MINOR}/site-packages
)
