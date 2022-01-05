import datetime

LOGGING_LEVELS = {
    "-1": "[U]",  # Unknown (Default)
    "0": "[I]",  # Info
    "1": "[W]",  # Warning
    "2": "[E]",  # Error
    "3": "[F]",  # Fatal Error
    "4": "[D]",  # Debug
    "5": "[V]",  # Verbose
}

def log(buf, prio=0):
    line = buf

    if (prio := str(prio)) in LOGGING_LEVELS:
        line = f"{LOGGING_LEVELS[prio]}: " + buf
    else:
        line = "[U]: " + buf

    print(line)

def die(msg, ecl):
    log(f"{msg}", ecl)
    exit(ecl)