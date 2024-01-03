# Licensed under the GPLv3 License: https://www.gnu.org/licenses/gpl-3.0.html
# For details: https://github.com/muziing/Py2exe-GUI/blob/main/README.md#license

"""此模块包含将 PyInstaller 命令导出为 Shell 脚本的相关功能
"""

"""
进行导出时，需要指定入口脚本 my_script.py 的绝对路径

尝试向入口脚本所在目录的上层逐层寻找 git 存储库，如果找到，视有.git目录的目录为
项目根目录，记录其名称、与入口脚本的相对路径关系

用户可以在两个位置运行导出版 shell 脚本：my_script.py所在目录/项目根目录
"""

"""
脚本伪代码

if [my_script.py] not in current_working_dir:
    print("")
    exit()

if current_working_dir == [project_root_dir]:
    cd [my_script.py].Parent

try:
    run("python -c 'import pyinstaller'")
except Exception:
    print("在当前 Python 环境中找不到 PyInstaller，如项目使用了虚拟环境，请先激活虚拟环境再运行此脚本。")
    exit()

# 正式运行 PyInstaller
pyinstaller D:/Works/Py2exe-GUI/src/Py2exe-GUI.py `
     --windowed `
     --name Py2exe-GUI `
     --clean

"""
