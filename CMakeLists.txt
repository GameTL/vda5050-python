# This CMake is to define the Python Wheel Build. Build the PyBind extension module, decide which subprojects to pull in, built it and pull into the python package
# Require CMake 3.15+ (matching scikit-build-core) Use new versions of all
# policies up to CMake 4.0
cmake_minimum_required(VERSION 3.15...4.0)

# Scikit-build-core sets these values for you, or you can just hard-code the
# name and version.
project(
  ${SKBUILD_PROJECT_NAME}
  VERSION ${SKBUILD_PROJECT_VERSION}
  LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# Find pybind11 and Python
find_package(pybind11 CONFIG REQUIRED)
add_subdirectory(src/vda5050/vda5050_core)

# Add a library using FindPython's tooling (pybind11 also provides a helper like
# this)
pybind11_add_module(_core 
src/vda5050/_core.cpp
src/vda5050/vda5050_core/python/src/rmf_migration.cpp # dependancy of _core.cpp
)

target_link_libraries(_core PRIVATE 
pybind11::headers
vda5050_core::client
vda5050_core::execution
vda5050_core::transport
vda5050_core::types
vda5050_core::master
)
target_include_directories(_core PRIVATE src/vda5050/vda5050_core/python/include
)

# This is passing in the version as a define just as an example
target_compile_definitions(_core PRIVATE VERSION_INFO=${PROJECT_VERSION})

# The install directory is the output (wheel) directory
install(TARGETS _core DESTINATION vda5050)
install(TARGETS 
  vda5050_client
  vda5050_execution
  vda5050_transport 
  vda5050_order_utils 
  vda5050_logger
  vda5050_layout
  vda5050_master
  LIBRARY DESTINATION vda5050
  RUNTIME DESTINATION vda5050
  )

# macOS uses @loader_path; Linux ELF uses $ORIGIN so packaged .so/.dylib siblings resolve.
if(APPLE)
  set(_vda5050_rpath "@loader_path")
elseif(UNIX)
  set(_vda5050_rpath "$ORIGIN")
endif()
if(DEFINED _vda5050_rpath)
  set_target_properties(_core PROPERTIES
    BUILD_WITH_INSTALL_RPATH ON
    INSTALL_RPATH "${_vda5050_rpath}"
    BUILD_RPATH "${_vda5050_rpath}"
  )
endif()
if(APPLE)
  set_target_properties(_core PROPERTIES MACOSX_RPATH ON)
endif()


# add_subdirectory(src/vda5050)
# target_link_libraries(_core PRIVATE vda5050_core::)
