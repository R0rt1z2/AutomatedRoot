import os

VERSION = "v7.0\n"
BANNER = """
     _____     _                 _         _ _____         _
    |  _  |_ _| |_ ___ _____ ___| |_ ___ _| | __  |___ ___| |_
    |     | | |  _| . |     | .'|  _| -_| . |    -| . | . |  _|
    |__|__|___|_| |___|_|_|_|__,|_| |___|___|__|__|___|___|_|  """

# Supported SoCs/Archs
REGIDX_ARCH = ["arm", "arm64"]
REGIDX_CPU = "(mt67|mt816|mt817|mt6580|mt6595)\s?(.*)"

# Menu options
MENU_OPTIONS = '''
    -> 1. Root the device (system-mode).
    -> 2. Root the device (bootless-mode).
    -> 3. Unroot the device.
    -> 4. Exit the tool.
'''

# Magisk Root (manual instructions)
MAGISK_INST = """[I]: Once the Init.d support app pops up, accept its terms and allow it to access media:
    -> Set 'Run scripts on boot time' to CHECKED.
    -> Set 'Execution delay' to NO DELAY.
    -> Set 'Selected folder' to init.d folder located in the Internal Storage.
    -> Click on 'Run scripts now' and watch the ad to unlock the feature. (Support the developer!)."""

# Clean stdout
CLEAN = ('cls' if os.name == 'nt' else 'clear')

# List of properties dumped by the script (debug)
REGIDX_PROP = {
    "ro.product.model": "Model",
    "ro.build.version.release": "Android Version",
    "ro.product.manufacturer": "Product Manufracturer",
    "ro.build.version.security_patch": "Security Patch"
}

# ADB (default) client IP
DEFAULT_IP = "127.0.0.1"

# PoC's result patterns
RESULT_PATTERN = "(All good|This firmware cannot be supported|Firmware support not implemented|Incompatible platform|permission denied)\s?(.*)"
