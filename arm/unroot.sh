##########################################################################################
# Unroot Script
##########################################################################################

# Define the files that we are going to delete.
ROOT_FILES="
system/xbin/su
system/xbin/daemonsu
system/xbin/supolicy
system/lib/libsupol.so
"
# Mount system as read-write.
mount -o remount -rw /system

# Delete the root files.
rm $ROOT_FILES

# Mount system as read-ony.
mount -o remount -ro /system
