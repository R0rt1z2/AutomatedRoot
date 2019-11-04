echo Start unroot process...
mount -o remount -rw /system
rm /system/xbin/su
rm /system/xbin/daemonsu
rm /system/xbin/supolicy
rm /system/lib/libsupol.so
rm /system/lib64/libsupol.so
echo Completed!
