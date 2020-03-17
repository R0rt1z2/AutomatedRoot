#!/system/bin/sh

ARCH=`getprop ro.product.cpu.abi` # ARCH (i.e: armeabi-v7a, arm64-v8a, mips, etc...)

# Define the files that we are going to delete.
ROOT_FILES_64="
system/xbin/su
system/xbin/daemonsu
system/xbin/supolicy
system/lib/libsupol.so
system/lib64/libsupol.so
system/bin/app_process_init
system/bin/app_process64
system/bin/app_process64_original
system/bin/app_process"

ROOT_FILES_32="
system/xbin/su
system/xbin/daemonsu
system/xbin/supolicy
system/lib/libsupol.so
system/bin/app_process_init
system/bin/app_process
system/bin/app_process32_original"

# Mount system as read-write.
mount -o remount -rw /system

# Delete the root files.
echo "[?] Deleting su files..."
if [ "$ARCH" == "arm64-v8a" ]; then
   rm $ROOT_FILES_64
elif [ "$ARCH" == "armeabi-v7a" ]; then
   rm $ROOT_FILES_32
fi

# Restore original app_process.
echo "[?] Restoring original app_process..."
if [ "$ARCH" == "arm64-v8a" ]; then
   mv /system/bin/app_process_original /system/bin/app_process
   mv /system/bin/app_process_original32 /system/bin/app_process32 
   mv /system/bin/app_process_original64 /system/bin/app_process64
elif [ "$ARCH" == "armeabi-v7a" ]; then
   mv /system/bin/app_process_original /system/bin/app_process
   mv /system/bin/app_process_original32 /system/bin/app_process32 
fi

# Set correct permissions to app_process to satisfy SELinux.
chcon u:object_r:zygote_exec:s0 /system/bin/app_process32
chcon u:object_r:system_file:s0 /system/bin/app_process
if [ "$ARCH" == "arm64-v8a" ]; then
   chcon u:object_r:zygote_exec:s0 /system/bin/app_process64
fi

# Mount system as read-only.
mount -o remount -ro /system

echo "[+] Unroot complete!"
exit