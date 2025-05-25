#!/bin/bash
set -e

#———————————————
# 1. 清理旧构建
#———————————————
echo "清理旧构建文件..."
rm -rf build python/three_body* .venv/ vcpkg_installed/ vcpkg/

#———————————————
# 2. 创建并激活 uv 虚拟环境（Python 3.12）
#———————————————
echo "创建并激活 Python 3.12 虚拟环境..."
uv venv .venv         # 默认为系统 Python3.12
source .venv/bin/activate

# 安装 Python 可视化脚本依赖
uv pip install -r requirements.txt

#———————————————
# 3. Configure and build C++ module
#———————————————
echo "配置 CMake（指向 venv 中的 python）..."

cmake -B build \
  -DCMAKE_TOOLCHAIN_FILE=~/vcpkg/scripts/buildsystems/vcpkg.cmake \
  -DPython3_EXECUTABLE=$(which python) \
  -DCMAKE_BUILD_TYPE=Release

echo "开始编译 C++ 扩展..."
cmake --build build

#———————————————
# 4. 检查生成结果
#———————————————
echo "生成的 Python 模块："
ls -l python/ | grep three_body

#———————————————
# 5. 运行可视化脚本
#———————————————
echo "执行 uv run python/visualize.py 启动三体模拟..."
echo "执行 uv run python/dynamic.py 启动动态模拟..."
# uv run python/visualize.py

