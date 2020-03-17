#!/system/bin/sh
##########################################################################################
# Bootless ROOT Helper Script
##########################################################################################

INITD_DIR="/sdcard/init.d/"
FILES=$(ls $INITD_DIR | grep bin)
DONE="/data/local/tmp/done"

# Check pushed files
if [ "$FILES" -eq 0 ]; then
   echo ""
else
   echo "[!] Cannot find pushed files... Abort!\n"
   exit 1
fi

PACKAGES=$(pm list packages | grep initd)
RES=$?
# Check if initd app was installed correctly
if [ "$RES" -eq 1 ]; then
   echo "[!] Cannot find initd support app... Abort!\n"
   exit 1
fi

# Launch Initd Support
am start com.ryosoftware.initd/.PreferencesActivity > /dev/null 2>&1

# Show instructions to follow them manually.
echo "[?] Accept the terms and allow initd support to access media. Then follow the following instructions:\n"
echo "    - Set 'Run scripts on boot time' to CHECKED."
echo "    - Set 'Execution delay' to NO DELAY."
echo "    - Set 'Selected folder' to init.d folder located in the Internal Storage."
echo "    - Click on 'Run scripts now' and watch the ad to unlock the feature. (Support the developer!)."
echo ""

# Constantly check if suboot finished...
echo "[?] Checking if succeed...\n"

logcat | grep -E --line-buffered 'suboot finished' | while read line; do touch /data/local/tmp/done; done &

while [ 1 == 1 ]
do
   RES=$(ls /data/local/tmp/ | grep done)
   RES=$?
   if [ "$RES" -eq 0 ]; then
      echo "[+] suboot script ran succsusfully!\n"
	  rm /data/local/tmp/done
	  logcat -c
	  break
   fi
done

# Launch Magisk
echo "[?] Launching Magisk...\n"
am start com.topjohnwu.magisk/a.c > /dev/null 2>&1

exit 0