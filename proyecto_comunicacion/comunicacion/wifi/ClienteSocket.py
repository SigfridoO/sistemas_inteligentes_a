import argparse
import socket
import threading


class ClienteSocket:
    DIRECCION = "127.0.0.1"
    PUERTO = 65432
    MAX_MENSAJE = 4096

    def __init__(self, direccion=None, puerto=None):
        self.DIRECCION = direccion if direccion is not None else self.DIRECCION
        self.PUERTO = puerto if puerto is not None else self.PUERTO
        self.cliente = None
        self.detener = threading.Event()
        self.hilo_recepcion = None

    def conectar(self):
        self.cliente = socket.create_connection((self.DIRECCION, self.PUERTO), timeout=5)
        self.cliente.settimeout(0.5)
        self.detener.clear()
        self.hilo_recepcion = threading.Thread(target=self.recibir, name="RecepcionTCP", daemon=True)
        self.hilo_recepcion.start()
        print(f"Conectado a {self.DIRECCION}:{self.PUERTO}")

    def enviar(self, mensaje):
        datos = mensaje.encode("utf-8")
        if b"\n" in datos or b"\r" in datos or len(datos) > self.MAX_MENSAJE:
            raise ValueError("Mensaje inválido o demasiado largo")
        if self.cliente is None or self.detener.is_set():
            raise ConnectionError("Cliente no conectado")
        self.cliente.sendall(datos + b"\n")

    def recibir(self):
        buffer = bytearray()
        try:
            while not self.detener.is_set():
                try:
                    bloque = self.cliente.recv(1024)
                except socket.timeout:
                    continue
                except OSError:
                    break
                if not bloque:
                    print("\nEl servidor cerró la conexión", flush=True)
                    break
                buffer.extend(bloque)
                while b"\n" in buffer:
                    indice = buffer.index(10)
                    if indice > self.MAX_MENSAJE:
                        print("Respuesta demasiado larga")
                        return
                    linea = bytes(buffer[:indice]).rstrip(b"\r")
                    del buffer[:indice + 1]
                    try:
                        mensaje = linea.decode("utf-8")
                    except UnicodeDecodeError:
                        print("Mensaje recibido con UTF-8 inválido")
                        continue
                    print(f"\nServidor: {mensaje}", flush=True)
                    if mensaje.lower() == "cerrada":
                        return
                if len(buffer) > self.MAX_MENSAJE:
                    print("Respuesta demasiado larga")
                    return
        finally:
            self.detener.set()

    def desconectar(self):
        self.detener.set()
        if self.cliente is not None:
            try:
                self.cliente.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self.cliente.close()
            self.cliente = None
        if self.hilo_recepcion is not None and threading.current_thread() is not self.hilo_recepcion:
            self.hilo_recepcion.join(timeout=2)
        print("Conexión cerrada")

    def iniciar(self):
        try:
            self.conectar()
            print("Escribe mensajes libremente; escribe 'cerrar' para desconectar.")
            while not self.detener.is_set():
                try:
                    mensaje = input("Cliente> ")
                except (KeyboardInterrupt, EOFError):
                    break
                self.enviar(mensaje)
                if mensaje.lower() == "cerrar":
                    self.detener.wait(0.3)
                    break
        except (OSError, ValueError, ConnectionError) as error:
            print(f"Error de comunicación: {error}")
        finally:
            self.desconectar()


def main():
    print("Prueba")
    parser = argparse.ArgumentParser(description="Cliente TCP bidireccional")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=65432)
    args = parser.parse_args()
    ClienteSocket(args.host, args.port).iniciar()


if __name__ == "__main__":
    main()
