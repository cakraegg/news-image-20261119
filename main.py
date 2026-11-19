"""news-image-20261119 v2: deliver the finished front page.

The entry is a dense one-page broadsheet for Thursday 19 November 2026:
27 verified stories of the day -- the Shenzhen trilateral, GTA VI's launch,
the record Anthropic IPO, the ICJ's Myanmar ruling and 23 more -- drawn as
one 1024x1024 JPEG with a date check that names what is NOT today's news.

The picture itself was composed offline (PIL text over AI illustrations and
hand-drawn charts) and is shipped as entry.png beside this file. This
program only hands it over: it reads the bytes, proves they are one whole
JPEG inside the competition's limits, and writes them unchanged to the
output directory. No network, no clock, no randomness -- run it twice and
the two outputs are byte for byte the same file.
"""

import os
import pathlib
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = ROOT / "entry.png"

SOI = b"\xff\xd8"
EOI = b"\xff\xd9"
LIMIT_BYTES = 1_048_576
LIMIT_SIDE = 1024

# JPEG markers whose segments carry a frame header (baseline, extended,
# progressive). Other markers are skipped by their declared length.
FRAME_MARKERS = {0xC0, 0xC1, 0xC2}


def fail(message):
    """Abort with a plain error line; a bad picture must never be delivered."""
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def read_picture():
    """Load entry.png and reject anything that is not a JPEG of legal size."""
    try:
        data = SOURCE.read_bytes()
    except FileNotFoundError:
        fail("entry.png is missing from the bundle")
    if len(data) > LIMIT_BYTES:
        fail("entry.png is over the 1 MiB limit")
    if not data.startswith(SOI):
        fail("entry.png does not start with a JPEG SOI marker")
    if not data.endswith(EOI):
        fail("entry.png does not end with a JPEG EOI marker")
    return data


def frame_size(data):
    """Walk the JPEG segments and return (width, height) from the frame.

    The walk also proves the header region is not truncated: every
    segment's declared length must end inside the file. Once the scan
    data starts (SOS), entropy bytes follow until the EOI marker, which
    read_picture already verified sits at the very end of the file.
    """
    cursor = 2  # past SOI
    found = None
    while cursor + 9 <= len(data):
        if data[cursor] != 0xFF:
            fail("entry.png has a broken JPEG segment")
        marker = data[cursor + 1]
        if marker in FRAME_MARKERS:
            height, width = struct.unpack(">HH", data[cursor + 5:cursor + 9])
            found = (width, height)
        if marker == 0xD9:
            break
        if marker == 0xDA:  # start of scan: entropy data runs to EOI
            break
        if marker == 0x01 or 0xD0 <= marker <= 0xD7:
            cursor += 2  # standalone markers carry no length
            continue
        size = struct.unpack(">H", data[cursor + 2:cursor + 4])[0]
        if cursor + 2 + size > len(data):
            fail("entry.png has a truncated JPEG segment")
        cursor += 2 + size
    if found is None:
        fail("entry.png has no JPEG frame header")
    if found[0] == 0 or found[1] == 0:
        fail("entry.png has a zero-size JPEG frame")
    return found


def deliver():
    """Write the validated picture to the output directory."""
    blob = read_picture()
    width, height = frame_size(blob)
    if width > LIMIT_SIDE or height > LIMIT_SIDE:
        fail("entry.png is larger than 1024 by 1024")
    target_dir = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "entry.png").write_bytes(blob)


if __name__ == "__main__":
    deliver()
