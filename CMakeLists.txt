cmake_minimum_required(VERSION 3.20)
project(3BodySimulator LANGUAGES CXX)

# 使用 vcpkg 的 Toolchain
if(NOT DEFINED CMAKE_TOOLCHAIN_FILE)
  set(
    CMAKE_TOOLCHAIN_FILE "~/vcpkg/scripts/buildsystems/vcpkg.cmake"
    DPython3_EXECUTABLE=$(which python)
    DCMAKE_BUILD_TYPE=Release
    CACHE STRING ""
  )
endif()

add_subdirectory(src)

