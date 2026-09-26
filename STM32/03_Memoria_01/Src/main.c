#include <stdint.h>

volatile uint32_t global_value = 0x12345678U;

volatile uint32_t global_array[4] = {
    0x11111111U,
    0x22222222U,
    0x33333333U,
    0x44444444U
};

int main(void)
{
    volatile uint32_t local_value = 0xABCDEF01U;
    volatile uint32_t dummy;


    dummy = global_value;
    dummy = global_array[0];

    while (1)
    {
        local_value++;


        if (dummy == 0xFFFFFFFFU)
        {
            dummy = 0U;
        }
    }
}
