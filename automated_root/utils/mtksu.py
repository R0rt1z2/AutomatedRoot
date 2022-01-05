import os
import re
import sys
import glob

from automated_root.utils.device import Device
from automated_root.utils.switch import Switch

import automated_root.utils.logger as logger
import automated_root.utils.config as config

def cmd_handler(client, opt):
    os.system(config.CLEAN)

    dev = Device()
    dev.find_device(client)

    os.system(config.CLEAN)
    print(config.BANNER, '\n')
    logger.log("Found device = {}".format(dev.serial))

    logger.log("Handshake")
    dev.handshake()

    logger.log("Dump device info")
    dev.dump_info("devinfo.txt")

    m = re.search(config.REGIDX_CPU, dev.cpu)

    if not m or m.group(1) not in dev.cpu:
        logger.die("Invalid platform: {}".format(dev.cpu), 3)

    if dev.arch not in config.REGIDX_ARCH:
        logger.die("Invalid arch: {}".format(dev.arch), 3)

    logger.log("Valid device = {} ({})".format(dev.cpu, dev.arch))

    if not os.path.isfile(f'automated_root/files/{dev.arch}/mtk-su'):
        logger.die("Missing mtk-su binaries!", 3)

    logger.log("Send files")
    for file in os.listdir('automated_root/files/common'):
        dev.push(f'automated_root/files/common/{file}', f'/data/local/tmp/{file}', perms='a+x')

    for file in os.listdir(f'automated_root/files/{dev.arch}'):
        dev.push(f'automated_root/files/{dev.arch}/{file}', f'/data/local/tmp/{dev.arch}/{file}', perms='a+x')

    with Switch(opt) as s:
        if s.case(1):
            if not dev.is_installed('eu.chainfire.supersu'):
                dev.install(f'automated_root/files/common/SuperSU.apk')

            logger.log("Let's rock")

            root_cmd = [
                f'/data/local/tmp/{dev.arch}/mtk-su',
                '-c', '/data/local/tmp/root.sh' ]

            logger.log("Wait for the script to finish")

            try:
                result = dev.run_cmd(root_cmd).replace('\n', ' - ')
            except Exception as e:
                logger.die("Something went horribly while trying to root the device ({})".format(e), 3)

            m = re.search(config.RESULT_PATTERN, result)

            if m and "All good" in m.group(1):
                logger.log(m.group(1))
            else:
                try:
                    logger.log("Couldn't root the device ({})".format(m.group(1)), 2)
                except Exception:
                    logger.log("Couldn't root the device ({})".format(result), 2)

            exit("")

        if s.case(2):
            if not dev.is_installed('com.topjohnwu.magisk'):
                dev.install(f'automated_root/files/common/Magisk.apk')

            if not dev.is_installed('com.ryosoftware.initd'):
                dev.install(f'automated_root/files/common/InitD.apk')

            logger.log("Let's rock")

            root_cmd = [
                '/data/local/tmp/magisk-root.sh' ]

            logger.log("Follow on-screen instructions, please")
            print(config.MAGISK_INST)

            try:
                result = dev.run_cmd(root_cmd).replace('\n', ' - ')
            except Exception as e:
                logger.die("Something went horribly while trying to root the device ({})".format(e), 3)

            m = re.search(config.RESULT_PATTERN, result)

            if m and "All good" in m.group(1):
                logger.log(m.group(1))
            else:
                try:
                    logger.log("Couldn't root the device ({})".format(m.group(1)), 2)
                except Exception:
                    logger.log("Couldn't root the device ({})".format(result), 2)

            exit("")

        if s.case(3):
            if dev.is_installed('eu.chainfire.supersu'):
                dev.uninstall('eu.chainfire.supersu')

            if dev.is_installed('com.topjohnwu.magisk'):
                dev.uninstall('com.topjohnwu.magisk')

            if dev.is_installed('com.ryosoftware.initd'):
                dev.uninstall('com.ryosoftware.initd')

            logger.log("Let's rock")

            unroot_cmd = [
                f'/data/local/tmp/{dev.arch}/mtk-su',
                '-c', '/data/local/tmp/unroot.sh' ]

            logger.log("Wait for the script to finish")

            try:
                result = dev.run_cmd(unroot_cmd).replace('\n', ' - ')
            except Exception as e:
                logger.die("Something went horribly while trying to unroot the device ({})".format(e), 3)

            m = re.search(config.RESULT_PATTERN, result)

            if m and "All good" in m.group(1):
                logger.log(m.group(1))
            else:
                try:
                    logger.log("Couldn't unroot the device ({})".format(m.group(1)), 2)
                except Exception:
                    logger.log("Couldn't unroot the device ({})".format(result), 2)

            exit("")

        if s.default():
            logger.die("Invalid option: {}".format(opt), 3)
