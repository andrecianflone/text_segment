
# Remove old Release
rm -rf Release

# Check if path includes conda's python 2.7
py_loc=$(which python)
if [[ $py_loc == *"anaconda2"* ]]; then
  echo "Python 2 detected, using location: $py_loc"
else
  echo "Python 2 not detected, prepending anaconda2 to PATH variable"
  export export PATH="/home/$USER/anaconda2/bin:$PATH"
  printf "Testing which python:\n$(which python)\n"
fi

py_loc=$(which python)
if [[ $py_loc != *"anaconda2"* ]]; then
  echo "Looks like you don't have Anaconda Python 2.7, exiting"
  exit 1
fi

mkdir Release && cd Release
cmake -D CMAKE_BUILD_TYPE=Release ..
make
cd ..
