	/* Debug Exception and Monitor Control Register base address */
	#define DEMCR                  *((volatile uint32_t*)0xE000EDFCU)
	
	/* ITM register addresses */
	#define ITM_STIMULUS_PORT0     *((volatile uint32_t*)0xE0000000U)
	#define ITM_TRACE_EN           *((volatile uint32_t*)0xE0000E00U)
	
	void ITM_SendChar(uint8_t ch)
	{
		/* Enable TRCENA */
		DEMCR |= (1U << 24);
		
		/* Enable stimulus port 0 */
		ITM_TRACE_EN |= (1U << 0);
		
		/* Read FIFO/status condition for stimulus port 0 */
		while (!(ITM_STIMULUS_PORT0 & 1U))
		{
		}
		
		/* Write character to ITM stimulus port 0 */
		ITM_STIMULUS_PORT0 = ch;
	}