from datetime import datetime
import csv
import os
import os.path


HEADERS = ["TIMESTAMP", "CLASS", "DLVL", "NOTE"]


class Logger:
    def __init__(self):
        today = datetime.today()
        self.prefix = today.strftime("%Y%m%d_%H%M")
        self.suffix = "_log.csv"
        cwd = os.getcwd()
        self.directory: str = f"{str(cwd)}/logs/"

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        with open(
            f"{self.directory}{self.prefix}{self.suffix}", "w", newline=""
        ) as file:
            writer = csv.writer(file, quotechar="|", quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADERS)

    def append(self, _class: str = "Logger", level: str = "info", note: str = ""):
        time_stamp = datetime.today().strftime("%Y%m%d_%H%M%S")
        newRow = [time_stamp, _class, level, note]
        with open(
            f"{self.directory}{self.prefix}{self.suffix}", "a", newline=""
        ) as file:
            writer = csv.writer(file, quotechar="|", quoting=csv.QUOTE_MINIMAL)
            writer.writerow(newRow)
