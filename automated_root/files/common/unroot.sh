#!/system/bin/sh
BOOLESS=1
ROOT_FILES_64="
system/xbin/su
system/xbin/daemonsu
system/xbin/supolicy
system/lib/libsupol.so
system/lib64/libsupol.so
system/bin/app_process_init
system/bin/app_process64
system/bin/app_process"
ROOT_FILES_32="
system/xbin/su
system/xbin/daemonsu
system/xbin/supolicy
system/lib/libsupol.so
system/bin/app_process_init
system/bin/app_process"

if [ "$(getprop ro.product.cpu.abi)" == "arm64-v8a" ]; 
  then
     ARCH="arm64"
elif [ "$(getprop ro.product.cpu.abi)" == "armeabi-v7a" ]; 
  then
     ARCH="arm"
fi

mount -o remount -rw /system
if [ $? -eq 0 ] && [ ! -d "/sdcard/init.d" ]; then
  if [ ! -f "/system/xbin/su" ];
    then
      echo "Failed\nDevice not rooted"
      exit 1
  fi

  if [ "$ARCH" == "arm64" ]; 
    then
      rm $ROOT_FILES_64 > /dev/null 2>&1
  elif [ "$ARCH" == "arm" ]; 
    then
      rm $ROOT_FILES_32 > /dev/null 2>&1
  fi

  if [ "$ARCH" == "arm64" ]; 
    then
     mv /system/bin/app_process_original32 /system/bin/app_process32 > /dev/null 2>&1
     mv /system/bin/app_process_original64 /system/bin/app_process64 > /dev/null 2>&1
     ln /system/bin/app_process64 /system/bin/app_process > /dev/null 2>&1
  elif [ "$ARCH" == "arm" ]; 
    then
     mv /system/bin/app_process_original /system/bin/app_process > /dev/null 2>&1
     mv /system/bin/app_process_original32 /system/bin/app_process32 > /dev/null 2>&1
     ln /system/bin/app_process32 /system/bin/app_process > /dev/null 2>&1
  fi

  chcon u:object_r:zygote_exec:s0 /system/bin/app_process32 > /dev/null 2>&1
  chcon u:object_r:system_file:s0 /system/bin/app_process > /dev/null 2>&1
  chcon u:object_r:zygote_exec:s0 /system/bin/app_process64 > /dev/null 2>&1
else
  if [ ! -f "/sdcard/init.d/bin/mtk-su" ];
    then
      echo "Failed\nDevice not rooted"
      exit 1
  else
    rm -rf /sdcard/init.d > /dev/null 2>&1
  fi
fi

echo "All good"
exit 0