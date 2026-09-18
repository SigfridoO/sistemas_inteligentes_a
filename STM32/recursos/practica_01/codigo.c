/* 
 * Registro DEMCR (Debug Exception and Monitor Control Register).
 *
 * Este registro forma parte del bloque de depuración del núcleo Cortex-M4
 * y se encuentra en la dirección 0xE000EDFC.
 *
 * En esta práctica se utiliza el bit TRCENA (bit 24), cuya activación
 * habilita la infraestructura de traza del procesador. Esto permite
 * utilizar módulos como ITM (Instrumentation Trace Macrocell) y enviar
 * información de diagnóstico hacia el depurador.
 */
#define DEMCR                  *((volatile uint32_t*)0xE000EDFCU)

/*
 * ITM Stimulus Port 0.
 *
 * El ITM dispone de varios puertos de estímulo que pueden ser utilizados
 * por el software para enviar información de traza. En esta práctica se
 * utiliza exclusivamente el puerto 0 para transmitir caracteres.
 *
 * Cada carácter enviado mediante printf() terminará siendo escrito en
 * este registro y posteriormente será transportado mediante SWO hacia
 * el ST-LINK y finalmente hacia STM32CubeIDE.
 */
#define ITM_STIMULUS_PORT0     *((volatile uint32_t*)0xE0000000U)

/*
 * Registro ITM Trace Enable Register (TER).
 *
 * Este registro permite habilitar individualmente los diferentes
 * puertos de estímulo del ITM.
 *
 * Cada bit corresponde a un puerto. El bit 0 habilita el
 * ITM Stimulus Port 0, que es el utilizado en esta práctica.
 */
#define ITM_TRACE_EN           *((volatile uint32_t*)0xE0000E00U)


/*
 * Función: ITM_SendChar
 *
 * Envía un carácter hacia el ITM Stimulus Port 0.
 *
 * Parámetro:
 *   ch : carácter de 8 bits que se desea transmitir.
 *
 * Esta función forma parte de la ruta utilizada para redireccionar
 * la salida estándar de printf() hacia la consola SWV de STM32CubeIDE.
 *
 * La secuencia general es:
 *
 * printf()
 *     -> _write()
 *         -> ITM_SendChar()
 *             -> ITM Stimulus Port 0
 *                 -> SWO
 *                     -> ST-LINK
 *                         -> SWV ITM Data Console
 */
void ITM_SendChar(uint8_t ch)
{

    DEMCR |= (1U << 24);
    ITM_TRACE_EN |= (1U << 0);

    while (!(ITM_STIMULUS_PORT0 & 1U))
    {
    }

    ITM_STIMULUS_PORT0 = ch;
}