#!/bin/bash

[[ -d release ]] && rm -rf release

RELEASE_DIRECTORY=release/usr/nativeapps

mkdir -p ${RELEASE_DIRECTORY}

cp -a aliyun ${RELEASE_DIRECTORY}
cp aliyungateway.py ${RELEASE_DIRECTORY}

chmod -R 777 release
