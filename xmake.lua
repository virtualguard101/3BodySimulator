-- xmake.lua
add_rules("mode.debug", "mode.release")

-- 设置项目信息
set_project("3BodySimulator")
set_version("1.0.0")

-- 设置默认构建模式
set_defaultmode("release")

-- 配置目标编译语言为 C++
set_languages("cxx17")

-- 添加 src 子目录，里面应该也有 xmake.lua
includes("src")
