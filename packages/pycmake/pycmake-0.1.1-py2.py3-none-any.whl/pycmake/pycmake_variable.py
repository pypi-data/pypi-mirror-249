import os
from . import input_args
from . import cmake_variable

# pycmake variables
PY_CMAKE_LISTS_FILE_NAME = "CMakeLists.txt"
PY_CMAKE_LISTS_PATH = os.path.join(
    cmake_variable.CMAKE_CURRENT_SOURCE_DIR, PY_CMAKE_LISTS_FILE_NAME
)

PY_CMAKE_CONFIGURE_ARGS = ""
if input_args.args.configure:
    for ua in input_args.unknown_args:
        PY_CMAKE_CONFIGURE_ARGS += ua
