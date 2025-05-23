# 查找 pybind11（由 vcpkg 安装并集成）
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(three_body
  three_body.cpp
)

target_include_directories(three_body
  PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
)

# 设置 C++17 标准
target_compile_features(three_body PUBLIC cxx_std_17)

