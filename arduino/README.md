# Prácticas de Microcontroladores

Este repositorio reúne las prácticas, ejemplos y recursos utilizados durante el desarrollo de la asignatura de **Microcontroladores**.

El objetivo es conservar una colección ordenada de programas que permita consultar, ejecutar y reutilizar los ejercicios realizados en clase y laboratorio. Conforme avance el curso se agregarán nuevas prácticas para diferentes dispositivos y plataformas.

Por el momento, la primera práctica se desarrolla con un **ESP32** utilizando **Arduino IDE**.

---

## Índice

- [Prácticas disponibles](#prácticas-disponibles)
- [Práctica 1. Hola mundo con ESP32](#práctica-1-hola-mundo-con-esp32)
- [Requisitos](#requisitos)
- [Estructura sugerida del repositorio](#estructura-sugerida-del-repositorio)
- [Enlaces útiles](#enlaces-útiles)
- [Convenciones de trabajo](#convenciones-de-trabajo)
- [Estado del repositorio](#estado-del-repositorio)

---

# Prácticas disponibles

| No. | Práctica | Plataforma | Entorno | Estado |
|---:|---|---|---|---|
| 1 | Hola mundo | ESP32 | Arduino IDE | Disponible |

Las prácticas siguientes se irán incorporando conforme avance el curso.

---

# Práctica 1. Hola mundo con ESP32

La primera práctica tiene como propósito verificar el funcionamiento básico de la plataforma de desarrollo y familiarizar al estudiante con el proceso completo de creación, compilación y ejecución de un programa para ESP32.

## Objetivos

Al finalizar la práctica, el estudiante será capaz de:

- reconocer la tarjeta ESP32 utilizada en el laboratorio;
- instalar y configurar el entorno de desarrollo;
- seleccionar correctamente la tarjeta y el puerto de comunicación;
- crear un programa básico;
- compilar el proyecto;
- cargar el programa en el ESP32;
- utilizar el monitor serial;
- comprobar la ejecución mediante mensajes de diagnóstico.

## Plataforma

```text
Microcontrolador / tarjeta: ESP32
Entorno de desarrollo: Arduino IDE
Lenguaje: C/C++ para Arduino
Comunicación de diagnóstico: Puerto serial
```

# Requisitos

## Hardware

- tarjeta ESP32;
- cable USB compatible;
- computadora;
- protoboard;
- cables de conexión;
- componentes electrónicos requeridos por cada práctica.

## Software

- Arduino IDE;
- soporte para tarjetas ESP32 instalado en Arduino IDE;
- controlador USB correspondiente a la tarjeta, cuando sea necesario.

---

# Estructura del repositorio

```text
practicas/
│
├── README.md
│
├── esp32/
│   ├── 00_holamundo/
│   │   └── 00_holamundo.ino
│   └── ...
│
├── stm32/
│   └── ...
│
└── recursos/
    ├── enlaces/
    ├── diagramas/
    └── documentacion/
```

Cada práctica deberá conservar, cuando sea posible:

- código fuente;
- descripción del ejercicio;
- conexiones utilizadas;
- configuración necesaria;
- resultado esperado;
- observaciones importantes.

---

# Enlaces útiles

Esta sección reúne recursos que pueden utilizarse durante las prácticas.

## Temporizador para Arduino

Ejemplo de temporizador para Arduino disponible en GitHub Gist:

https://gist.github.com/SigfridoO/ae2462603e3c8288c024dd8dde54b7fc

Este recurso puede utilizarse como referencia para ejercicios que requieran ejecutar acciones periódicas sin depender exclusivamente de retardos bloqueantes.

## Próximos enlaces

Se agregarán progresivamente recursos relacionados con:

- instalación y configuración de Arduino IDE;
- instalación del soporte para ESP32;
- documentación de ESP32;
- temporizadores;
- interrupciones;
- comunicación serial;
- I2C;
- SPI;
- sensores;
- actuadores.


