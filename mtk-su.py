import os
import subprocess

# By R0rt1z2
# All the credits goes to diplomatic for create his excellent MTK-SU!

#set supported chipsets
supported = ['mt81', 'mt67']

def menu():
        """
        Fucntion to clean
        """
        os.system('cls')
        print("\t Big thanks to diplomatic")
        print("\t1 - Root the Device")
        print("\t2 - Spawn Root Shell")
        print("\t3 - Exit")

while True:
        #show menu
        menu()

        #user sets option
        option = input("Select an option >> ")

        if option=="1":
             print("Detecting device information....")
             print("--------------------------------------")
             subprocess.call("adb.exe shell getprop ro.boot.veritymode > verity.txt",shell=True)
             with open('verity.txt') as myfile:
               verity = myfile.read()
             subprocess.call("adb.exe shell getprop debug.mtklog.netlog.Running > mtk.txt",shell=True)
             with open('mtk.txt') as myfile:
               mtk = myfile.read()
             subprocess.call("adb.exe shell getprop ro.product.model > device.txt",shell=True)
             with open('device.txt') as myfile:
               device = myfile.read()
             subprocess.call("adb.exe shell getprop ro.hardware > platform.txt",shell=True)
             with open('platform.txt', 'r') as myfile:
               platform = myfile.read(4)
             subprocess.call("adb.exe shell getprop ro.hardware > platform2.txt",shell=True)
             with open('platform2.txt') as myfile:
               platform2 = myfile.read()
             subprocess.call("adb.exe shell getprop ro.product.cpu.abi > arch.txt",shell=True)
             with open('arch.txt') as myfile:
               arch = myfile.read()
             subprocess.call("adb.exe shell getprop ro.build.version.release > android.txt",shell=True)
             with open('android.txt') as myfile:
               android = myfile.read()
             subprocess.call("adb.exe shell getprop ro.product.manufacturer > brand.txt",shell=True)
             with open('brand.txt') as myfile:
               brand = myfile.read()
             subprocess.call("adb.exe shell getenforce > selinux.txt",shell=True)
             with open('selinux.txt') as myfile:
               selinux = myfile.read()
             subprocess.call("adb.exe shell pm list packages | grep supersu > supersu.txt",shell=True)
             with open('selinux.txt') as myfile:
               supersu = myfile.read()
             print("Device: " + device)
             print("Brand: " + brand)
             print("ARCH: " + arch)
             print("Platform: " + platform2)
             print("Android: " + android)
             print("SELinux status: " + selinux)
             print("--------------------------------------")
             if platform in ('mt81', 'mt67'):
              if platform in set(supported):
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
                subprocess.call("adb.exe push arm64/mtk-su arm64/root.sh arm64/su arm64/supolicy arm64/libsupol.so /data/local/tmp",shell=True)
                print("--------------------------------------")
                print("Pushed files succsefully!")
                print("--------------------------------------")
                print("Installing SuperSU...")
                subprocess.call("adb.exe install files/SuperSU.apk",shell=True)
                print("--------------------------------------")
                print("Starting Root Process...")
                subprocess.call("adb.exe shell chmod 755 /data/local/tmp/mtk-su",shell=True)
                subprocess.call("adb.exe shell chmod 755 /data/local/tmp/root.sh",shell=True)
                subprocess.call('adb.exe shell /data/local/tmp/mtk-su -c "/data/local/tmp/root.sh"',shell=True)
                print("--------------------------------------")
                wait = input("PRESS ENTER TO CONTINUE.")
                print("--------------------------------------")
                os.system('cls')
             # ty t0x1cSH
             elif "armeabi-v7a" in arch:
                print("Detected armv7 arch.. Pushing armv7 mtk-su & files")
                subprocess.call("adb.exe push arm/mtk-su arm/root.sh arm/su arm/supolicy arm/libsupol.so /data/local/tmp",shell=True)
                print("--------------------------------------")
                print("Pushed files succsefully!")
                print("--------------------------------------")
                print("Installing SuperSU...")
                subprocess.call("adb.exe install files/SuperSU.apk",shell=True)
                print("--------------------------------------")
                print("Starting Root Process...")
                subprocess.call("adb.exe shell chmod 755 /data/local/tmp/mtk-su",shell=True)
                subprocess.call("adb.exe shell chmod 755 /data/local/tmp/root.sh",shell=True)
                subprocess.call('adb.exe shell /data/local/tmp/mtk-su -c "/data/local/tmp/root.sh"',shell=True)
                print("--------------------------------------")
                wait = input("PRESS ENTER TO CONTINUE.")
                print("--------------------------------------")


        elif option=="2":
               print("ROOT SHELL SPAWNER")
               subprocess.call("adb.exe shell getprop ro.product.cpu.abi > arch.txt",shell=True)
               with open('arch.txt') as myfile:
                  arch = myfile.read()
               print("Spawning Root Shell... \n For exit type 'exit' two times or Control+C for terminate the script")
               # ty again t0x1cSH :)
               if "arm64-v8a" in arch:
                   subprocess.call("adb.exe push arm64/mtk-su /data/local/tmp",shell=True)
                   subprocess.call("adb shell chmod 755 /data/local/tmp/mtk-su",shell=True)
                   subprocess.call("adb shell /data/local/tmp/mtk-su",shell=True)
                   wait = input("PRESS ENTER TO CONTINUE.")
                   os.system('cls')
               elif "armeabi-v7a" in arch:
               # ty again again XD
                   subprocess.call("adb.exe push arm/mtk-su /data/local/tmp",shell=True)
                   subprocess.call("adb.exe shell chmod 755 /data/local/tmp/mtk-su",shell=True)
                   subprocess.call("adb.exe shell /data/local/tmp/mtk-su",shell=True)
                   wait = input("PRESS ENTER TO CONTINUE.")
                   os.system('cls')

        elif option=="3":
               break

        else:
               print("")
               input("Incorrect option...\nPress any key to continue..")
