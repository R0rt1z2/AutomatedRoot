import os
import time
import subprocess

from ppadb.client import Client as AdbClient

from automated_root.utils import logger
from automated_root.utils import config
from automated_root.utils import mtksu

def main():
    os.system(config.CLEAN)
    try:
        subprocess.call(['adb', 'start-server'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)
    except Exception as e:
        logger.die(f"Could not start the ADB server ({e})!", 3)

    client = AdbClient(host=config.DEFAULT_IP, port=5037)
    print(config.BANNER, config.VERSION, config.MENU_OPTIONS)

    opt = 0
    while opt == 0 or opt > 4:
        try:
            opt = int(input("[I]: Please select >> "))
        except ValueError:
            pass

    if opt == 4:
        exit("")

    mtksu.cmd_handler(client, opt)

if __name__ == '__main__':
    main()
