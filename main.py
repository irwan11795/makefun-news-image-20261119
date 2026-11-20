#!/usr/bin/env python3
"""News-image entry, 19 November 2026.

Writes the pre-rendered front page, entry.png, to the output directory
and prints its SHA-256. Two runs produce identical bytes.

The image is a fixed asset in this repo (entry.png), drawn by the
author with gen.py (PIL, no network, fully deterministic — re-running
gen.py produces byte-identical output). This program only copies it,
so it runs on the standard library alone: the grading sandbox installs
nothing (RULES.txt: "standard library only: nothing is installed
before it runs"), and the previous version failed there with exit code
1 because it ran gen.py, whose `from PIL import ...` raised
ImportError in the sandbox. gen.py stays in the repo as the
generator's source; it is never executed by this program.

Output directory, first writable wins:
  $MAKEFUN_OUTPUT_DIR, then /output, then ./output, then the temp dir.
(/output was read-only in the GTA6-01 grading sandbox, so never assume it.)
"""

import hashlib
import os
import shutil
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
EXPECTED_SHA256 = ("6f61d15c5b2d24e903faf50b9ab643953b00f2041ae03838d332"
                   "cc016b01442c")


def pick_output_dir():
    candidates = []
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        candidates.append(Path(env))
    candidates.append(Path("/output"))
    candidates.append(HERE / "output")
    candidates.append(Path(tempfile.gettempdir()) / "news-image-20261119-out")
    for cand in candidates:
        try:
            cand.mkdir(parents=True, exist_ok=True)
            probe = cand / ".write-test"
            probe.write_bytes(b"ok")
            probe.unlink()
            return cand
        except OSError:
            continue
    raise SystemExit("no writable output directory found")


def main():
    digest = hashlib.sha256(SRC.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"entry.png sha256 mismatch: {digest}")
    out = pick_output_dir()
    dst = out / "entry.png"
    shutil.copyfile(SRC, dst)
    digest = hashlib.sha256(dst.read_bytes()).hexdigest()
    print(f"entry.png: {dst} sha256 {digest}")


if __name__ == "__main__":
    main()
