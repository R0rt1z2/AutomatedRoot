import os
import time
import threading

import automated_root.utils.logger as logger
import automated_root.utils.config as config

class UserInputThread(threading.Thread):
    def __init__(self, msg = "* * * If your device is not authorized, authorize it now * * *", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.done = False
        self.msg = msg
        self.stop = False

    def run(self):
        print("")
        print(self.msg)
        print("")
        while not self.done:
            time.sleep(0.25)
        self.done = True

class Device:
    def __init__(self):
        self.dev = None
        self.serial = None
        self.arch = None
        self.cpu = None

    def find_device(self, client):
        devices = {}
        i = 0

        os.system(config.CLEAN)

        if len(client.devices()) == 0:
            logger.log("Waiting for device", 0)

        while len(client.devices()) == 0:
            time.sleep(0.25)

        if len(client.devices()) > 1:
            logger.log("Multiple devices found", 1)

            for device in client.devices():
                devices[i] = device.serial
                print(f"  => {i}: {device.serial}")
                i += 1

            opt = -1
            while opt == -1 or opt > len(client.devices()):
                try:
                    opt = int(input("[I]: Please select your device -> "))
                except ValueError:
                    pass

            self.serial = devices[opt]

        else:
            for device in client.devices():
                self.serial = device.serial

        self.dev = client.device(self.serial)
    
    def handshake(self):
        thread = UserInputThread()
        thread.start()
        while not thread.done:
            try:
                self.run_cmd(['ping', '-c', '1', config.DEFAULT_IP])
                thread.done = True
            except RuntimeError:
                pass

    def run_cmd(self, cmd):
        return self.dev.shell(" ".join(cmd)).rstrip()

    def install(self, name):
        return self.dev.install(name)
    
    def uninstall(self, name):
        return self.dev.uninstall(name)
    
    def is_installed(self, name):
        return self.dev.is_installed(name)

    def push(self, file, dst, perms='w+r'):
        self.dev.push(file, dst)
        self.set_perm(perms, dst)
    
    def pull(self, file, dst):
        return self.dev.pull(file, dst)

    def get_prop(self, name):
        return self.run_cmd(['getprop', name]).rstrip()
    
    def set_perm(self, perm, file):
        return self.run_cmd(['chmod', perm, file])
    
    def mv_file(self, src, dst):
        return self.run_cmd(['mv', '-f', src, dst])

    def dump_info(self, file):
        with open(file, 'w') as devinfo:
            for prop in config.REGIDX_PROP:
                devinfo.write(f'{config.REGIDX_PROP[prop]} -> {self.get_prop(prop)}\n')
        
        if self.get_prop('ro.product.cpu.abi') == 'armeabi-v7a':
            self.arch = 'arm'
        elif self.get_prop('ro.product.cpu.abi') == 'arm64-v8a':
            self.arch = 'arm64'
        
        self.cpu = self.get_prop('ro.hardware')