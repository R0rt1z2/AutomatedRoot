#!/system/bin/sh

# Get the device props
BRAND=$(getprop ro.product.brand) # Brand (i.e: Asus, bq, Amazon, etc...)
DEVICE=$(getprop ro.product.device) # Product model (i.e: suez, douglas, etc...)
HARDWARE=$(getprop ro.hardware) # CPU (i.e: mt8163, mt8173, mt6735, etc...)
ARCH=$(getprop ro.product.cpu.abi) # ARCH (i.e: armeabi-v7a, arm64-v8a, mips, etc...)

# Check if the script was launched from a root shell
ID=$(id | grep uid=0\(root\))

if [ $? -eq 1 ]; then
   echo "[!] FATAL: Script wasn't launched from root id"
   exit 1
fi

VENDOR=$(readlink -f /vendor | grep system)

if [ $? -eq 1 ]; then
   echo "[?] This device has vendor partition!"
   HAS_VENDOR="YES"
fi

if [ "$HAS_VENDOR" -eq "YES" ]; then
   echo "[?] Checking fstab in vendor..."
   VERIFY=$(cat /vendor/etc/fstab* 2>/dev/null | grep verify | grep system)
   if [ $? -eq 0 ]; then
       echo "[-] DM-Verity it's present on this device. Abort!"
       exit 1
   else
       echo "[!] Couldn't find verify flag in vendor. Searching in initramfs."
       VERIFY=$(cat /fstab* 2>/dev/null | grep verify | grep system)
       if [ $? -eq 0 ]; then
           echo "[-] DM-Verity it's present on this device. Abort!"
           exit 1
       fi
       echo "[?] DM-Verity it's not enabled on this device. Continue..."
   fi
else
   echo "[?] Checking fstab in initramfs..."
   VERIFY=$(cat /fstab* 2>/dev/null | grep verify | grep system)
   if [ $? -eq 0 ]; then
        echo "[-] DM-Verity it's present on this device. Abort!"
        exit 1
   fi
   echo "[?] DM-Verity it's not enabled in this device. Continue..."
fi

# Mount system read-write.
mount -o remount -rw /system

# Backup original app_process.
cp /system/bin/app_process /system/bin/app_process_original
cp /system/bin/app_process32 /system/bin/app_process_original32
if [ "$ARCH" == "arm64-v8a" ]; then
   echo "[?] Copying 64 bit app_process..."
   cp /system/bin/app_process64 /system/bin/app_process_original64
fi

# Copy su files.
if [ "$ARCH" == "arm64-v8a" ]; then
   echo "[?] Copying 64 bit files..."
   cp /data/local/tmp/arm64/su /system/xbin/su
   mv /data/local/tmp/arm64/su /system/xbin/daemonsu 2>/dev/null
   cp /data/local/tmp/arm64/supolicy /system/xbin/
   cp /data/local/tmp/arm64/libsupol.so /system/lib/
   cp /data/local/tmp/arm64/libsupol.so /system/lib64/
elif [ "$ARCH" == "armeabi-v7a" ]; then
   echo "[?] Copying 32 bit files..."
   cp /data/local/tmp/arm/su /system/xbin/su
   mv /data/local/tmp/arm/su /system/xbin/daemonsu 2>/dev/null
   cp /data/local/tmp/arm/supolicy /system/xbin/
   cp /data/local/tmp/arm/libsupol.so /system/lib/
fi

# Set correct permissions.
echo "[?] Setting permissions..."
chmod 0755 /system/xbin/su
chcon u:object_r:system_file:s0 /system/xbin/su
chmod 0755 /system/xbin/daemonsu
chcon u:object_r:system_file:s0 /system/xbin/daemonsu

# Start the daemon.
echo "[?] Starting the daemon..."
daemonsu --auto-daemon

# Delete old files.
echo "[?] Deleting old files..."
rm -rf /data/local/tmp/arm
rm -rf /data/local/tmp/arm64
rm /data/local/tmp/root.sh

echo "[?] Now open the SuperSU app and update the binaries!"
exit 0
