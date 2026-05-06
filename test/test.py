import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles

async def reset(dut):
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)


async def load_word(dut, value, load_bit):
    # load_bit = 0 for mc, 1 for mp
    for byte_sel in range(4):
        byte = (value >> (8 * byte_sel)) & 0xFF

        dut.ui_in.value = byte
        dut.uio_in.value = (1 << load_bit) | (byte_sel << 3)

        await RisingEdge(dut.clk)

    dut.uio_in.value = 0
    await RisingEdge(dut.clk)


async def start_mult(dut):
    # uio_in[2] = start
    dut.uio_in.value = 0b00000100
    await RisingEdge(dut.clk)
    dut.uio_in.value = 0
    await RisingEdge(dut.clk)


async def wait_done(dut, max_cycles=100):
    for _ in range(max_cycles):
        await RisingEdge(dut.clk)
        if int(dut.uio_out.value) & 1:
            return
    raise AssertionError("Multiplier did not assert done")


async def read_product(dut):
    product = 0

    for out_sel in range(8):
        # uio_in[7:5] selects output byte
        dut.uio_in.value = out_sel << 5
        await RisingEdge(dut.clk)

        byte = int(dut.uo_out.value)
        product |= byte << (8 * out_sel)

    return product





@cocotb.test()
async def test_pm32_multiplier(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    test_cases = [
        (3, 5),
        (12, 7),
        (-1, 0),
        (9999, 9999),
        (0, 999),
        (1908, 2004),
        (0, 0),
    	(2147483647, (2**(32-1) - 1)),
    	(-1, 54),
    	(-2147483648, 1),
    	    ]

    for mc, mp in test_cases:
        await reset(dut)

        dut._log.info(f"Testing {mc} * {mp}")

        await load_word(dut, mc, load_bit=0)
        await load_word(dut, mp, load_bit=1)

        await start_mult(dut)
        await wait_done(dut)

        result = await read_product(dut)
        expected = (mc * mp) & ((1 << 64) - 1)

        assert result == expected, f"{mc} * {mp}: got {result}, expected {expected}"

    dut._log.info("All PM32 multiplier tests passed")
