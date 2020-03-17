#!/system/bin/sh
#
# Updated: Dec 26, 2019
# by diplomatic
#
# This script sets up bootless root with Magisk on MediaTek Android devices.
# It uses mtk-su, the temporary root tool for MediaTek ARMv8 chips. Currently
# this only supports Magisk up to 18.1. Must be run from the app 
# 'init.d scripts support' by RYO Software. Put this file into
# /storage/emulated/0/init.d along with mtk-su and magiskinit into .../init.d/bin
# Point the app to run sh scripts from /storage/emulated/0/init.d at boot time.
#
# WARNING: DO NOT UPDATE MAGISK THROUGH MAGISK MANAGER OR YOU WILL BRICK YOUR
#          DEVICE ON A LOCKED BOOTLOADER
#

HOMEDIR=/data/data/com.ryosoftware.initd/files/bin
SRCDIR=/storage/emulated/0/init.d

SU_MINISCRIPT='
# Magisk function to find boot partition and prevent the installer from finding
# it again
toupper() {
  echo "$@" | tr "[:lower:]" "[:upper:]"
}

grep_prop() {
  local REGEX="s/^$1=//p"
  shift
  local FILES=$@
  sed -n "$REGEX" $FILES 2>/dev/null | head -n 1
}

find_block() {
  for BLOCK in "$@"; do
    DEVICES=`find /dev/block -type l -iname $BLOCK` 2>/dev/null
    for DEVICE in $DEVICES; do
      if [ -h "$DEVICE" ]; then
	    cd ${DEVICE%/*}
	    BASENAME="${DEVICE##*/}"
	    mv "$BASENAME" ".$BASENAME"
	    cd -
	  fi
	done
  done
  # Fallback by parsing sysfs uevents
  for uevent in /sys/dev/block/*/uevent; do
    local PARTNAME=`grep_prop PARTNAME $uevent`
    for BLOCK in "$@"; do
      if [ "`toupper $BLOCK`" = "`toupper $PARTNAME`" ]; then
        #echo /dev/block/$DEVNAME
        #return 0
        chmod 0 $uevent
      fi
    done
  done
  return 1
}

# Root only at this point; hoping selinux is permissive
if [ $(id -u) != 0 ] || [ "$(getenforce)" != "Permissive" ]; then
	echo "Root user only" >&2
	exit 1
fi

cd $HOMEDIR

# Patch selinux policy -- error messages here are normal
./magiskpolicy --live --magisk "allow magisk * * *"
if [ ! -f /sbin/.init-stamp ]; then
	# Create tmpfs /xbin overlay
	./magisk --startup

	if [ ! -f /sbin/magiskinit ] || [ ! -f /sbin/magisk.bin ]; then
		echo "Bad /sbin mount?" >&2
		setenforce 1
		exit 1
	fi

	# Copy binaries
	cp magiskinit /sbin/

	export PATH=/sbin:$PATH
	magiskinit -x magisk /sbin/magisk.bin

	# Finish startup calls
	magisk --post-fs-data
	magisk --service
	magisk --boot-complete

	touch /sbin/.init-stamp
fi

# Disaster prevention
SLOT=$(getprop ro.boot.slot_suffix)
find_block boot$SLOT

setenforce 1
'

mkdir -p $HOMEDIR
cd $HOMEDIR || exit 1

if ! cmp -s $SRCDIR/bin/magiskinit magiskinit; then
	cp $SRCDIR/bin/magiskinit ./
	chmod 700 magiskinit

	./magiskinit -x magisk ./magisk || exit 1
	chmod 700 magisk

	ln -fs magiskinit magiskpolicy
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

RESULT=$?

echo "EXIT CODE: $RESULT"

logcat -c

if [ $RESULT -eq 0 ]; then
   log -p e -t suboot suboot finished
fi
