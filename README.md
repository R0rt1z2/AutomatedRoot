# AutomatedRoot
![GitHub](https://img.shields.io/github/license/R0rt1z2/AutomatedRoot)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/R0rt1z2/AutomatedRoot?include_prereleases)
![GitHub All Releases](https://img.shields.io/github/downloads/R0rt1z2/AutomatedRoot/total)

Root MediaTek arm64 devices using `mtk-su` exploit (**CVE-2020-0069**).

## Requirements
* Python 3.X (with local path defined in windows).
* ADB (with local path defined in windows).
* `mtk-su` binary downloaded into the corresponding folder (`files/arm[64]`).

## Usage
```bash
./MTK-SU.sh # unix-based systems
./MTK-SU.bat # windows-based systems
```

## Available options
1. Root the device. (system-mode + SuperSU).
2. Unroot the device. (deleting su files and restoring original app_process).
3. Root the device. (bootless-mode + Magisk).

## Download
* Tool downloads are available at: [AutomatedRoot's releases page](https://github.com/R0rt1z2/AutomatedRoot/releases).
* `mtk-su` downloads are available at: [MediaTek's SU XDA page](https://forum.xda-developers.com/t/amazing-temp-root-for-mediatek-armv8-2020-08-24.3922213/).

## Reporting bugs
* If you find any bug create and report the issue [here](https://github.com/R0rt1z2/AutomatedRoot/issues).
* Feel free to use [this template](https://github.com/R0rt1z2/AutomatedRoot/blob/master/files/assets/bugreport.md) to help me to find out what's going on. 

## Special thanks
* diplomatic (xda): the creator of the `mtk-su` exploit.
* RYO Software: the creator of the Init.d Support App.

## License
* This tool is licensed under the GNU (v3) General Public License. See `LICENSE` for more details.
* `files/common/Initd.apk` is property of RYO Software.
* `files/common/Mafisk.apk` is property of topjohnwu.
* `files/common/SuperSU.apk` and `files/arm[64]` are property of chainfire.