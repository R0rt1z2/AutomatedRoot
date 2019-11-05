##########################################################################################
# Root Script
##########################################################################################

# Mount system read-write.
mount -o remount -rw /system

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

# Mount system read-only.
mount -o remount -ro /system

# Start SuperSU app.
am start -a android.intent.action.MAIN -n eu.chainfire.supersu/.MainActivity
