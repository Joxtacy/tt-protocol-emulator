# tt-protocol-emulator

Entry for the Jane Street Protocol Emulator ASIC competition
(https://blog.janestreet.com/protocol-emulator-asic-competition/): an open-source,
programmable bit-banging core (in the spirit of RP2040 PIO / TI PRU) that runs
protocols such as UART, SPI and I2C as software loaded after fabrication.

## Competition constraints

- Deadline: 2027-01-18. Winners go on the March 2027 IHP shuttle.
- Process: IHP 130nm CMOS5L through Tiny Tapeout (`ihp-sg13cmos5l`).
- Area: 6x4 tiles (`info.yaml`), ~0.7 mm², roughly 1K logic cells per tile.
  8x4 may become available later.
- Required protocols: UART, SPI, I2C. Stretch goals: low-speed USB, 10 Mbit Ethernet.
  Other ideas: JTAG, SWD, PS/2, CAN.
- Protocols must be reprogrammable after fabrication.
- Judged on novel functionality and novel design/verification methodology.
- Must stay open source.

## Design facts

- Top module: `tt_um_joxtacy_protocol_emu` in `src/project.v`.
- Pins: `ui_in[7:0]` inputs, `uo_out[7:0]` outputs, `uio_*[7:0]` bidirectional
  (`uio_oe` high = output). Every output must be driven.
- Clock: 50 MHz (`clock_hz` in `info.yaml`, `CLOCK_PERIOD` 20 ns in `src/config.json`).
  Do not edit `src/config.json` below its "DO NOT CHANGE" marker.
- Reset is synchronous, active low (`rst_n`).
- Prefer SRAM over flip-flops for instruction memory.
- Adding a source file: list it in both `info.yaml` `source_files` and
  `PROJECT_SOURCES` in `test/Makefile`. All sources live in `src/`.

## Commands

Python is managed with uv (Python 3.12; cocotb 2.0.1 does not build on 3.14).

```sh
cd test && uv run make -B                  # cocotb RTL tests (Icarus), writes tb.fst
verilator --lint-only -Wall src/*.v        # DECLFILENAME on project.v is expected
yosys -p "read_verilog src/*.v; synth -top tt_um_joxtacy_protocol_emu; stat"
```

The Yosys `stat` cell count is generic, not IHP cells, so treat it as a rough
area estimate. Real hardening (GDS), precheck and gate-level tests run in the
GitHub Actions `gds` workflow.

## Python dependencies

`pyproject.toml` and `uv.lock` are the source of truth. `test/requirements.txt`
is generated from the lockfile because the upstream Tiny Tapeout `gl_test`
action and the devcontainer install it with pip; CI fails if it drifts. After
changing dependencies:

```sh
uv export --no-hashes --no-annotate --format requirements-txt -o test/requirements.txt
```

## Version control

- Use `jj`, not `git` (colocated repo).
- Commit messages follow Conventional Commits:
  `<type>(<optional scope>): <summary>`, e.g. `feat(core): add wait-on-pin instruction`.
  Types: feat, fix, test, docs, refactor, perf, build, ci, chore.
