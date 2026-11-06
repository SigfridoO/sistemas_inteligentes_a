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
        self.clientes = {}  # id: (socket, direccion)
        self.hilos = set()
        self.siguiente_id = 1
        self.bloqueo = threading.Lock()
        self.detener = threading.Event()

    def enviar(self, cliente_id, mensaje):
        datos = mensaje.encode("utf-8")
        if b"\n" in datos or b"\r" in datos or len(datos) > self.MAX_MENSAJE:
            raise ValueError("Mensaje inválido o demasiado largo")
        with self.bloqueo:
            cliente = self.clientes.get(cliente_id)
        if cliente is None:
            return False
        try:
            cliente[0].sendall(datos + b"\n")
            return True
        except OSError:
            return False

    def enviar_todos(self, mensaje):
        with self.bloqueo:
            ids = list(self.clientes)
        return sum(self.enviar(identificador, mensaje) for identificador in ids)

    def mostrar_clientes(self):
        with self.bloqueo:
            clientes = [(i, d) for i, (_, d) in self.clientes.items()]
        if not clientes:
            print("No hay clientes conectados", flush=True)
        for identificador, direccion in clientes:
            print(f"[{identificador}] {direccion[0]}:{direccion[1]}", flush=True)

    def procesar_mensaje(self, mensaje, direccion, cliente_id):
        print(f"\n[Cliente {cliente_id} | {direccion[0]}:{direccion[1]}] {mensaje}", flush=True)
        # Punto de integración futuro para las instrucciones ESP32.
        # No responde automáticamente: cada extremo puede escribir libremente.

    def atender_cliente(self, cliente_socket, cliente_direccion, cliente_id):
        buffer = bytearray()
        try:
            cliente_socket.settimeout(0.5)
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
                        self.enviar(cliente_id, "error: mensaje demasiado largo")
                        return
                    linea = bytes(buffer[:indice]).rstrip(b"\r")
                    del buffer[:indice + 1]
                    try:
                        mensaje = linea.decode("utf-8")
                    except UnicodeDecodeError:
                        self.enviar(cliente_id, "error: UTF-8 invalido")
                        continue
                    if mensaje.lower() == "cerrar":
                        self.enviar(cliente_id, "cerrada")
                        return
                    self.procesar_mensaje(mensaje, cliente_direccion, cliente_id)
                if len(buffer) > self.MAX_MENSAJE:
                    self.enviar(cliente_id, "error: mensaje demasiado largo")
                    break
        finally:
            with self.bloqueo:
                self.clientes.pop(cliente_id, None)
                self.hilos.discard(threading.current_thread())
            try:
                cliente_socket.close()
            except OSError:
                pass
            print(f"Cliente {cliente_id} desconectado", flush=True)

    def _aceptar_clientes(self):
        while not self.detener.is_set():
            try:
                cliente_socket, direccion = self.servidor.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            with self.bloqueo:
                identificador = self.siguiente_id
                self.siguiente_id += 1
                self.clientes[identificador] = (cliente_socket, direccion)
                hilo = threading.Thread(target=self.atender_cliente,
                    args=(cliente_socket, direccion, identificador),
                    name=f"TCP-Cliente-{identificador}", daemon=True)
                self.hilos.add(hilo)
            hilo.start()
            print(f"Cliente {identificador} conectado: {direccion[0]}:{direccion[1]}", flush=True)

    def consola(self):
        print("Comandos: /clientes | /enviar ID mensaje | /todos mensaje | /salir", flush=True)
        print("Escribir un mensaje sin comando lo envía a todos.", flush=True)
        while not self.detener.is_set():
            try:
                texto = input("Servidor> ").strip()
            except (KeyboardInterrupt, EOFError):
                break
            if not texto:
                continue
            if texto == "/salir":
                break
            if texto == "/clientes":
                self.mostrar_clientes()
            elif texto.startswith("/enviar "):
                partes = texto.split(" ", 2)
                if len(partes) != 3 or not partes[1].isdigit():
                    print("Uso: /enviar ID mensaje")
                elif not self.enviar(int(partes[1]), partes[2]):
                    print("No se pudo enviar: cliente desconectado o ID incorrecto")
            else:
                mensaje = texto[7:] if texto.startswith("/todos ") else texto
                try:
                    enviados = self.enviar_todos(mensaje)
                    print(f"Mensaje enviado a {enviados} cliente(s)")
                except ValueError as error:
                    print(error)

    def iniciar(self, consola=True):
        self.detener.clear()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.bind((self.DIRECCION, self.PUERTO))
            servidor.listen(10)
            servidor.settimeout(0.5)
            self.servidor = servidor
            print(f"Servidor escuchando en {self.DIRECCION}:{servidor.getsockname()[1]}", flush=True)
            aceptador = threading.Thread(target=self._aceptar_clientes, daemon=True, name="AceptadorTCP")
            aceptador.start()
            try:
                if consola:
                    self.consola()
                else:
                    self.detener.wait()
            finally:
                self.cerrar()
                aceptador.join(timeout=2)
                with self.bloqueo:
                    hilos = list(self.hilos)
                for hilo in hilos:
                    hilo.join(timeout=2)
                self.servidor = None
                print("Servidor cerrado", flush=True)

    def cerrar(self):
        self.detener.set()
        if self.servidor is not None:
            try:
                self.servidor.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
        with self.bloqueo:
            clientes = [socket_cliente for socket_cliente, _ in self.clientes.values()]
        for cliente in clientes:
            try:
                cliente.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            cliente.close()


def main():
    parser = argparse.ArgumentParser(description="Servidor TCP bidireccional multicliente")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=65432)
    args = parser.parse_args()
    ServidorSocket(args.host, args.port).iniciar()


if __name__ == "__main__":
    main()
