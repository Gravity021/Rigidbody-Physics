# (c) Isaac Godman 2024

import time
import traceback

from .terminal_formatting import *

class Debug:
    _init_time = time.time()

    _messages = []

    _message_format = "[{0}][{1} : {2}][{3}] {4}\n"

    _colours = {
        "LOG":      [ANSI_PURPLE],
        "INFO":     [ANSI_BLUE],
        "WARNING":  [ANSI_YELLOW, ANSI_BOLD],
        "ERROR":    [ANSI_RED, ANSI_BOLD, ANSI_ITALIC]
    }
    
    def log(message):
        called_from = traceback.extract_stack()[-2]
        Debug._messages.append({
            "time": time.time() - Debug._init_time,
            "level": "LOG",
            # TODO: path should show class name
            "class_name": ".".join(called_from.filename.split("\\")[9:])[:-3] + "." + called_from.name,
            "line_no": called_from.lineno,
            "message": message,
        })

    def log_info(message):
        called_from = traceback.extract_stack()[-2]
        Debug._messages.append({
            "time": time.time() - Debug._init_time,
            "level": "INFO",
            "class_name": ".".join(called_from.filename.split("\\")[9:])[:-3] + "." + called_from.name,
            "line_no": called_from.lineno,
            "message": message,
        })

    def log_warning(message):
        called_from = traceback.extract_stack()[-2]
        Debug._messages.append({
            "time": time.time() - Debug._init_time,
            "level": "WARNING",
            "class_name": ".".join(called_from.filename.split("\\")[9:])[:-3] + "." + called_from.name,
            "line_no": called_from.lineno,
            "message": message,
        })
    
    def log_error(message):
        called_from = traceback.extract_stack()[-2]
        Debug._messages.append({
            "time": time.time() - Debug._init_time,
            "level": "ERROR",
            "class_name": ".".join(called_from.filename.split("\\")[9:])[:-3] + "." + called_from.name,
            "line_no": called_from.lineno,
            "message": message,
        })
    
    def print_logs():
        output_string = "\n-------- DEBUG LOG --------\n"
        
        maxLogLevelLength = 0
        maxClassLength = 0
        maxLineNoLength = 0
        for log in Debug._messages:
            maxLogLevelLength = max(maxLogLevelLength, len(log["level"]))
            maxClassLength = max(maxClassLength, len(log["class_name"]))
            maxLineNoLength = max(maxLineNoLength, len(str(log["line_no"])))
        
        for log in Debug._messages:
            output_string += Debug._message_format.format(
                f"{{:<{maxLogLevelLength}}}".format(log["level"]),
                f"{{:<{maxClassLength}}}".format(log["class_name"]),
                f"{{:<{maxLineNoLength}}}".format(log["line_no"]),
                f"{{:.7f}}".format(log["time"]),
                log["message"]
            )

        print(output_string)
    
    def print_pretty_logs():
        output_string = "\n-------- " + term_format("DEBUG LOG", ANSI_BRIGHT_BLUE) + " --------\n"
        
        maxLogLevelLength = 0
        maxClassLength = 0
        maxLineNoLength = 0
        for log in Debug._messages:
            maxLogLevelLength = max(maxLogLevelLength, len(log["level"]))
            maxClassLength = max(maxClassLength, len(log["class_name"]))
            maxLineNoLength = max(maxLineNoLength, len(str(log["line_no"])))
        
        for log in Debug._messages:
            output_string += Debug._message_format.format(
                term_format(f"{{:<{maxLogLevelLength}}}".format(log["level"]),      Debug._colours[log["level"]]),
                term_format(f"{{:<{maxClassLength}}}".format(log["class_name"]),    ANSI_GREEN),
                term_format(f"{{:<{maxLineNoLength}}}".format(log["line_no"]),      ANSI_GREEN),
                f"{{:.7f}}".format(log["time"]),
                log["message"]
            )

        print(output_string)