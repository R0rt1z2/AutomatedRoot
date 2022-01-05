#!/system/bin/sh

CHECK="/data/local/tmp/.check"

if [ "$(getprop ro.product.cpu.abi)" == "arm64-v8a" ]; 
  then
     ARCH="arm64"
elif [ "$(getprop ro.product.cpu.abi)" == "armeabi-v7a" ]; 
  then
     ARCH="arm"
fi

mkdir -p {/sdcard/init.d,/sdcard/init.d/bin} > /dev/null 2>&1
cp -r /data/local/tmp/magisk-boot.sh /sdcard/init.d/ > /dev/null 2>&1
cp -r /data/local/tmp/${ARCH}/{mtk-su,magiskinit} /sdcard/init.d/bin > /dev/null 2>&1

am start com.ryosoftware.initd/.PreferencesActivity > /dev/null 2>&1
logcat | grep -E --line-buffered 'retcode 0' | while read line; do touch $CHECK; done &

while [ 1 == 1 ]
do
   ls $CHECK > /dev/null 2>&1
   if [ "$?" -eq 0 ]; then
	  rm $CHECK; logcat -c; break
   fi
done

am start com.topjohnwu.magisk/a.c > /dev/null 2>&1

echo "All good"