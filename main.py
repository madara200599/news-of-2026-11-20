#!/usr/bin/env python3
"""Entry point: draw the front page, then copy it to the output dir.

The image is generated deterministically by artwork.py (Pillow, stdlib
plus Pillow only for drawing). The grader runs this program with no
network; it writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png).
"""

import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    # Re-draw the image from scratch so the output is reproducible.
    subprocess.run([sys.executable, os.path.join(HERE, "artwork.py")],
                   check=True, cwd=HERE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
