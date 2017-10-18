PYTHON3_VERSION=`python3 --version | cut -d " " -f2`
PYTHON3_LIBRARY=`find /usr/local/Cellar/python3/$PYTHON3_VERSION/ -iname libpython3.6m.dylib`

# get the first result
PYTHON3_LIBRARY=$PYTHON3_LIBRARY | cut -d " " -f1
PYTHON3_INCLUDE_DIR=`find /usr/local/Cellar/python3/$PYTHON3_VERSION/ -iname include`

cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D PYTHON3_LIBRARY=$PYTHON3_LIBRARY \
    -D PYTHON3_INCLUDE_DIR=$PYTHON3_INCLUDE_DIR \
    -D PYTHON3_EXECUTABLE=$VIRTUAL_ENV/bin/python \
    -D BUILD_opencv_python2=OFF \
    -D BUILD_opencv_python3=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=ON ..
