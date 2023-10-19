from datetime import datetime
import csv

HEADERS = ['TIMESTAMP', 'CLASS', 'DLVL', 'NOTE']


class Logger:
    def __init__(self):
        today = datetime.today()
        self.prefix = today.strftime("%Y%m%d_%H%M")
        self.suffix = '_log.csv'
        with open(f'{self.prefix}{self.suffix}', 'w', newline='') as file:
            writer = csv.writer(file, quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADERS)

    def append(self, _class='Logger', dlvl='info', note=''):
        time_stamp = datetime.today().strftime("%Y%m%d_%H%M%S")
        newRow = [time_stamp, _class, dlvl, note]
        with open(f'{self.prefix}{self.suffix}', 'a', newline='') as file:
            writer = csv.writer(file, quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(newRow)
