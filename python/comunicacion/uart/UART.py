import serial


puerto_serie = serial.Serial()
puerto_serie.port = "/dev/ttyUSB0" # "COM3"
puerto_serie.baudrate = 115200
puerto_serie.parity  =  serial.PARITY_NONE
puerto_serie.stopbits = serial.STOPBITS_ONE
puerto_serie.bytesize = serial.EIGHTBITS

puerto_serie.timeout = 1

puerto_serie.open()
if puerto_serie.is_open:
    while True:
        res = puerto_serie.read(1)
        if res:
            print("Respuesta >>", ord(res))

puerto_serie.close()