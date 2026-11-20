#!/usr/bin/env python3
"""Entry point: render the front page and write it to the output dir.

The image is generated deterministically by artwork.py using only the
Python standard library (no Pillow, no font files), so it runs in the
competition sandbox exactly as shipped. The grader runs this program
with no network and the repository mounted read-only, so nothing is
written beside the code: the PNG bytes go straight to
/output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png).
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    # The grader runs python3 -P, which leaves the script's directory
    # off sys.path; put it back so `import artwork` always works.
    sys.path.insert(0, HERE)

import artwork


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as fh:
        fh.write(artwork.render_png())


if __name__ == "__main__":
    main()
