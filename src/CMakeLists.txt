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

# 把生成的共享库 (.so/.pyd) 放到 ../python 目录
set_target_properties(three_body PROPERTIES
  LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/python
  OUTPUT_NAME "three_body"    # 忽略 ABI tag，统一输出 three_body.so
  PREFIX ""                   # 无前缀
  SUFFIX ".so"                # 强制后缀 .so
)
