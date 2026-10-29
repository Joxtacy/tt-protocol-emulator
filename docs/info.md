<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This is a placeholder for a programmable protocol emulator: a small core for bit-banging protocols
such as UART, SPI and I2C, reprogrammable after fabrication.

The current design is an 8-bit counter. While `ui_in[0]` (EN) is high, the counter increments on
every rising clock edge, and its value is driven on `uo_out[7:0]`. It wraps from 255 to 0.
Reset (`rst_n` low) clears it to 0.

## How to test

1. Hold `rst_n` low for a few clock cycles, then release it. `uo_out` reads 0.
2. Drive `ui_in[0]` high. `uo_out` counts up by one per clock cycle.
3. Drive `ui_in[0]` low. `uo_out` holds its value.

With a slow clock, LEDs on `uo_out` show the count in binary.

## External hardware

None.
