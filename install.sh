
# Remove old Release
rm -rf Release

# Check if path includes conda's python 2.7
PY_INT=$(which python)
if [[ $PY_INT == *"anaconda2"* ]]; then
  echo "Anaconda Python 2 detected, using location: $PY_INT"
  CONDA_HOME=$(dirname $(dirname $PY_INT))
else
  echo "Anaconda Python 2 not detected, prepending anaconda2 to PATH variable"
  export export PATH="/home/$USER/anaconda2/bin:$PATH"
  PY_INT=$(which python)
  printf "Testing which python:\n$PY_INT\n"
  if [[ $PY_INT != *"anaconda2"* ]]; then
    echo "Looks like you don't have Anaconda Python 2.7"
    echo "Will use system default, but may have issues"
    CONDA_HOME=false
  else
    echo "Anaconda Python 2 found!"
    CONDA_HOME=$(dirname $(dirname $PY_INT))
  fi
fi

mkdir Release && cd Release

if [ "$CONDA_HOME" != false ]; then
  cmake -D CMAKE_BUILD_TYPE=Release ..\
    -DPYTHON_LIBRARY=$CONDA_HOME/lib/libpython2.7.so \
    -DPYTHON_INCLUDE_DIR=$CONDA_HOME/include/python2.7 \
    -DPYTHON_EXECUTABLE=$CONDA_HOME/bin/python
else
  cmake -D CMAKE_BUILD_TYPE=Release ..
fi

make
cd ..
