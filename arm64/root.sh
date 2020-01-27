##########################################################################################
# Root Script
##########################################################################################

# Get the device props
BRAND=`getprop ro.product.brand` # Brand (i.e: Asus, bq, Amazon, etc...)
DEVICE=`getprop ro.product.device` # Product model (i.e: suez, douglas, etc...)

# If device is amazon-branded check the FireOS version
if [ $BRAND == "Amazon" ]; then
    echo "This is an Amazon Device..."
	echo "Checking FireOS version..."
	FOS_VER=`getprop ro.build.version.name | awk -F"[()]" '{print $2}'`
	FOS_NUMBER=`getprop ro.build.version.fireos`
    echo "Your device seems to be in FireOS $FOS_VER"
	if [ $DEVICE == "suez" ] || [ $DEVICE == "douglas" ] && [ $FOS_VER -gt 636558520 ]; then
	   echo "FireOS 5.6.4.0 build 636558520 and up are not supported in Fire 7th gen devices!"
    fi
	elif [ $DEVICE == "giza" ] && [ $FOS_VER -gt 626533320 ] &&; then
	   echo "FireOS 5.3.6.4 build 626533320 and up are not supported in Fire 6th gen devices!"
    fi
	elif [ $DEVICE == "sloane" ] && [ $FOS_NUMBER -gt "5.2.2.0" ]; then
	   echo "FireOS 5.2.2.0 and up are not supported in Fire TV 2 (2015)!"
    fi
	elif [ $DEVICE == "karnak" ] && [ $FOS_NUMBER -gt "6.3.0.1" ]; then
	   echo "FireOS 6.3.0.1 and up are not supported in Fire HD8 (2018)!"
    fi
	elif [ $DEVICE == "maverick" ] && [ $FOS_NUMBER -gt "7.3.1.0" ]; then
	   echo "FireOS 7.3.1.0 and up are not supported in Fire HD10 (2019)!"
    fi
	elif [ $DEVICE == "mustang" ] && [ $FOS_NUMBER -gt "6.3.1.2" ]; then
	   echo "FireOS 7.3.1.0 and up are not supported in Fire 7 (2019)!"
    fi
fi	

# Mount system read-write.
mount -o remount -rw /system

# Backup stock app_process.
cp /system/bin/app_process /system/bin/app_process_original
cp /system/bin/app_process32 /system/bin/app_process_original32
cp /system/bin/app_process64 /system/bin/app_process_original64

# Copy su files.
cp /data/local/tmp/su /system/xbin/su
mv /data/local/tmp/su /system/xbin/daemonsu
cp /data/local/tmp/supolicy /system/xbin/
cp /data/local/tmp/libsupol.so /system/lib/
cp /data/local/tmp/libsupol.so /system/lib64/

# Set correct permissions.
chmod 0755 /system/xbin/su
chcon u:object_r:system_file:s0 /system/xbin/su
chmod 0755 /system/xbin/daemonsu
chcon u:object_r:system_file:s0 /system/xbin/daemonsu

# Start the daemon.
daemonsu --auto-daemon

# Start SuperSU app.
am start -a android.intent.action.MAIN -n eu.chainfire.supersu/.MainActivity
