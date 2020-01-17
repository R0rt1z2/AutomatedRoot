import os
import subprocess
import time
from subprocess import Popen, PIPE, DEVNULL, STDOUT, check_call, call
from sys import platform as _platform

# By R0rt1z2
# All the credits goes to diplomatic for create his excellent MTK-SU!

# Define clean variable for various OS.
if _platform == "linux":
    clean = "clear"
elif _platform == "win64" or "win32":
    clean = "cls"

def push_file(file, target):
        call(f'adb push {file} {target}')

def menu():
        os.system(clean)
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
             os.system(clean)
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
             supersu = Popen('adb shell pm list packages', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
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
                 time.sleep(1)
                 break
             # ty t0x1cSH
             if "arm64-v8a" in arch:
                print("Detected arm64 arch.. Pushing arm64 mtk-su & files")
                push_file("arm64/mtk-su", "/data/local/tmp")
                push_file("arm64/root.sh", "/data/local/tmp")
                push_file("arm64/su", "/data/local/tmp")
                push_file("arm64/supolicy", "/data/local/tmp")
                push_file("arm64/libsupol.so", "/data/local/tmp")
                print("--------------------------------------")
                print("Pushed files succsefully!")
                print("--------------------------------------")
                if "chainfire" in supersu:
                   print("SuperSU already installed... Skip the install")
                   pass
                else:
                   print("Installing SuperSU...")
                   call("adb install files/SuperSU.apk",shell=True)
                   pass
                print("--------------------------------------")
                print("Starting Root Process...")
                call("adb shell chmod 755 /data/local/tmp/mtk-su",shell=True)
                call("adb shell chmod 755 /data/local/tmp/root.sh",shell=True)
                call('adb shell /data/local/tmp/mtk-su -c "/data/local/tmp/root.sh"',shell=True)
                print("--------------------------------------")
                wait = input("PRESS ENTER TO CONTINUE.")
                print("--------------------------------------")
                os.system(clean)
             elif "armeabi-v7a" in arch:
                print("Detected armv7 arch.. Pushing armv7 mtk-su & files")
                push_file("arm/mtk-su", "/data/local/tmp")
                push_file("arm/root.sh", "/data/local/tmp")
                push_file("arm/su", "/data/local/tmp")
                push_file("arm/supolicy", "/data/local/tmp")
                push_file("arm/libsupol.so", "/data/local/tmp")
                print("--------------------------------------")
                print("Pushed files succsefully!")
                print("--------------------------------------")     
                if "supersu" in supersu:
                   print("SuperSU already installed... Skip the install")
                   pass
                else:
                   print("Installing SuperSU...")
                   call("adb install files/SuperSU.apk",shell=True)
                   pass
                print("--------------------------------------")
                print("Starting Root Process...")
                call("adb shell chmod 755 /data/local/tmp/mtk-su",shell=True)
                call("adb shell chmod 755 /data/local/tmp/root.sh",shell=True)
                call('adb shell /data/local/tmp/mtk-su -c "/data/local/tmp/root.sh"',shell=True)
                print("--------------------------------------")
                wait = input("PRESS ENTER TO CONTINUE.")
                print("--------------------------------------")


        elif option=="2":
               os.system(clean)
               print("ROOT SHELL SPAWNER")
               arch = Popen('adb shell getprop ro.product.cpu.abi', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
               print("Spawning Root Shell... \n For exit type 'exit' or Control+C for terminate the script")
               if "arm64-v8a" in arch:
                   call("adb push arm64/mtk-su /data/local/tmp",shell=True)
                   call("adb shell chmod 755 /data/local/tmp/mtk-su",shell=True)
                   call("adb shell /data/local/tmp/mtk-su",shell=True)
                   wait = input("PRESS ENTER TO CONTINUE.")
                   os.system(clean)
               elif "armeabi-v7a" in arch:
                   call("adb push arm/mtk-su /data/local/tmp",shell=True)
                   call("adb shell chmod 755 /data/local/tmp/mtk-su",shell=True)
                   call("adb shell /data/local/tmp/mtk-su",shell=True)
                   wait = input("PRESS ENTER TO CONTINUE.")
                   os.system(clean)

        elif option=="3":
               os.system(clean)
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
                      print ("Pushing files...")
                      os.system("adb push arm/unroot.sh /data/local/tmp")
                      print("Setting correct permissions...")
                      os.system("adb shell chmod 755 /data/local/tmp/*")
                      print("Starting the unroot process")
                      os.system("adb shell su -c './data/local/tmp/unroot.sh'")
                      os.system("sleep 5")
                   elif "arm64" in arch:
                      arch = "arm64"
                      print ("Pushing files...")
                      os.system("adb push arm64/unroot.sh /data/local/tmp")
                      print("Setting correct permissions...")
                      os.system("adb shell chmod 755 /data/local/tmp/*")
                      print("Starting the unroot process")
                      os.system("adb shell su -c './data/local/tmp/unroot.sh'")


        elif option=="4":
              os.system(clean)
              print("BYE BYE")
              time.sleep(0.5)
              os.system(clean)
              break

        else:
               print("")
               input("Incorrect option...\nPress any key to continue..")
