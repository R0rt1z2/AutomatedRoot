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
    print(f"{LOGGING_LEVELS.get(prio, LOGGING_LEVELS[str(prio)])}: {buf}")

def die(msg, ecl):
    log(f"{msg}\n", ecl)
    exit(ecl)
