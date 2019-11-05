##########################################################################################
# Root Script
##########################################################################################

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
