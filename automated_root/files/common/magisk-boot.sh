#!/system/bin/sh
#
# Updated: Mar 31, 2020
# by diplomatic
#
# This script sets up bootless root with Magisk on MediaTek Android devices.
# It uses mtk-su, the temporary root tool for MediaTek ARMv8 chips. Must be run
# from the app 'init.d scripts support' by RYO Software. Put this file into
# /storage/emulated/0/init.d along with mtk-su and magiskinit into .../init.d/bin
# Point the app to run sh scripts from /storage/emulated/0/init.d at boot time.
#
# WARNING: DO NOT UPDATE MAGISK THROUGH MAGISK MANAGER OR YOU WILL BRICK YOUR
#		   DEVICE ON A LOCKED BOOTLOADER
#

HOMEDIR=/data/data/com.ryosoftware.initd/files/bin
SRCDIR=/storage/emulated/0/init.d

SU_MINISCRIPT='
# Magisk function to find boot partition and prevent the installer from finding
# it again
find_block() {
  for BLOCK in "$@"; do
    DEVICES=$(find /dev/block -type l -iname $BLOCK) 2>/dev/null
    for DEVICE in $DEVICES; do
      cd ${DEVICE%/*}
      local BASENAME="${DEVICE##*/}"
      mv "$BASENAME" ".$BASENAME"
      cd -
    done
  done
  # Fallback by parsing sysfs uevents
  typeset -l PARTNAME BLOCK
  local FILELIST=$(grep -s PARTNAME= /sys/dev/block/*/uevent) 2>/dev/null
  for uevent in $FILELIST; do
    local PARTNAME=${uevent##*PARTNAME=}
    for BLOCK in "$@"; do
      if [ "$BLOCK" = "$PARTNAME" ]; then
        local FNAME=${uevent%:*}
        chmod 0 $FNAME
      fi
    done
  done
  return 0
}

# Root only at this point; hoping selinux is permissive
if [ $(id -u) != 0 ] || [ "$(getenforce)" != "Permissive" ]; then
	echo "Root user only" >&2
	exit 1
fi

# Disaster prevention
SLOT=$(getprop ro.boot.slot_suffix)
find_block boot$SLOT

cd $HOMEDIR || { setenforce 1; exit 1; }

# Patch selinux policy
./magiskpolicy --live --magisk "allow magisk * * *"
if [ ! -f /sbin/.init-stamp ]; then
	# Set up /root links to /sbin files
	mount | grep -qF rootfs
	have_rootfs=$?
	if [ $have_rootfs -eq 0 ]; then
		mount -o rw,remount /
		mkdir -p /root
		chmod 750 /root
		if ! ln /sbin/* /root; then
			echo "Error making /sbin hardlinks" >&2
			setenforce 1
			exit 1
		fi
		mount -o ro,remount /
	fi
	# Create tmpfs /sbin overlay
	# This may crash on system-as-root with no /root directory
	./magisk -c >&2

	touch /sbin/.init-stamp

	if [ ! -f /sbin/magiskinit ] || [ ! -f /sbin/magisk ]; then
		echo "Bad /sbin mount?" >&2
		setenforce 1
		exit 1
	fi

	# Copy binaries
	cp magiskinit /sbin/

	if [ $have_rootfs -ne 0 ]; then
		mkdir /sbin/.magisk/mirror/system_root
		block=$(mount | grep " / " | cut -d\  -f1)
		[ $block = "/dev/root" ] && block=/dev/block/dm-0
		mount -o ro $block /sbin/.magisk/mirror/system_root
		for file in /sbin/.magisk/mirror/system_root/sbin/*; do
			if [ -L $file ]; then
			  cp -a $file /sbin/
			else
			  cp -ps $file /sbin/${file##*/}
			fi
		done
	fi

	export PATH=/sbin:$PATH

	# Finish startup calls
	magisk --post-fs-data
	sleep 1		# hack to prevent race with later service calls
	magisk --service
	magisk --boot-complete
fi

setenforce 1
'

mkdir -p $HOMEDIR
cd $HOMEDIR || exit 1

if ! cmp -s $SRCDIR/bin/magiskinit magiskinit; then
	cp $SRCDIR/bin/magiskinit ./
	chmod 700 magiskinit

	ln -fs magiskinit magiskpolicy
	ln -fs magiskinit magisk
fi

if ! cmp -s $SRCDIR/bin/mtk-su mtk-su; then
	cp $SRCDIR/bin/mtk-su ./
	chmod 700 mtk-su
fi

# strip ':c512...' tail from selinux context
ctx=$(cat /proc/$$/attr/current)
newctx=${ctx/%:s0:*/:s0}

# start SU daemon
export HOMEDIR
echo "$SU_MINISCRIPT" | ./mtk-su -Z $newctx

log -p e -t suboot "retcode ${?}"