import argparse
import socket
import threading


class ServidorSocket:
    DIRECCION = "0.0.0.0"
    PUERTO = 65432
    MAX_MENSAJE = 4096

    def __init__(self, direccion=None, puerto=None):
        self.DIRECCION = direccion if direccion is not None else self.DIRECCION
        self.PUERTO = puerto if puerto is not None else self.PUERTO
        self.servidor = None
        self.clientes = set()
        self.hilos = set()
        self.bloqueo = threading.Lock()
        self.detener = threading.Event()
        print(f"Inicializando servidor en {self.DIRECCION}:{self.PUERTO}")

    def procesar_mensaje(self, mensaje, direccion):
        # Punto de extensión para futuras instrucciones del ESP32.
        print(f"[{direccion[0]}:{direccion[1]}] Recibido: {mensaje}")
        if mensaje.lower() == "cerrar":
            return "cerrada"
        return "aceptada"

    def atender_cliente(self, cliente_socket, cliente_direccion):
        print(f"Cliente conectado: {cliente_direccion[0]}:{cliente_direccion[1]}")
        buffer = bytearray()
        try:
            cliente_socket.settimeout(1.0)
            with cliente_socket:
                while not self.detener.is_set():
                    try:
                        bloque = cliente_socket.recv(1024)
                    except socket.timeout:
                        continue
                    except OSError:
                        break
                    if not bloque:
                        break
                    buffer.extend(bloque)
                    while b"\n" in buffer:
                        indice = buffer.index(10)
                        if indice > self.MAX_MENSAJE:
                            cliente_socket.sendall(b"error: mensaje demasiado largo\n")
                            return
                        linea = bytes(buffer[:indice]).rstrip(b"\r")
                        del buffer[:indice + 1]
                        try:
                            mensaje = linea.decode("utf-8")
                        except UnicodeDecodeError:
                            cliente_socket.sendall(b"error: UTF-8 invalido\n")
                            continue
                        try:
                            respuesta = self.procesar_mensaje(mensaje, cliente_direccion)
                        except Exception as error:
                            print(f"Error procesando mensaje de {cliente_direccion}: {error}")
                            cliente_socket.sendall(b"error: procesamiento fallido\n")
                            continue
                        cliente_socket.sendall((respuesta + "\n").encode("utf-8"))
                        if respuesta == "cerrada":
                            return
                    if len(buffer) > self.MAX_MENSAJE:
                        cliente_socket.sendall(b"error: mensaje demasiado largo\n")
                        break
        except (ConnectionResetError, BrokenPipeError, OSError) as error:
            print(f"Conexión interrumpida ({cliente_direccion}): {error}")
        finally:
            with self.bloqueo:
                self.clientes.discard(cliente_socket)
                self.hilos.discard(threading.current_thread())
            print(f"Cliente desconectado: {cliente_direccion[0]}:{cliente_direccion[1]}")

    def iniciar(self):
        self.detener.clear()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            self.servidor = servidor
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.bind((self.DIRECCION, self.PUERTO))
            servidor.listen(10)
            servidor.settimeout(1.0)
            print(f"Escuchando en {self.DIRECCION}:{servidor.getsockname()[1]}")
            try:
                while not self.detener.is_set():
                    try:
                        cliente_socket, cliente_direccion = servidor.accept()
                    except socket.timeout:
                        continue
                    except OSError:
                        if self.detener.is_set():
                            break
                        raise
                    hilo = threading.Thread(
                        target=self.atender_cliente,
                        args=(cliente_socket, cliente_direccion),
                        daemon=True,
                        name=f"TCP-{cliente_direccion[0]}:{cliente_direccion[1]}"
                    )
                    with self.bloqueo:
                        self.clientes.add(cliente_socket)
                        self.hilos.add(hilo)
                    hilo.start()
            except KeyboardInterrupt:
                print("\nDeteniendo servidor...")
            finally:
                self.detener.set()
                with self.bloqueo:
                    clientes = list(self.clientes)
                    hilos = list(self.hilos)
                for cliente in clientes:
                    try:
                        cliente.shutdown(socket.SHUT_RDWR)
                    except OSError:
                        pass
                    cliente.close()
                for hilo in hilos:
                    hilo.join(timeout=2.0)
                self.servidor = None
                print("Servidor cerrado")

    def cerrar(self):
        self.detener.set()
        if self.servidor is not None:
            try:
                self.servidor.close()
            except OSError:
                pass

    def __str__(self):
        return f"ServidorSocket(DIRECCION={self.DIRECCION}, PUERTO={self.PUERTO})"


def main():
    parser = argparse.ArgumentParser(description="Servidor TCP multicliente para pruebas de comunicación")
    parser.add_argument("--host", default="0.0.0.0", help="Interfaz de escucha")
    parser.add_argument("--port", type=int, default=65432, help="Puerto TCP (predeterminado 65432)")
    args = parser.parse_args()
    ServidorSocket(args.host, args.port).iniciar()


if __name__ == "__main__":
    main()
