import argparse
import socket


class ClienteSocket:
    DIRECCION = "127.0.0.1"
    PUERTO = 65432
    MAX_MENSAJE = 4096

    def __init__(self, direccion=None, puerto=None):
        self.DIRECCION = direccion if direccion is not None else self.DIRECCION
        self.PUERTO = puerto if puerto is not None else self.PUERTO
        self.cliente = None
        self.buffer = bytearray()

    def conectar(self):
        if self.cliente is not None:
            return
        self.cliente = socket.create_connection((self.DIRECCION, self.PUERTO), timeout=5.0)
        self.cliente.settimeout(5.0)
        print(f"Conectado a {self.DIRECCION}:{self.PUERTO}")

    def enviar(self, mensaje):
        if self.cliente is None:
            raise ConnectionError("El cliente no está conectado")
        datos = mensaje.encode("utf-8")
        if b"\n" in datos or b"\r" in datos:
            raise ValueError("El mensaje no debe contener saltos de línea")
        if len(datos) > self.MAX_MENSAJE:
            raise ValueError("El mensaje supera el tamaño máximo permitido")
        self.cliente.sendall(datos + b"\n")

    def recibir(self):
        if self.cliente is None:
            raise ConnectionError("El cliente no está conectado")
        while True:
            indice = self.buffer.find(b"\n")
            if indice >= 0:
                if indice > self.MAX_MENSAJE:
                    raise ValueError("Respuesta demasiado larga")
                linea = bytes(self.buffer[:indice]).rstrip(b"\r")
                del self.buffer[:indice + 1]
                return linea.decode("utf-8")
            if len(self.buffer) > self.MAX_MENSAJE:
                raise ValueError("Respuesta demasiado larga")
            bloque = self.cliente.recv(1024)
            if not bloque:
                raise ConnectionError("El servidor cerró la conexión")
            self.buffer.extend(bloque)

    def desconectar(self):
        if self.cliente is not None:
            try:
                self.cliente.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self.cliente.close()
            self.cliente = None
            self.buffer.clear()
            print("Conexión cerrada")

    def iniciar(self):
        try:
            self.conectar()
            while True:
                mensaje = input("Escriba un mensaje (cerrar para salir): ")
                self.enviar(mensaje)
                respuesta = self.recibir()
                print(f"Servidor: {respuesta}")
                if mensaje.lower() == "cerrar" or respuesta.lower() == "cerrada":
                    break
        except (OSError, ConnectionError, UnicodeError, ValueError) as error:
            print(f"Error de comunicación: {error}")
        except (KeyboardInterrupt, EOFError):
            print("\nInterrumpido por el usuario")
        finally:
            self.desconectar()


def main():
    parser = argparse.ArgumentParser(description="Cliente TCP para ServidorSocket")
    parser.add_argument("--host", default="127.0.0.1", help="Dirección IP del servidor")
    parser.add_argument("--port", type=int, default=65432, help="Puerto TCP (predeterminado: 65432)")
    args = parser.parse_args()
    ClienteSocket(args.host, args.port).iniciar()


if __name__ == "__main__":
    main()
