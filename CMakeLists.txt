cmake_minimum_required(VERSION 3.10)
project(KF-GINS)

set(CMAKE_CXX_STANDARD 14)

# 设置编译的可执行文件存放位置： ./bin
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
# 设置库可执行文件存放位置 ./lib
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

# 这段没看懂，知道是设置编译选项，但MSVC， STREQUAL 等等是什么？
if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
    add_definitions( -D_USE_MATH_DEFINES=True)
    add_compile_options("$<$<C_COMPILER_ID:MSVC>:/utf-8>")
    add_compile_options("$<$<CXX_COMPILER_ID:MSVC>:/utf-8>")
else()
    set(CMAKE_CXX_FLAGS "-Wno-unused-result")
endif()

# 全局搜索源文件，并定义为source.
file(GLOB_RECURSE SOURCE
        src/kf_gins.cpp
        src/fileio/fileloader.cc
        src/fileio/filesaver.cc
        src/kf-gins/gi_engine.cpp
        src/kf-gins/insmech.cpp)

# include directory 和之前的 SOURCE 是什么关系 ？ include directory 的作用？
include_directories(${PROJECT_SOURCE_DIR}/src)

# 由此可以推测：定义SOURCE实际上是简化了添加可执行文件的代码
add_executable(${PROJECT_NAME} ${SOURCE} src/kf-gins/kf_gins_types.h src/fileio/gnssfileloader.h src/common/types.h src/common/angle.h src/fileio/imufileloader.h src/kf-gins/gi_engine.h)

# Eigen3
include_directories(ThirdParty/eigen-3.3.9)

# yaml-cpp-0.7.0
add_subdirectory(ThirdParty/yaml-cpp-0.7.0)
target_link_libraries(${PROJECT_NAME} yaml-cpp)

# abseil
set(ABSL_PROPAGATE_CXX_STD true)
add_subdirectory(ThirdParty/abseil-cpp-20220623.1)
target_link_libraries(${PROJECT_NAME}
        absl::strings
        absl::str_format
        absl::time)

# abseil 库是干嘛用的 ？ 标准库的扩展 ？
