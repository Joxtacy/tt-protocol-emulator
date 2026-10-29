# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


async def reset(dut):
    # 20 ns period = 50 MHz, matching CLOCK_PERIOD in src/config.json
    clock = Clock(dut.clk, 20, unit="ns")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)


@cocotb.test()
async def test_counter_counts_when_enabled(dut):
    await reset(dut)
    assert dut.uo_out.value == 0

    dut.ui_in.value = 1
    await ClockCycles(dut.clk, 5)
    # Sampled just after the edge, so the 5th increment is not yet visible
    start = int(dut.uo_out.value)
    await ClockCycles(dut.clk, 100)
    assert int(dut.uo_out.value) == start + 100


@cocotb.test()
async def test_counter_holds_when_disabled(dut):
    await reset(dut)

    dut.ui_in.value = 1
    await ClockCycles(dut.clk, 20)
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 2)
    held = int(dut.uo_out.value)
    await ClockCycles(dut.clk, 50)
    assert int(dut.uo_out.value) == held


@cocotb.test()
async def test_counter_wraps(dut):
    await reset(dut)

    dut.ui_in.value = 1
    await ClockCycles(dut.clk, 300)
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 2)
    # 300 enabled cycles mod 256
    assert int(dut.uo_out.value) == 300 % 256
