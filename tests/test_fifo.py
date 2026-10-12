import os
import json
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer


@cocotb.test()
async def random_traffic(dut):
    seed = int(os.environ.get("RANDOM_SEED", "1"))
    rng = random.Random(seed)

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    dut.rst.value = 1
    dut.wr_en.value = 0
    dut.rd_en.value = 0
    dut.din.value = 0
    for _ in range(3):
        await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst.value = 0

    model = []
    depth = 8
    cov = {"cycles_run": 0, "empty_cycles": 0, "full_cycles": 0,
           "simultaneous_requests": 0, "writes_blocked_full": 0,
           "reads_blocked_empty": 0, "accepted_writes": 0,
           "accepted_reads": 0, "max_occupancy": 0}

    try:
        for cyc in range(2000):
            await FallingEdge(dut.clk)
            wr = rng.random() < 0.6
            rd = rng.random() < 0.4
            data = rng.randrange(256)

            occ = len(model)
            cov["cycles_run"] += 1
            cov["empty_cycles"] += occ == 0
            cov["full_cycles"] += occ == depth
            cov["simultaneous_requests"] += wr and rd
            cov["writes_blocked_full"] += wr and occ == depth
            cov["reads_blocked_empty"] += rd and occ == 0

            dut.wr_en.value = int(wr)
            dut.rd_en.value = int(rd)
            dut.din.value = data

            do_wr = wr and len(model) < depth
            do_rd = rd and len(model) > 0
            expected_data = model[0] if do_rd else None
            if do_rd:
                model.pop(0); cov["accepted_reads"] += 1
            if do_wr:
                model.append(data); cov["accepted_writes"] += 1
            cov["max_occupancy"] = max(cov["max_occupancy"], len(model))

            await RisingEdge(dut.clk)
            await Timer(1, units="ns")

            assert int(dut.full.value) == int(len(model) == depth), (
                f"full mismatch cycle={cyc}, actual={int(dut.full.value)}, "
                f"expected={int(len(model) == depth)}, occupancy={len(model)}, "
                f"wr={int(wr)}, rd={int(rd)}")
            assert int(dut.empty.value) == int(len(model) == 0), (
                f"empty mismatch cycle={cyc}, actual={int(dut.empty.value)}, "
                f"expected={int(len(model) == 0)}, occupancy={len(model)}")
            if do_rd:
                assert int(dut.dout.value) == expected_data, (
                    f"data mismatch cycle={cyc}, "
                    f"got={int(dut.dout.value)}, expected={expected_data}")
    finally:
        coverage_file = os.environ.get("COVERAGE_FILE")
        if coverage_file:
            out = Path(coverage_file)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps({k: int(v) for k, v in cov.items()}, indent=2))
