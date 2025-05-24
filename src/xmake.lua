add_requires("pybind11")

target("three_body")
    set_kind("shared")
    add_files("three_body.cpp")
    add_packages("pybind11")
    set_languages("cxx17")

    -- 自动处理 Python 扩展的命名（Linux: .so, Windows: .pyd）
    add_rules("python.library")


    set_basename("three_body")
	after_build(function (target)
    local targetfile = target:targetfile()  -- 获取实际构建出的文件路径
    local python_dir = "$(projectdir)/python"  -- 指向项目根目录下的 python 文件夹
	
	os.cp(targetfile, python_dir)
    print("Copied %s to %s", targetfile, python_dir)
end)
