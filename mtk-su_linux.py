import os
import subprocess

# By R0rt1z2
# All the credits goes to diplomatic for create his excellent MTK-SU!

#set null variables

def menu():
        """
        Fucntion to clean
        """
        os.system('clear')
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
             subprocess.call("adb shell getprop ro.boot.veritymode > verity.txt",shell=True)
             with open('verity.txt') as myfile:
               verity = myfile.read()
             subprocess.call("adb shell getprop debug.mtklog.netlog.Running > mtk.txt",shell=True)
             with open('mtk.txt') as myfile:
               mtk = myfile.read()
             subprocess.call("adb shell getprop ro.product.model > device.txt",shell=True)
             with open('device.txt') as myfile:
               device = myfile.read()
             subprocess.call("adb shell getprop ro.hardware > platform.txt",shell=True)
             with open('platform.txt') as myfile:
               platform = myfile.read()
             subprocess.call("adb shell getprop ro.product.cpu.abi > arch.txt",shell=True)
             with open('arch.txt') as myfile:
               arch = myfile.read()
             subprocess.call("adb shell getprop ro.build.version.release > android.txt",shell=True)
             with open('android.txt') as myfile:
               android = myfile.read()
             print("Device: " + device)
             print("ARCH: " + arch)
             print("Platform: " + platform)
             print("Android: " + android)
             print("--------------------------------------")
             if "enforcing" in verity:
                 print("Sorry! Your device seems to have DM-Verity, this method will not work. Exiting...")
                 break
             elif " " in verity:
                 continue
             # ty t0x1cSH
             if "mt6582" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt6580" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt6572" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt8127" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt6592" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt8695" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt8123" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt6577" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt6589" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt8121" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt8125" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt8135" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt8389" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt6582v" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt6592v" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt6582t" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt6592t" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt8135v" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt8317" in platform:
                 print("Incompatible CPU, exiting")
                 break
             elif "mt8317t" in platform:
                 print("Incompatible CPU, exiting")
                 break
             if "arm64-v8a" in arch:
                print("--------------------------------------")
                print("Detected arm64 arch.. Pushing arm64 mtk-su & files")
                subprocess.call("adb push arm64/mtk-su arm64/root.sh arm64/su arm64/supolicy arm64/libsupol.so /data/local/tmp",shell=True)
                print("--------------------------------------")
                print("Pushed files succsefully!")
                print("Rooting the device...")
                subprocess.call("adb install files/SuperSU.apk",shell=True)
                subprocess.call("adb shell chmod 755 /data/local/tmp/mtk-su",shell=True)
                subprocess.call("adb shell chmod 755 /data/local/tmp/root.sh",shell=True)
                subprocess.call('adb shell /data/local/tmp/mtk-su -c "/data/local/tmp/root.sh"',shell=True)
                wait = input("PRESS ENTER TO CONTINUE.")
                os.system('clear')
             # ty t0x1cSH
             elif "armeabi-v7a" in arch:
                print("Detected armv7 arch.. Pushing armv7 mtk-su & files")
                subprocess.call("adb push arm/mtk-su arm/root.sh arm/su arm/supolicy arm/libsupol.so /data/local/tmp",shell=True)
                print("--------------------------------------")
                print("Pushed files succsefully!")
                print("Rooting the device...")
                subprocess.call("adb install files/SuperSU.apk",shell=True)
                subprocess.call("adb shell chmod 755 /data/local/tmp/mtk-su",shell=True)
                subprocess.call("adb shell chmod 755 /data/local/tmp/root.sh",shell=True)
                subprocess.call('adb shell /data/local/tmp/mtk-su -c "/data/local/tmp/root.sh"',shell=True)



        elif option=="2":
               print("ROOT SHELL SPAWNER")
               subprocess.call("adb shell getprop ro.product.cpu.abi > arch.txt",shell=True)
               with open('arch.txt') as myfile:
                  arch = myfile.read()
               print("Spawning Root Shell... \n For exit type 'exit' two times or Control+C for terminate the script")
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
               break

        else:
               print("")
               input("Incorrect option...\nPress any key to continue..")
