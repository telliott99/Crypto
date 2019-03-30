#! /bin/bash

desktop=~/Desktop
src=~/Dropbox/Github/Crypto/AES-math/code

mkdir $desktop/tmp
dst=$desktop/tmp

# pwd   # $desktop
cp $src/*.py $dst
cp $src/g3.tables/*.txt $dst

# ls $dst
cd $dst
echo "starting test.py"
python test.py

retval=$?
if [ $retval -ne 0 ]; then
  echo "test failed"
  exit 1
else 
  echo "test finished with no errors"
  cd ..
fi

rm -rf $dst
