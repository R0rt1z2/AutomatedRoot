<p align="center">
  <img src="https://github.com/R0rt1z2/AutomatedRoot/blob/master/files/images/banner.PNG?raw=true" alt="AutomatedRoot"/>
</p>

***WHAT IS THIS?***

This tool, will automatically root your 64 bit MediaTek based device using the mtk-su exploit (CVE-2020-0069) created/found by diplomatic@xda.
It will automatically check if your device has dm-verity, the arch, the android version, etc... And will push the required files to obtain full ROOT (Android 5.0 - 7.1) or bootless ROOT in any Android Version.

NOTE: It can also root a few 32 bit platforms such as mt6580 & mt6595.

***REQUERIMENTS:***
* Python 3.X. (With local path defined in windows).
* ADB. (With local path defined in windows).

***HOW TO USE THE TOOL?***
* Windows Users: double-Click on MTK-SU.bat.
* Linux Users: ```$ chmod a+x MTK-SU.sh && ./MTK-SU.sh```

***AVAILABLE OPTIONS:***
* Root the device. (System-mode using SuperSU).
* Spawn a root shell.
* Unroot the device. (Deleting su files and restoring original app_processes).
* Bootless root for devices with dm-verity enabled.

***DOWNLOAD:***
* Downloads: https://github.com/R0rt1z2/AutomatedRoot/releases (Latest release).

***REPORTING BUGS***
* If you find any bug in my tool, please create and report the issue [here](https://github.com/R0rt1z2/AutomatedRoot/issues).
* Use [this template](https://github.com/R0rt1z2/AutomatedRoot/blob/master/files/images/bugreport_template.md) to help me to find out what's going on. 

***SPECIAL THANKS TO:***
* diplomatic for create his MTK-SU and the bootless root method!
* RYO Software for the Initd Support App!
* t0x1cSH and uniminin for the help with the script.

***LICENSE:***
* This tool is licensed under the GNU General Public License.
* See LICENSE.MIT and LICENSE.GPL2 for more details.
