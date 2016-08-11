rm -rf release

mkdir release
cd ./release
mkdir -p ./usr/bin
mkdir -p ./usr/nativeapps
mkdir -p ./usr/nativeapps_test
cd ..


cp -r ./aliyun ./release/usr/nativeapps
cp  aliyungateway.py ./release/usr/nativeapps
chmod -R 777 ./release
