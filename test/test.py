import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start PM32 smoke test")

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 5)

    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)

    assert dut.uo_out.value.is_resolvable
    assert dut.uio_out.value.is_resolvable

    dut._log.info("PM32 smoke test passed")
