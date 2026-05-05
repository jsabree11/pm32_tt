# PM32 Multiplier

A 32-bit serial-parallel multiplier implemented in Verilog for Tiny Tapeout.

## How it works

The design loads two 32-bit operands one byte at a time using the Tiny Tapeout input pins. The PM32 multiplier then performs multiplication over multiple clock cycles and stores the 64-bit product internally.

Because Tiny Tapeout has only 8 output pins, the design outputs one selected byte of the 64-bit product at a time. The output select pins choose which product byte appears on `uo_out[7:0]`.

## How to test

Load the multiplicand and multiplier into the design using `ui_in[7:0]`, the byte select pins, and the load control pins. Then pulse the start signal. After the multiplication completes, the done signal goes high. Use the output select pins to read each byte of the 64-bit product on `uo_out[7:0]`.

