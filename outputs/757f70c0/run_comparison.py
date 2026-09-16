"""aviad12g's comparison driver for villa #1626, run as specified with two robustness changes.

Kept verbatim from the request: the env vars, the command list per side, the inputs, the
10-minute cap, JSON + combined stdout/stderr retained per side.

Changed, and reported back as such:
  1. `check=False` instead of `check=True`, recording each exit code. With `check=True` a failure
     on the first side raises before the second side runs, and the request explicitly wants a log
     even when a side fails ("a log of that limitation is enough").
  2. The four compiled `vc_spiral` .pyd files (built once with MSVC from the unmodified revision;
     the patch touches only a .py file) are copied into each tree's own
     `spiral-fitting/vc_spiral/`, as an editable install would place them.
"""
import os
from pathlib import Path
import subprocess
import sys
import time
import json

W = Path(r"D:/Competition/Vesuvius progress prizes/_repro1626")
original = (W / "original" / "spiral-fitting").resolve()
candidate = (W / "candidate" / "spiral-fitting").resolve()
bundle = (W / "bundle").resolve()
results = (W / "villa-pcl-gpu-comparison").resolve()
results.mkdir(exist_ok=False)
env = dict(os.environ, AGENTS_AGENT_MODE="1", PYTHONDONTWRITEBYTECODE="1",
           FIT_SPIRAL_COMPILE="0", FIT_SPIRAL_TRITON="0",
           FIT_SPIRAL_NUM_THREADS="2", OMP_NUM_THREADS="2", MKL_NUM_THREADS="2",
           FIT_SPIRAL_PATCH_LOAD_WORKERS="1", FIT_SPIRAL_PATCH_LOAD_IO_THREADS="1",
           WANDB_MODE="disabled", MPLCONFIGDIR=str(results / "matplotlib-cache"))
# Native modules are placed inside each tree's own spiral-fitting/vc_spiral/ (what an editable
# install does). A PYTHONPATH entry does NOT work: the source vc_spiral/ package next to the
# script shadows it, because the script's directory is first on sys.path.
summary = {}
for side, source in [("original", original), ("candidate", candidate)]:
    command = [sys.executable, str(source / "find_inconsistent_windings.py"),
               "--checkpoint", str(bundle / "sealed-baseline-seed17.ckpt"),
               "--patches-dir", str(bundle / "inputs/patches"),
               "--umbilicus", str(bundle / "inputs/umbilicus.json"),
               "--patch-id", "0000_mid_band_final"]
    for name in ["abs_winding.json", "relative_windings.json", "same_windings.json"]:
        command += ["--pcl", str(bundle / "inputs/pcl" / name)]
    command += ["--z-range", "10500,11500", "--max-hops", "0",
                "--step-size", "1.0", "--medial-weight", "4.0",
                "--detect-loops", "--no-min-fix", "--no-plot",
                "--output", str(results / (side + ".json"))]
    t0 = time.time()
    with (results / (side + ".log")).open("x") as log:
        try:
            rc = subprocess.run(command, env=env, cwd=results, stdout=log,
                                stderr=subprocess.STDOUT, timeout=600).returncode
        except subprocess.TimeoutExpired:
            rc = "timeout_600s"
    summary[side] = dict(exit=rc, seconds=round(time.time() - t0, 1),
                         json_written=(results / (side + ".json")).exists())
    print(side, summary[side], flush=True)
json.dump(summary, open(results / "summary.json", "w"), indent=1)
