#!/system/bin/sh

readlink -f /vendor | grep system > /dev/null 2>&1

if [ $? -eq 1 ]; then
   HAS_VENDOR="YES"
fi

if [ "$(getprop ro.product.cpu.abi)" == "arm64-v8a" ]; 
  then
     ARCH="arm64"
elif [ "$(getprop ro.product.cpu.abi)" == "armeabi-v7a" ]; 
  then
     ARCH="arm"
fi

if [ "$HAS_VENDOR" -eq "YES" ]; then
   cat /vendor/etc/fstab* 2>/dev/null | grep verify | grep system > /dev/null 2>&1
   if [ $? -eq 0 ]; then
       echo "Failed\nDevice uses dm-verity"
       exit 1
   else
       cat /fstab* 2>/dev/null | grep verify | grep system > /dev/null 2>&1
       if [ $? -eq 0 ]; then
           echo "Failed\nDevice uses dm-verity"
           exit 1
       fi
   fi
else
   cat /fstab* 2>/dev/null | grep verify | grep system > /dev/null 2>&1
   if [ $? -eq 0 ]; then
        echo "Failed\nDevice uses dm-verity"
        exit 1
   fi
fi

mount -o remount -rw /system > /dev/null 2>&1

cp /system/bin/app_process /system/bin/app_process_original > /dev/null 2>&1
cp /system/bin/app_process32 /system/bin/app_process_original32 > /dev/null 2>&1
cp /system/bin/app_process64 /system/bin/app_process_original64 > /dev/null 2>&1

if [ "$ARCH" == "arm64" ]; 
  then
    cp /data/local/tmp/arm64/su /system/xbin/su > /dev/null 2>&1
    mv /data/local/tmp/arm64/su /system/xbin/daemonsu > /dev/null 2>&1
    cp /data/local/tmp/arm64/supolicy /system/xbin/ > /dev/null 2>&1
    cp /data/local/tmp/arm64/libsupol.so /system/lib/ > /dev/null 2>&1
    cp /data/local/tmp/arm64/libsupol.so /system/lib64/ > /dev/null 2>&1
elif [ "$ARCH" == "arm" ]; 
  then
    cp /data/local/tmp/arm/su /system/xbin/su > /dev/null 2>&1
    mv /data/local/tmp/arm/su /system/xbin/daemonsu > /dev/null 2>&1
    cp /data/local/tmp/arm/supolicy /system/xbin/ > /dev/null 2>&1
    cp /data/local/tmp/arm/libsupol.so /system/lib/ > /dev/null 2>&1
fi

chmod 0755 /system/xbin/su  > /dev/null 2>&1
chcon u:object_r:system_file:s0 /system/xbin/su  > /dev/null 2>&1
chmod 0755 /system/xbin/daemonsu > /dev/null 2>&1
chcon u:object_r:system_file:s0 /system/xbin/daemonsu  > /dev/null 2>&1

daemonsu --auto-daemon  > /dev/null 2>&1

rm -rf /data/local/tmp/${ARCH}  > /dev/null 2>&1
rm /data/local/tmp/*.sh  > /dev/null 2>&1

echo "All good"

exit 0