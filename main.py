#!/usr/bin/env python3
"""News-image entry, 19 November 2026.

Deterministic, stdlib-only (plus Pillow for the drawing in gen.py), no
network. Writes ONE image, entry.png, to the output directory and prints
its SHA-256. Two runs produce identical bytes.

Output directory, first writable wins:
  $MAKEFUN_OUTPUT_DIR, then /output, then ./output, then the temp dir.
(/output was read-only in the GTA6-01 grading sandbox, so never assume it.)
"""

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


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
    out = pick_output_dir()
    work = Path(tempfile.mkdtemp(prefix="news-image-20261119-"))
    try:
        subprocess.run([sys.executable, str(HERE / "gen.py")], cwd=work,
                       check=True)
        src = work / "entry.png"
        dst = out / "entry.png"
        shutil.copyfile(src, dst)
        digest = hashlib.sha256(dst.read_bytes()).hexdigest()
        print(f"entry.png: {dst} sha256 {digest}")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
