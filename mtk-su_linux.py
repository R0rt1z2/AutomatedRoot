import os
import subprocess
import time
from subprocess import Popen, PIPE, DEVNULL, STDOUT, check_call

# By R0rt1z2
# All the credits goes to diplomatic for create his excellent MTK-SU!

def menu():
        """
        Fucntion to clean
        """
        os.system('clear')
        print("\t Big thanks to diplomatic")
        print("\t1 - Root the Device")
        print("\t2 - Spawn Root Shell")
        print("\t3 - Unroot the device")
        print("\t4 - Exit")

while True:
        #show menu
        menu()

        #user sets option
        option = input("Select an option >> ")

        if option=="1":
             # Clean before continue
             os.system("clear")
             print("Detecting device information....")
             print("--------------------------------------")
             verity = Popen('adb shell getprop ro.boot.veritymode', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
             mtk = Popen('adb shell getprop debug.mtklog.netlog.Running', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
             device = Popen('adb shell getprop ro.product.model', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
             platform = Popen('adb shell getprop ro.hardware', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
             platform2 = Popen('adb shell getprop ro.hardware', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
             arch = Popen('adb shell getprop ro.product.cpu.abi', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
             android = Popen('adb shell getprop ro.build.version.release', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
             brand = Popen('adb shell getprop ro.product.manufacturer', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
             selinux = Popen('adb shell getenforce', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
             supersu = Popen('adb shell pm list packages | grep chainfire', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
             root = Popen('adb shell which su', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
             if "su" in root:
                   root = "yes"
                   pass
             else:
                   root = "no"
                   pass
             print("Device: " + device)
             print("Brand: " + brand)
             print("ARCH: " + arch)
             print("Platform: " + platform2)
             print("Android: " + android)
             print("SELinux status: " + selinux)
             print("Root: " + root)
             print("--------------------------------------")
             if "mt81" or "mt67" in platform:
               pass
             else:
               wait = input("Incompatible CPU! BYE!")
               break
             if "enforcing" in verity:
                 print("Sorry! Your device seems to have DM-Verity, this method will not work. Exiting...")
                 break
             elif " " in verity:
                 continue
             # ty t0x1cSH
             if "arm64-v8a" in arch:
                print("Detected arm64 arch.. Pushing arm64 mtk-su & files")
                subprocess.call("adb push arm64/mtk-su arm64/root.sh arm64/su arm64/supolicy arm64/libsupol.so /data/local/tmp",shell=True)
                print("--------------------------------------")
                print("Pushed files succsefully!")
                print("--------------------------------------")
                print(supersu)
                if "chainfire" in supersu:
                   print("SuperSU already installed... Skip the install")
                   pass
                else:
                   print("Installing SuperSU...")
                   subprocess.call("adb install files/SuperSU.apk",shell=True)
                   pass
                print("--------------------------------------")
                print("Starting Root Process...")
                subprocess.call("adb shell chmod 755 /data/local/tmp/mtk-su",shell=True)
                subprocess.call("adb shell chmod 755 /data/local/tmp/root.sh",shell=True)
                subprocess.call('adb shell /data/local/tmp/mtk-su -c "/data/local/tmp/root.sh"',shell=True)
                print("--------------------------------------")
                wait = input("PRESS ENTER TO CONTINUE.")
                print("--------------------------------------")
                os.system('clear')
             # ty t0x1cSH
             elif "armeabi-v7a" in arch:
                print("Detected armv7 arch.. Pushing armv7 mtk-su & files")
                subprocess.call("adb push arm/mtk-su arm/root.sh arm/su arm/supolicy arm/libsupol.so /data/local/tmp",shell=True)
                print("--------------------------------------")
                print("Pushed files succsefully!")
                print("--------------------------------------")     
                print(supersu)           
                if "supersu" in supersu:
                   print("SuperSU already installed... Skip the install")
                   pass
                else:
                   print("Installing SuperSU...")
                   subprocess.call("adb install files/SuperSU.apk",shell=True)
                   pass
                print("--------------------------------------")
                print("Starting Root Process...")
                subprocess.call("adb shell chmod 755 /data/local/tmp/mtk-su",shell=True)
                subprocess.call("adb shell chmod 755 /data/local/tmp/root.sh",shell=True)
                subprocess.call('adb shell /data/local/tmp/mtk-su -c "/data/local/tmp/root.sh"',shell=True)
                print("--------------------------------------")
                wait = input("PRESS ENTER TO CONTINUE.")
                print("--------------------------------------")


        elif option=="2":
               os.system("clear")
               print("ROOT SHELL SPAWNER")
               arch = Popen('adb shell getprop ro.product.cpu.abi', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
               print("Spawning Root Shell... \n For exit type 'exit' or Control+C for terminate the script")
               # ty again t0x1cSH :)
               if "arm64-v8a" in arch:
                   subprocess.call("adb push arm64/mtk-su /data/local/tmp",shell=True)
                   subprocess.call("adb shell chmod 755 /data/local/tmp/mtk-su",shell=True)
                   subprocess.call("adb shell /data/local/tmp/mtk-su",shell=True)
                   wait = input("PRESS ENTER TO CONTINUE.")
                   os.system('clear')
               elif "armeabi-v7a" in arch:
               # ty again again XD
                   subprocess.call("adb push arm/mtk-su /data/local/tmp",shell=True)
                   subprocess.call("adb shell chmod 755 /data/local/tmp/mtk-su",shell=True)
                   subprocess.call("adb shell /data/local/tmp/mtk-su",shell=True)
                   wait = input("PRESS ENTER TO CONTINUE.")
                   os.system('clear')

        elif option=="3":
               os.system("clear")
               print("Detecting device information....")
               print("--------------------------------------")
               verity = Popen('adb shell getprop ro.boot.veritymode', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
               mtk = Popen('adb shell getprop debug.mtklog.netlog.Running', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
               device = Popen('adb shell getprop ro.product.model', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
               platform = Popen('adb shell getprop ro.hardware', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
               platform2 = Popen('adb shell getprop ro.hardware', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
               arch = Popen('adb shell getprop ro.product.cpu.abi', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
               android = Popen('adb shell getprop ro.build.version.release', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
               brand = Popen('adb shell getprop ro.product.manufacturer', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
               selinux = Popen('adb shell getenforce', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
               supersu = Popen('adb shell pm list packages | grep chainfire', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
               root = Popen('adb shell which su', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
               if "su" in root:
                   root = "yes"
                   pass
               else:
                   root = "no"
                   pass
               print("Device: " + device)
               print("Brand: " + brand)
               print("ARCH: " + arch)
               print("Platform: " + platform2)
               print("Android: " + android)
               print("SELinux status: " + selinux)
               print("Root Status: " + root)
               print("--------------------------------------")
               if "no" in root:
                   print("You don't have root installed. How come you want to unroot it?")
                   break
               else:
                   print("Pushing unroot script & mtk-su...")
                   if "abi" in arch:
                      arch = "arm"
                      pusharm1 = "adb push " + arch + "/unroot.sh " + "/data/local/tmp"
                      pusharm2 = "adb push " + arch + "/mtk-su " + "/data/local/tmp"
                      os.system(pusharm1)
                      os.system(pusharm2)
                      print("Setting correct permissions...")
                      os.system("adb shell chmod 755 /data/local/tmp/*")
                      os.system("adb shell /data/local/tmp/mtk-su -c './data/local/tmp/unroot.sh'")
                      os.system("sleep 5")
                   elif "arm64" in arch:
                      arch = "arm64"
                      pusharm641 = "adb push " + arch + "/unroot.sh " + "/data/local/tmp"
                      pusharm642 = "adb push " + arch + "/mtk-su " + "/data/local/tmp"
                      os.system(pusharm641)
                      os.system(pusharm642)
                      print("Setting correct permissions...")
                      os.system("adb shell chmod 755 /data/local/tmp/*")
                      os.system("adb shell /data/local/tmp/mtk-su -c './data/local/tmp/unroot.sh'")
                      os.system("sleep 5")


        elif option=="3":
               break

        else:
               print("")
               input("Incorrect option...\nPress any key to continue..")
