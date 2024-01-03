from .command_builder import cmake_call_builder, builder, todo


# cmake argument keyword
class CMakeArgumentKeyword:
    def __init__(self, flag) -> None:
        self._FLAG = flag

    def __str__(self) -> str:
        return self._FLAG


CMAKE_PRIVATE = CMakeArgumentKeyword("PRIVATE")
CMAKE_VERSION = CMakeArgumentKeyword("VERSION")
CMAKE_CACHE = CMakeArgumentKeyword("CACHE")
CMAKE_BOOL = CMakeArgumentKeyword("BOOL")
CMAKE_FILEPATH = CMakeArgumentKeyword("FILEPATH")
CMAKE_PATH = CMakeArgumentKeyword("PATH")
CMAKE_STRING = CMakeArgumentKeyword("STRING")
CMAKE_INTERNAL = CMakeArgumentKeyword("INTERNAL")
CMAKE_LANGUAGES = CMakeArgumentKeyword("LANGUAGES")
CMAKE_CXX = CMakeArgumentKeyword("CXX")
CMAKE_ON = CMakeArgumentKeyword("ON")
CMAKE_REQUIRED = CMakeArgumentKeyword("REQUIRED")
CMAKE_STREQUAL = CMakeArgumentKeyword("STREQUAL")
CMAKE_STATIC = CMakeArgumentKeyword("STATIC")
CMAKE_SHARED = CMakeArgumentKeyword("SHARED")
CMAKE_NOT = CMakeArgumentKeyword("NOT")


# cmake command building
@cmake_call_builder
def cmake_call(custom_fn_name, *args):
    pass


@builder
def cmake_project(project_name):
    pass


@builder
def cmake_cmake_minimum_required(VERSION_KEYWORD, min_ver):
    pass


@builder
def cmake_add_executable(exe_name, *args):
    pass


@builder
def cmake_add_library(lib_name, *args):
    pass


@builder
def cmake_target_sources(target_name, scope_specifier, *sources):
    pass


@builder
def cmake_target_link_libraries(target_name, *libs):
    pass


@builder
def cmake_target_link_directories(target_name, *dirs):
    pass


@builder
def cmake_target_include_directories(target_name, *inc_dirs):
    pass


@builder
def cmake_target_compile_definitions(target_name, *defs):
    pass


@builder
def cmake_set(variable_name, *args):
    pass


@builder
def cmake_option(variable_name, help_string, value):
    pass


@builder
def cmake_find_package(package_name, *args):
    pass


@builder
def cmake_include(path, *args):
    pass


@todo
def cmake_add_subdirectory(sub_dir):
    pass


@builder
def cmake_if(*args):
    pass


@builder
def cmake_else():
    pass


@builder
def cmake_elseif(*args):
    pass


@builder
def cmake_endif():
    pass


# del the unrelevant names
del cmake_call_builder, builder, todo
