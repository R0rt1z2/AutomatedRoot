# AutomatedRoot
![GitHub](https://img.shields.io/github/license/R0rt1z2/AutomatedRoot)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/R0rt1z2/AutomatedRoot?include_prereleases)
![GitHub All Releases](https://img.shields.io/github/downloads/R0rt1z2/AutomatedRoot/total)
[![GitHub Maintained](https://img.shields.io/badge/maintained-yes-purple.svg)](https://github.com/R0rt1z2/AutomatedRoot)
![GitHub Issues](https://img.shields.io/bitbucket/issues-raw/R0rt1z2/AutomatedRoot?color=red)
![Github Contributors](https://img.shields.io/github/contributors/R0rt1z2/AutomatedRoot)

Root MediaTek devices using `mtk-su` exploit (**CVE-2020-0069**).

## Requirements
* Python 3.9 or newer(in %PATH% for Windows).
* ADB (in %PATH% for Windows).
* The **CVE-2020-0069** PoC (`mtk-su`).

## Usage
* Download the mtk-su binaries from the [MediaTek's SU XDA page](https://forum.xda-developers.com/t/amazing-temp-root-for-mediatek-armv8-2020-08-24.3922213/) and move them to their corresponding folders (`automated_root/files/arm[64]`).
* Download the [latest release of the tool](https://github.com/R0rt1z2/AutomatedRoot/releases).
* If you're using Windows, open a PowerShell. If you're using Linux open a Terminal.
* Install the requirements with `pip3 install -r requirements.txt`.
* Run the script with Python: `python3 mtk-su.py`.

## Available options
1. Root the device. (system-mode + SuperSU).
2. Root the device. (bootless-mode + Magisk).
3. Unroot the device. (supports both bootless and system mode).

## License
* This tool is licensed under the GNU (v3) General Public License. See `LICENSE` for more details.
* `files/common/Initd.apk` is property of RYO Software.
* `files/common/Magisk.apk` and `files/arm[64]/magiskinit` are property of topjohnwu.
* `files/common/SuperSU.apk` and `files/arm[64]/{libsupol.so,su,supolicy}` are property of Chainfire.

## Special thanks
* diplomatic (XDA): the creator of the `mtk-su` (CVE-2020-0069) exploit and the `magisk-boot.sh` script.
* RYO Software: the creator of the Init.d Support App.
* Chainfire: the creator of SuperSU (and its binaries).
* topjohnwu: the creator of Magisk (and its binaries).