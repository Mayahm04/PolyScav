cmake_minimum_required(VERSION 3.10)

# 🔥 On active le C ET le C++
project(OpenGLObjects LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# GLM
find_package(glm REQUIRED)

# GLFW
find_package(PkgConfig REQUIRED)
pkg_check_modules(GLFW REQUIRED glfw3)

include_directories(
    ${GLFW_INCLUDE_DIRS}
    ${GLM_INCLUDE_DIRS}
    external/glad/include
)

link_directories(
    ${GLFW_LIBRARY_DIRS}
)

add_definitions(${GLFW_CFLAGS_OTHER})

# 🔥 Glad est en C, mais grâce à LANGUAGES C CXX, plus besoin de set_source_files_properties
add_executable(opengl_objects
    main.cpp
    external/glad/src/glad.c
)

target_link_libraries(opengl_objects
    ${GLFW_LIBRARIES}
    GL
    m
    dl
    pthread
)
