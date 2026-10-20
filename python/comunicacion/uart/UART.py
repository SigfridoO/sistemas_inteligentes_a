import serial

class PuertoSerie:
    def __init__(self, puerto, baudrate):
        self.puerto = puerto
        self.baudrate = baudrate
        self.serial_port = serial.Serial()

    def abrir(self):
        self.serial_port.port = self.puerto
        self.serial_port.baudrate = self.baudrate
        self.serial_port.parity = serial.PARITY_NONE
        self.serial_port.stopbits = serial.STOPBITS_ONE
        self.serial_port.bytesize = serial.EIGHTBITS
        self.serial_port.timeout = 1

        self.serial_port.open()
        if self.serial_port.is_open:
            print(f"Puerto {self.puerto} abierto a {self.baudrate} baudios.")

    def leer(self):
        if self.serial_port.is_open:
            res = self.serial_port.read(1)
            if res:
                return ord(res)
        return None

    def escribir(self, data):
        if self.serial_port.is_open:
            self.serial_port.write(bytes([data]))
            print(f"Escrito: {data}")   
            
    def cerrar(self):
        if self.serial_port.is_open:
            self.serial_port.close()
            print(f"Puerto {self.puerto} cerrado.")

