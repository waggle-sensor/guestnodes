#!/bin/bash

set -x
set -e

# install dependencies
apt-get install -y libavcodec-dev libavformat-dev libswscale-dev python3-dev python3-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -e ${script_dir}/opencv2.tar.gz ]; then
	exit 1
fi

cd ${script_dir}
tar -zxvf opencv2.tar.gz

cd ${script_dir}/opencv2/include
cp -r * /usr/local/include

cd ${script_dir}/opencv2/lib
cp -r * /usr/local/lib

if [ -e /usr/local/lib/python3.5/dist-packages/ ]; then
	cd ${script_dir}/opencv2/python3
	cp -r * /usr/local/lib/python3.5/dist-packages/
else
	echo "No python3.5 found"
fi

echo "done"
