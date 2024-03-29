import time
import serial
import serial.tools.list_ports
from serial.tools.list_ports_common import ListPortInfo
from serial import Serial
from typing import Any
from GUI.constants import *


class SerialCom:
    def __init__(self, app: Any):
        self.offline = True
        self.isListening: bool = False
        self.arduino: Serial
        self.response = ""
        self.waitingResponse = False
        self.buffer = ""
        self.app = app

    def startListening(self):
        try:
            self.arduino = self.advancedSerialInit()
        except ConnectionError:
            self.app.file_log("serial", "error", "Arduino not found")
            return
        self.isListening = True
        self.offline = False

        self.app.file_log("serial", "info", "Serial connection established")
        while self.isListening:
            if not self.arduino.isOpen():  # type: ignore
                self.app.file_log("serial", "error", "Arduino is no longer connected")
                raise ConnectionError("Arduino is no longer connected")
            # data to send
            if self.buffer != "":
                self.arduino.write(f"{self.buffer}\n".encode())
                self.buffer = ""
            # data to read
            elif self.arduino.in_waiting:
                self.response = self.arduino.readline().decode("ascii").rstrip()
                if self.response != "":
                    self.waitingResponse = False

    def communicate(self, message: str) -> bool:
        """Send message via SERIAL PORT to PC
        :param message: message added to buffer
        :return: True if OFFLINE MODE or MESSAGE CONFIRMATION RECEIVED
        :raise: Connection error
        ---------
        :arg: "T" for test communication
        :arg: "S" for short exposure - most used
        :arg: "L" for long exposure - mA calibration only
        """
        if self.offline:
            self.app.file_log("serial", "warning", "Working in offline mode")
            return True

        print("message to send", message)
        res = self.write2Read(message)
        if res == message:
            return True
        self.app.file_log("serial", "error", "Message not responded")
        return False

    def start_short(self):
        message = "S"
        return self.communicate(message)

    def start_long(self):
        message = "L"
        if self.communicate(message):
            return True
        return False

    def end(self):
        return self.communicate("X")

    def endListening(self) -> bool:
        try:
            if not self.communicate("X"):
                return False
            self.offline = True
            self.isListening = False
            self.arduino.close()  # type: ignore
            time.sleep(2)
            self.app.file_log("serial", "info", "Port closed")

        except AttributeError:
            self.app.file_log("serial", "error", "Port not closed")
            return False
        except NameError:
            self.app.file_log("serial", "error", "Port not closed")
            return False
        else:
            return True

    def is_listening(self) -> bool:
        return self.isListening

    def is_offline(self) -> bool:
        return self.offline

    def write2Read(self, message: str):
        self.waitingResponse = True
        self.buffer = message
        while self.waitingResponse:
            pass
        return self.response

    def getPorts(self) -> list[ListPortInfo]:
        ports: list[ListPortInfo] = serial.tools.list_ports.comports()
        return ports

    def findItem(self, portsFound: list[ListPortInfo], matchingText: str) -> str:  # type: ignore
        commPort = ""
        numConnections = len(portsFound)  # type: ignore
        for i in range(0, numConnections):
            port = portsFound[i]  # type: ignore
            strPort = str(port)  # type: ignore
            if matchingText in strPort:
                splitPort = strPort.split(" ")
                commPort = splitPort[0]
        return commPort

    def advancedSerialInit(self) -> serial.Serial:
        portName = "CH340"
        foundPorts: list[ListPortInfo] = self.getPorts()
        connectPort = self.findItem(foundPorts, portName)
        if connectPort == "":
            raise ConnectionError("arduino not found")
        return serial.Serial(connectPort, 9600)
