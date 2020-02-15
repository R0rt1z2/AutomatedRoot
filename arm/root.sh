##########################################################################################
# Root Script
##########################################################################################

# Get the device props
BRAND=`getprop ro.product.brand` # Brand (i.e: Asus, bq, Amazon, etc...)
DEVICE=`getprop ro.product.device` # Product model (i.e: suez, douglas, etc...)
HARDWARE=`getprop ro.hardware` # CPU (i.e: mt8163, mt8173, mt6735, etc...)

# If device is "amazon-branded" check the FireOS version
if [ $BRAND == "Amazon" ]; then
    echo "This is an Amazon Device..."
    echo "Checking FireOS version..."
    FOS_VER=`getprop ro.build.version.name | awk -F"[()]" '{print $2}'`
    FOS_NUMBER=`getprop ro.build.version.fireos`
    echo "Your device seems to be in FireOS $FOS_VER"
    if [ $DEVICE == "suez" ] || [ $DEVICE == "douglas" ] && [ $FOS_VER -gt "636558520" ]; then
	   echo "FireOS 5.6.4.0 build 636558520 and up are not supported in Fire 7th gen devices!"
    elif [ $DEVICE == "giza" ] && [ $FOS_VER -gt 626533320 ]; then
	   echo "FireOS 5.3.6.4 build 626533320 and up are not supported in Fire 6th gen devices!"
    elif [ $DEVICE == "sloane" ] && [ $FOS_NUMBER -gt "5.2.2.0" ]; then
	   echo "FireOS 5.2.2.0 and up are not supported in Fire TV 2 (2015)!"
    elif [ $DEVICE == "karnak" ] && [ $FOS_NUMBER -gt "6.3.0.1" ]; then
	   echo "FireOS 6.3.0.1 and up are not supported in Fire HD8 (2018)!"
    elif [ $DEVICE == "maverick" ] && [ $FOS_NUMBER -gt "7.3.1.0" ]; then
	   echo "FireOS 7.3.1.0 and up are not supported in Fire HD10 (2019)!"
    elif [ $DEVICE == "mustang" ] && [ $FOS_NUMBER -gt "6.3.1.2" ]; then
	   echo "FireOS 6.3.1.2 and up are not supported in Fire 7 (2019)!"
    fi
fi

# Check if dm-veruty is present..
VERITY=`cat /fstab.$HARDWARE* | grep system | grep -oh "\w*verify\w*"` # Search for the "verify" flag in system mount line

if [ "$VERITY" == "" ]; then
   echo "Warning: Reached EOF without any verify flag."
   echo "Warning: Attempt to cat fstab in vendor!"
   VERITY=`cat /vendor/etc/fstab.$HARDWARE* | grep system | grep -oh "\w*verify\w*"` # Search for the "verify" flag in system mount line
fi

if [ "$VERITY" == "verify" ]; then
    echo "DM-Verity is present in this device. Abort!"
    exit
else
    echo "DM-Verity is not present in this device. Continue..."
fi

# Mount system read-write.
mount -o remount -rw /system

# Backup stock app_process.
cp /system/bin/app_process /system/bin/app_process_original
cp /system/bin/app_process32 /system/bin/app_process_original32

# Copy su files.
cp /data/local/tmp/su /system/xbin/su
mv /data/local/tmp/su /system/xbin/daemonsu
cp /data/local/tmp/supolicy /system/xbin/
cp /data/local/tmp/libsupol.so /system/lib/

# Set correct permissions.
chmod 0755 /system/xbin/su
chcon u:object_r:system_file:s0 /system/xbin/su
chmod 0755 /system/xbin/daemonsu
chcon u:object_r:system_file:s0 /system/xbin/daemonsu

# Start the daemon.
daemonsu --auto-daemon

# Start SuperSU app.
am start -a android.intent.action.MAIN -n eu.chainfire.supersu/.MainActivity
