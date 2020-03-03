import os
import subprocess
import time
from subprocess import Popen, PIPE, DEVNULL, STDOUT, check_call, call
from sys import platform as _platform
import sys

# By R0rt1z2
# All the credits goes to diplomatic for create his excellent MTK-SU!

if _platform == "linux":
    clean = "clear"
elif _platform == "win64" or "win32":
    clean = "cls"

def get_var_from_system(command):
        var = Popen(f'{command}', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
        return var

def push_file(file, target):
        os.system("adb push {} {}".format(file, target))

def get_prop(prop, name):
        name = Popen(f'adb shell getprop {prop}', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
        return name

def check_devices():
        devices = get_var_from_system("adb devices")
        sys.stdout.write("\n[?] Waiting for the device...")
        while True:
              if len(devices) == 24:
                 devices = get_var_from_system("adb devices")
                 sys.stdout.write("."); sys.stdout.flush()
                 time.sleep(1)
              else:
                 print("\n\n[+] Found device!\n")
                 if "offline" in devices or "unauthorized" in devices:
                     print("[!] ERROR: Device is unauthorized or offline!\n")
                     sys.exit(1)
                 break

def make_line(title, subtitle, margin):
         line_len = len("| {}: {}".format(title, subtitle))
         to_add = margin - line_len - 1
         h = ''.join(["   " + "| {}: {}".format(title, subtitle)] + [ ' ' *to_add ] + ['|'])
         print(h)

def print_device_info():
         ''' This needs a cleaner way! '''
         device = get_prop("ro.product.model", "model")
         platform = get_prop("ro.hardware", "platform")
         arch = get_prop("ro.product.cpu.abi", "arch")
         android_ver = get_prop("ro.build.version.release", "android")
         brand = get_prop("ro.product.manufacturer", "brand")
         selinux_status = get_var_from_system("adb shell getenforce")
         root_present = get_var_from_system("adb shell which su")
         margin = ''.join(["   " + '-' *50])
         print(margin)
         make_line("DEVICE", device, 50)
         make_line("BRAND", brand, 50)
         make_line("ARCH", arch, 50)
         make_line("PLATFORM", platform, 50)
         make_line("ANDROID VERSION", android_ver, 50)
         make_line("SELINUX STATUS", selinux_status, 50)
         make_line("ROOT?", root_present, 50)
         print(margin)

def print_banner():
         print("   __          _                        _           _   __    ___  ___  _____")
         print("  /_ \   _   _| |_ ___  _ __ ___   __ _| |_ ___  __| | /__\  /___\/___\/__   \ ")
         print(" //_\ \ | | | | __/ _ \| '_ ` _ \ / _` | __/ _ \/ _` |/ \// //  ///  //  / /\/")
         print("/  _   \| |_| ||   (_) | | | | | | (_| | ||  __/ (_| / _  \/ \_// \_//  / /   ")
         print("\_/ \_/ \__,_|\__ \___/|_| |_| |_|\__,_|\__\___|\__,_\/ \_/\___/\___/   \/ ")
                                                                           

def show_menu():
        os.system(clean)
        print_banner()
        print("\n  1 - Root the Device")
        print("\n  2 - Unroot the device")
        print("\n  3 - Spawn Root Shell")
        print("\n  4 - Exit")

while True:
        show_menu()

        option = input("\n[?] Select an option >> ")

        if option is "1":
             os.system(clean)
             print_banner()
             check_devices()
             print("\n[?] Getting device information...")

             print_device_info()

             arch = get_prop("ro.product.cpu.abi", "arch")
             platform = get_prop("ro.hardware", "platform")

             if "mt81" or "mt67" or "mt6595" or "mt6580" in platform:
                pass
             else:
                print("[!] Unsupported CPU! mtk-su is not compatible with {}!\n".format(platform))
                break
                sys.exit(1)
             if "arm64-v8a" in arch:
                print("[?] Pushing files...\n")
                Popen('adb shell mkdir /data/local/tmp/arm', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
                Popen('adb shell mkdir /data/local/tmp/arm64', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
                push_file("files/arm64/mtk-su", "/data/local/tmp/arm64")
                push_file("files/common/root.sh", "/data/local/tmp")
                push_file("files/arm64/su", "/data/local/tmp/arm64")
                push_file("files/arm64/supolicy", "/data/local/tmp/arm64")
                push_file("files/arm64/libsupol.so", "/data/local/tmp/arm64")
                push_file("files/arm/mtk-su", "/data/local/tmp/arm")
                push_file("files/arm/su", "/data/local/tmp/arm")
                push_file("files/arm/supolicy", "/data/local/tmp/arm")
                push_file("files/arm/libsupol.so", "/data/local/tmp/arm")

                supersu = get_var_from_system("adb shell pm list packages")

                if "supersu" in supersu:
                   print("\n[?] SuperSU it's already installed...\n")
                   pass
                else:
                   print("[?] Installing SuperSU...\n")
                   call("adb install files/common/SuperSU.apk",shell=True)
                   pass
                print("[?] Starting Root Process...\n")
                call("adb shell chmod 755 /data/local/tmp/arm/mtk-su",shell=True)
                call("adb shell chmod 755 /data/local/tmp/arm64/mtk-su",shell=True)
                call("adb shell chmod 755 /data/local/tmp/root.sh",shell=True)

                if "arm64" in arch:
                    call('adb shell /data/local/tmp/arm64/mtk-su -c "/data/local/tmp/root.sh"',shell=True)
                elif "armeabi-v7a" in arch:
                    call('adb shell /data/local/tmp/arm/mtk-su -c "/data/local/tmp/root.sh"',shell=True)

                ("[?] Press enter to continue\n")

        elif option is "3":
               os.system(clean)
               print_banner()
               check_devices()
               Popen('adb shell mkdir /data/local/tmp/arm', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
               Popen('adb shell mkdir /data/local/tmp/arm64', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
               arch = get_prop("ro.product.cpu.abi", "arch")
               print("[?] Spawning Root Shell...\n")
               print("[?] For exit type 'exit' or press Control+C for terminate the script\n")
               if "arm64-v8a" in arch:
                   call("adb push files/arm64/mtk-su /data/local/tmp/arm64",shell=True)
                   call("adb shell chmod 755 /data/local/tmp/arm64/mtk-su",shell=True)
                   call("adb shell /data/local/tmp/mtk-su -c '/system/bin/sh'",shell=True)
                   os.system(clean)
               elif "armeabi-v7a" in arch:
                   call("adb push files/arm/mtk-su /data/local/tmp/arm",shell=True)
                   call("adb shell chmod 755 /data/local/tmp/arm/mtk-su",shell=True)
                   call("adb shell /data/local/tmp/mtk-su -c '/system/bin/sh'",shell=True)
                   os.system(clean)               

        elif option is "2":
               os.system(clean)
               print_banner()
               check_devices()
               print("\n[?] Getting device information...")

               print_device_info()
               root = get_var_from_system("adb shell which su")
               if "su" in root:
                   root = "yes"
                   pass
               else:
                   root = "no"
                   pass
               if "no" in root:
                   print("[-] Your device doesn't seems to be rooted!\n")
                   break
               else:
                   print("[?] Pushing unroot script...\n")
                   os.system("adb push files/common/unroot.sh /data/local/tmp")
                   print("\n[?] Setting correct permissions...\n")
                   os.system("adb shell chmod 755 /data/local/tmp/unroot.sh")
                   print("[?] Starting the unroot process...\n")
                   os.system("adb shell su -c '/data/local/tmp/unroot.sh'")
                   input("[?] Press enter to continue\n")

        elif option is "4":
              os.system(clean)
              break
              exit(0)

        else:
               input("\n[!] {}: invalid option. Press any key to continue...\n".format(option))
