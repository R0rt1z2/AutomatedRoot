#!/usr/bin/env python3

         #====================================================#
         #              FILE: mtk-su.py                       #
         #              AUTHOR: R0rt1z2                       #
         #              DATE: 2019-2021                       #
         #====================================================#

#   Automated root script for mediatek arm64 devices. Usage:
#   "python3 mtk-su.py" (no arguments needed).
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#   Thanks to diplomatic (mtk-su/CVE-2020-0069).

import os
import os.path
import subprocess
import time
import sys

if sys.platform.startswith("win"):
    clean = "cls"
else:
    clean = "clear"

CPU_REGEX = [
    "mt81",
    "mt67",
    "mt6580",
    "mt6595"
]

def shellcmd(cmd):
    return subprocess.Popen(
        f'{cmd}', shell=True, bufsize=64, 
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        close_fds=True).stdout.read().rstrip().decode('utf-8')

def push_file(file, target):
    os.system("adb push {} {}".format(file, target))

def install_apk(apk):
    os.system("adb install {}".format(apk))

def check_devices():
    devices = shellcmd("adb devices")
    sys.stdout.write("\n[?] Waiting for devices...")
    while True:
        if len(devices) == 24:
            devices = shellcmd("adb devices")
            sys.stdout.write("."); sys.stdout.flush()
            time.sleep(1)
        else:
            print("\n\n[+] Found device!\n")
            if "offline" in devices or "unauthorized" in devices:
                print("\n\n[!] ERROR: Device is unauthorized or offline!\n")
                sys.exit(1)
            break

def mkline(title, subtitle, margin):
    line_len = len("| {}: {}".format(title, subtitle))
    to_add = margin - line_len - 1
    h = ''.join(["   " + "| {}: {}".format(title, subtitle)] + [ ' ' *to_add ] + ['|'])
    print(h)

def print_device_info():
    device = shellcmd("adb shell getprop ro.product.model")
    platform = shellcmd("adb shell getprop ro.hardware")
    arch = shellcmd("adb shell getprop ro.product.cpu.abi")
    android_ver = shellcmd("adb shell getprop ro.build.version.release")
    brand = shellcmd("adb shell getprop ro.product.manufacturer")
    selinux_status = shellcmd("adb shell getenforce")
    root_present = shellcmd("adb shell which su")
    margin = ''.join(["   " + '-' * 50])
    print(margin)
    mkline("DEVICE", device, 50)
    mkline("BRAND", brand, 50)
    mkline("ARCH", arch, 50)
    mkline("PLATFORM", platform, 50)
    mkline("ANDROID VERSION", android_ver, 50)
    mkline("SELINUX STATUS", selinux_status, 50)
    mkline("ROOT?", root_present, 50)
    print(margin)

def check_platform(platform):
    if platform[:4] not in CPU_REGEX:
        print("[!] Unsupported CPU! mtk-su is not compatible with {}!\n".format(platform))
        input("[?] Press any key to continue...\n")
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
    print("\n  3 - Bootless Root")
    print("\n  4 - Exit")

if not os.path.exists("files/arm/mtk-su") or not os.path.exists("files/arm64/mtk-su"):
    print("[!] Could not find mtk-su binaries. Make sure to download them from the XDA thread and put them in the corresponding folder!")
    input("[?] Press any key to continue...")
    sys.exit(1)

while True:
    show_menu()

    option = input("\n[?] Select an option >> ")

    if option == "1":
        os.system(clean)
        print_banner()
        check_devices()

        print("[?] Getting device information...")
        print_device_info()
        arch = shellcmd("adb shell getprop ro.product.cpu.abi")
        platform = shellcmd("adb shell getprop ro.hardware")
        check_platform(platform)
                
        print("[?] Pushing files...\n")
        shellcmd("adb shell mkdir /data/local/tmp/arm")
        shellcmd("adb shell mkdir /data/local/tmp/arm64")
        push_file("files/arm64/mtk-su", "/data/local/tmp/arm64")
        push_file("files/common/root.sh", "/data/local/tmp")
        push_file("files/arm64/su", "/data/local/tmp/arm64")
        push_file("files/arm64/supolicy", "/data/local/tmp/arm64")
        push_file("files/arm64/libsupol.so", "/data/local/tmp/arm64")
        push_file("files/arm/mtk-su", "/data/local/tmp/arm")
        push_file("files/arm/su", "/data/local/tmp/arm")
        push_file("files/arm/supolicy", "/data/local/tmp/arm")
        push_file("files/arm/libsupol.so", "/data/local/tmp/arm")

        packages = shellcmd("adb shell pm list packages")

        if "supersu" not in packages:
            print("\n[?] Installing SuperSU...\n")
            install_apk("files/common/SuperSU.apk")

        print("\n[?] Starting Root Process...\n")
        shellcmd("adb shell chmod 755 /data/local/tmp/arm/mtk-su")
        shellcmd("adb shell chmod 755 /data/local/tmp/arm64/mtk-su")
        shellcmd("adb shell chmod 755 /data/local/tmp/root.sh")

        if "arm64" in arch:
            subprocess.call('adb shell /data/local/tmp/arm64/mtk-su -c "/data/local/tmp/root.sh"', shell=True)
        elif "armeabi-v7a" in arch:
            subprocess.call('adb shell /data/local/tmp/arm/mtk-su -c "/data/local/tmp/root.sh"', shell=True)

        input("[?] Press any key to continue...\n")

    elif option == "2":
        os.system(clean)
        print_banner()
        check_devices()

        print("\n[?] Getting device information...")

        print_device_info()
        root = shellcmd("adb shell which su")

        if "su" not in root:
            print("[-] Your device doesn't seem to be rooted!\n")
            break
        else:
            print("[?] Pushing unroot script...\n")
            push_file("files/common/unroot.sh", "/data/local/tmp")
            print("\n[?] Setting correct permissions...\n")
            shellcmd("adb shell chmod 755 /data/local/tmp/unroot.sh")
            print("[?] Starting the unroot process...\n")
            subprocess.call("adb shell su -c '/data/local/tmp/unroot.sh'", shell=True)
            input("[?] Press any key to continue...\n")

    elif option == "3":
        os.system(clean)
        print_banner()
        check_devices()

        print("[?] Bootless Root Enabler")
 
        print("\n[?] Getting device information...")
        print_device_info()
        arch = shellcmd("adb shell getprop ro.product.cpu.abi")
        platform = shellcmd("adb shell getprop ro.hardware")
        check_platform(platform)

        print("[?] Preparing environment...\n")
        shellcmd("adb shell mkdir /sdcard/init.d")
        shellcmd("adb shell mkdir /sdcard/init.d/bin")

        if "arm64" in arch:
            push_file("files/arm64/mtk-su", "/sdcard/init.d/bin/")
        elif "abi" in arch:
            push_file("files/arm/mtk-su", "/sdcard/init.d/bin/")
            push_file("files/common/magiskinit", "/sdcard/init.d/bin/")
            push_file("files/common/magisk-boot.sh", "/sdcard/init.d/")

        packages = shellcmd("adb shell pm list packages")

        if "initd" in packages:
            print("\n[?] Initd Support app already installed. Skip the install...\n")
            shellcmd("adb shell pm clear com.ryosoftware.initd")
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
        shellcmd("adb shell chmod 755 /data/local/tmp/bootless_helper.sh")

        print("\n[?] Calling the helper...")
        subprocess.call("adb shell /data/local/tmp/bootless_helper.sh", shell=True)
        print("[?] Exiting in 10 seconds...\n")
        time.sleep(10)
        os.system(clean)
        break

    elif option == "4":
        os.system(clean)
        break

    else:
        input("\n[!] {}: invalid option. Press any key to continue...\n".format(option))