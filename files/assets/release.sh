#!/bin/bash

cd ../../

rm -rf release >/dev/null 2>&1

if [ ! -f files/arm/mtk-su ] || [ ! -f files/arm64/mtk-su ] ; then
	echo "Missing mtk-su binaries in files/"
	exit 1
fi

mkdir release
mkdir release/files

cp files/assets/{MTK-SU.bat,MTK-SU.sh} release/
chmod a+x release/*.sh

cp -r files/{arm,arm64,common} release/files/
chmod a+x release/files/common/*.sh
dos2unix release/files/common/*.sh

cp {mtk-su.py,README.md,LICENSE} release/