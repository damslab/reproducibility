cmake_minimum_required(VERSION 3.16.1)
project(RapidJSONCPP)

# set clang as the default compiler
set(CMAKE_C_COMPILER "clang")
set(CMAKE_CXX_COMPILER "clang++")

# set the output directory
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_SOURCE_DIR}/bin")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${PROJECT_SOURCE_DIR}/libraries")
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${PROJECT_SOURCE_DIR}/tools/cmake")
set(CTEST_BINARY_DIRECTORY "${PROJECT_SOURCE_DIR}/bin")

# check the operating system and add the appropriate flags
if (APPLE)
    SET(CMAKE_CXX_FLAGS " -std=c++11 -g -fPIC -Wno-deprecated-declarations")
    SET(CMAKE_MODULE_LINKER_FLAGS "${CMAKE_MODULE_LINKER_FLAGS} -undefined dynamic_lookup")
elseif (UNIX AND NOT APPLE)
    SET(CMAKE_CXX_FLAGS " -std=c++11 -g -march=native -O3 -fPIC -Wno-deprecated-declarations -pthread ")
endif ()

# set the directories with the common header files
include_directories("${PROJECT_SOURCE_DIR}/src/at/tugraz/header")
include_directories("${PROJECT_SOURCE_DIR}/src/at/tugraz/Utils/header")

# set the directories with the common source files
include_directories("${PROJECT_SOURCE_DIR}/src/at/tugraz/source")
include_directories("${PROJECT_SOURCE_DIR}/src/at/tugraz/Utils/source")

# set project header files
file(GLOB header "${PROJECT_SOURCE_DIR}/src/at/tugraz/header/*.h")
file(GLOB utilsHeader "${PROJECT_SOURCE_DIR}/src/at/tugraz/Utils/header/*.h")

# set project source files
file(GLOB source "${PROJECT_SOURCE_DIR}/src/at/tugraz/source/*.cpp")
file(GLOB utilsSource "${PROJECT_SOURCE_DIR}/src/at/tugraz/Utils/source/*.cpp")

# aminer-author
add_executable(aminer-author-json
        src/at/tugraz/aminerAuthor.cpp
        ${source}
        ${header}
        ${utilsSource}
        ${utilsHeader}
        ${rapidjson}
        )
# aminer-paper
add_executable(aminer-paper-json
        src/at/tugraz/aminerPaper.cpp
        ${source}
        ${header}
        ${utilsSource}
        ${utilsHeader}
        )
## twitter
#add_executable(twitter-json
#        src/at/tugraz/twitter.cpp
#        ${source}
#        ${header}
#        ${utilsSource}
#        ${utilsHeader}
#        )
#
## twitter-throu
#add_executable(twitter-throu-json
#        src/at/tugraz/twitter-throu.cpp
#        ${source}
#        ${header}
#        ${utilsSource}
#        ${utilsHeader}
#        )

## tpch
#add_executable(tpch-json
#        src/at/tugraz/tpch.cpp
#        ${source}
#        ${header}
#        ${utilsSource}
#        ${utilsHeader}
#        )

# yelp-json
add_executable(yelp-json
        src/at/tugraz/queryEngine.cpp
        ${source}
        ${header}
        ${utilsSource}
        ${utilsHeader}
        )