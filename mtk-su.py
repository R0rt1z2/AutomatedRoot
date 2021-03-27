import os
import os.path
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

def install_apk(apk):
    os.system("adb install {}".format(apk))

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
                print("\n\n[!] ERROR: Device is unauthorized or offline!\n")
                sys.exit(1)
            break

def check_binary():
    if os.path.exists("files/arm/mtk-su") and os.path.exists("files/arm64/mtk-su"):
        pass
    else:
        print("[!] Could not find mtk-su binaries. Be sure to download them from the XDA thread and put them in the corresponding folder!\n")
        exit(1)

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

def check_platform(platform):
    print("[?] Checking platform...\n")
    if platform.startswith("mt81") or platform.startswith("mt67") or platform.startswith("mt6595") or platform.startswith("mt6580"):
        pass
    else:
        print("[!] Unsupported CPU! mtk-su is not compatible with {}!\n".format(platform))
        input()
        sys.exit(1)

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
    print("\n  4 - Bootless Root")
    print("\n  5 - Exit")

while True:
    show_menu()

    option = input("\n[?] Select an option >> ")

    if option is "1":
        os.system(clean)
        print_banner()
        check_devices()
        check_binary()

        print("[?] Getting device information...")

        print_device_info()

        arch = get_prop("ro.product.cpu.abi", "arch")
        platform = get_prop("ro.hardware", "platform")

        check_platform(platform)
                
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
            print("\n[?] SuperSU already installed...\n")
            pass
        else:
            print("\n[?] Installing SuperSU...\n")
            install_apk("files/common/SuperSU.apk")

        print("\n[?] Starting Root Process...\n")
        call("adb shell chmod 755 /data/local/tmp/arm/mtk-su",shell=True)
        call("adb shell chmod 755 /data/local/tmp/arm64/mtk-su",shell=True)
        call("adb shell chmod 755 /data/local/tmp/root.sh",shell=True)

        if "arm64" in arch:
            call('adb shell /data/local/tmp/arm64/mtk-su -c "/data/local/tmp/root.sh"',shell=True)
        elif "armeabi-v7a" in arch:
            call('adb shell /data/local/tmp/arm/mtk-su -c "/data/local/tmp/root.sh"',shell=True)

        input("[?] Press any key to continue...\n")

    elif option is "3":
        os.system(clean)
        print_banner()
        check_devices()
        check_binary()
               
        Popen('adb shell mkdir /data/local/tmp/arm', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
        Popen('adb shell mkdir /data/local/tmp/arm64', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
        arch = get_prop("ro.product.cpu.abi", "arch")
        print("[?] Spawning Root Shell...\n")
        print("[?] To quit the shell, type 'exit' or press CTRL+C to kill the script\n")
        if "arm64-v8a" in arch:
            call("adb push files/arm64/mtk-su /data/local/tmp/arm64",shell=True)
            call("adb shell chmod 755 /data/local/tmp/arm64/mtk-su",shell=True)
            call("adb shell /data/local/tmp/mtk-su -c '/system/bin/sh'",shell=True)
            os.system(clean)
            break
        elif "armeabi-v7a" in arch:
            call("adb push files/arm/mtk-su /data/local/tmp/arm",shell=True)
            call("adb shell chmod 755 /data/local/tmp/arm/mtk-su",shell=True)
            call("adb shell /data/local/tmp/mtk-su -c '/system/bin/sh'",shell=True)
            os.system(clean)
            break

    elif option is "2":
        os.system(clean)
        print_banner()
        check_devices()
        check_binary()

        print("\n[?] Getting device information...")

        print_device_info()
        root = get_var_from_system("adb shell which su")

        if "su" not in root:
            print("[-] Your device doesn't seems to be rooted!\n")
            break
        else:
            print("[?] Pushing unroot script...\n")
            call("adb push files/common/unroot.sh /data/local/tmp", shell=True)
            print("\n[?] Setting correct permissions...\n")
            call("adb shell chmod 755 /data/local/tmp/unroot.sh", shell=True)
            print("[?] Starting the unroot process...\n")
            call("adb shell su -c '/data/local/tmp/unroot.sh'", shell=True)
            input("[?] Press any key to continue...\n")

    elif option is "4":
        os.system(clean)
        print_banner()
        check_devices()
        check_binary()

        print("[?] Bootless Root Enabler")
 
        print("\n[?] Getting device information...")

        print_device_info()

        arch = get_prop("ro.product.cpu.abi", "arch")
        platform = get_prop("ro.hardware", "platform")

        check_platform(platform)

        print("[?] Preparing environment...\n")

        Popen('adb shell mkdir /sdcard/init.d', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
        Popen('adb shell mkdir /sdcard/init.d/bin', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')

        if "arm64" in arch:
            push_file("files/arm64/mtk-su", "/sdcard/init.d/bin/")
        elif "abi" in arch:
            push_file("files/arm/mtk-su", "/sdcard/init.d/bin/")
            push_file("files/common/magiskinit", "/sdcard/init.d/bin/")
            push_file("files/common/magisk-boot.sh", "/sdcard/init.d/")

        packages = get_var_from_system("adb shell pm list packages")

        if "initd" in packages:
            print("\n[?] Initd Support app already installed. Skip the install...\n")
            Popen('adb shell pm clear com.ryosoftware.initd', shell=True, bufsize=64, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True).stdout.read().strip().decode('utf-8')
        else:
            print("\n[?] Installing Initd Support app...\n")
            install_apk("files/common/Initd.apk")

        if "magisk" in packages:
            print("[?] Magisk Manager is already installed. Skip the install...\n")
        else:
            print("[?] Installing Magisk Manager...\n")
            install_apk("files/common/Magisk.apk")

        print("[?] Pushing the helper...\n")
        push_file("files/common/bootless_helper.sh", "/data/local/tmp/")
        call("adb shell chmod 755 /data/local/tmp/bootless_helper.sh", shell=True)

        print("\n[?] Calling the helper...")
        call("adb shell /data/local/tmp/bootless_helper.sh", shell=True)
        print("[?] Exiting in 10 seconds...\n")
        time.sleep(10)
        os.system(clean)
        break

    elif option is "5":
        os.system(clean)
        break

    else:
        input("\n[!] {}: invalid option. Press any key to continue...\n".format(option))
