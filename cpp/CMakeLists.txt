cmake_minimum_required(VERSION 3.15)
project(twocascade_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Default to Release build if not specified
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
endif()

# Set specific flags for Debug (with sanitizers per §5.5).
# NOTE: ASan is disabled on macOS — Apple Clang 17's ASan runtime deadlocks in
# its own initializer (re-entrant malloc during shadow-memory setup) on
# macOS 26.5, hanging every binary before main(). Verified 2026-06-11 via
# /usr/bin/sample; MallocNanoZone=0 does not help. UBSan still works.
# Full ASan coverage should be obtained on Linux (PACE / CI).
if(APPLE)
    set(CMAKE_CXX_FLAGS_DEBUG "-O0 -g -fsanitize=undefined")
    set(CMAKE_EXE_LINKER_FLAGS_DEBUG "-fsanitize=undefined")
else()
    set(CMAKE_CXX_FLAGS_DEBUG "-O0 -g -fsanitize=address,undefined")
    set(CMAKE_EXE_LINKER_FLAGS_DEBUG "-fsanitize=address,undefined")
endif()

# Option for native CPU architecture optimizations (disable on PACE)
option(USE_NATIVE_MARCH "Enable native CPU optimization" ON)
if(USE_NATIVE_MARCH)
    include(CheckCXXCompilerFlag)
    if(APPLE)
        check_cxx_compiler_flag("-mcpu=native" HAS_MCPU_NATIVE)
        if(HAS_MCPU_NATIVE)
            add_compile_options(-mcpu=native)
        endif()
    else()
        check_cxx_compiler_flag("-march=native" HAS_MARCH_NATIVE)
        if(HAS_MARCH_NATIVE)
            add_compile_options(-march=native)
        endif()
    endif()
endif()

# Help Apple Clang find Homebrew's libomp on Apple Silicon.
# These hint variables must be set BEFORE find_package(OpenMP) to have any effect,
# and only when libomp is actually installed (otherwise the hardcoded path breaks the link).
if(APPLE AND CMAKE_CXX_COMPILER_ID MATCHES "Clang" AND EXISTS "/opt/homebrew/opt/libomp/lib/libomp.dylib")
    set(OpenMP_CXX_FLAGS "-Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include")
    set(OpenMP_CXX_LIB_NAMES "omp")
    set(OpenMP_omp_LIBRARY "/opt/homebrew/opt/libomp/lib/libomp.dylib")
endif()

# Find OpenMP (optional — build degrades to single-threaded without it)
find_package(OpenMP)

# Define twocascade core library
add_library(twocascade_core src/engine.cpp)
target_include_directories(twocascade_core PUBLIC include)
if(OpenMP_CXX_FOUND)
    target_link_libraries(twocascade_core PUBLIC OpenMP::OpenMP_CXX)
endif()

# Thin main CLI wrapper
add_executable(twocascade_run src/main.cpp)
target_link_libraries(twocascade_run PRIVATE twocascade_core)

# Test executable (we will use a custom TEST_ASSERT macro to avoid NDEBUG stripping)
add_executable(test_engine tests/test_engine.cpp)
target_link_libraries(test_engine PRIVATE twocascade_core)

# CTest integration
enable_testing()
add_test(NAME engine COMMAND test_engine)