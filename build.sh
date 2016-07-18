rm -rf release

mkdir release
cd ./release
mkdir bin
mkdir nativeapps
mkdir nativeapps_test
cd ..


cp -r ./aliyun ./release/nativeapps
cp  aliyungateway.py ./release/nativeapps
chmod -R 777 ./release
