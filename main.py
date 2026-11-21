"""Passport spread of the Republic of Velmara.

The entry program for the make.fun bounty
"the-passport-page-of-a-countr-2-20261121-0318".

The picture itself is committed as entry.png (drawn locally with
Pillow by draw_passport.py). This program does exactly one thing:
copy that file to $MAKEFUN_OUTPUT_DIR/entry.png.

Standard library only: os, shutil, pathlib. No network, no Pillow,
no other imports, so it runs unchanged in the grading sandbox.
"""

import os
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent


def main() -> None:
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(REPO_ROOT / "entry.png", output_dir / "entry.png")


if __name__ == "__main__":
    main()
