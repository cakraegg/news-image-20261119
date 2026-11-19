"""Deliver the finished front page for news-image-20261119 v2.

Thursday 19 November 2026, summed up in one dense broadsheet: 27
stories that were checked against the day's reporting -- the first
Trump-Xi-Putin meeting in Shenzhen, the worldwide GTA VI launch, and
Anthropic's record $81.3bn IPO at the top, plus a grid of smaller
stories, a world map, an "also on Thursday" list, and a date-check box
that names the big stories which actually broke on Wednesday 18
November, so they are not passed off as today's news.

The picture was laid out beforehand and ships next to this file as
entry.png. This program does not draw anything and does not fetch
anything: it reads those bytes, checks they really are one complete
JPEG inside the competition's limits, and copies them unchanged to
the output folder. No network, no clock, no randomness -- run it
twice and the two outputs are the same bytes.
"""

import os
import pathlib
import struct
import sys

HERE = pathlib.Path(__file__).resolve().parent
PICTURE = HERE / "entry.png"

START = b"\xff\xd8"  # JPEG start-of-image marker
END = b"\xff\xd9"    # JPEG end-of-image marker
MAX_BYTES = 1_048_576  # 1 MiB, the competition's image cap
MAX_SIDE = 1024        # longest allowed side in pixels

# Markers that open a frame segment (baseline, extended, progressive).
# Any other marker is either standalone or carries a length we skip over.
FRAME = (0xC0, 0xC1, 0xC2)


def die(why):
    """Stop with a clear error instead of delivering a broken picture."""
    print("error: " + why, file=sys.stderr)
    raise SystemExit(1)


def read_source():
    """Return the shipped picture, or stop if it is missing or too big."""
    try:
        blob = PICTURE.read_bytes()
    except FileNotFoundError:
        die("entry.png is missing next to main.py")
    if len(blob) > MAX_BYTES:
        die("entry.png is larger than 1 MiB")
    if not blob.startswith(START):
        die("entry.png is not a JPEG (no SOI marker)")
    if not blob.endswith(END):
        die("entry.png is not a complete JPEG (no EOI marker)")
    return blob


def jpeg_size(blob):
    """Return (width, height) read from the JPEG frame header.

    Walk the segments from the SOI marker, skipping each one by its
    declared length, until a frame segment gives the dimensions. A
    segment that claims to run past the end of the file, or a file with
    no frame segment at all, is rejected. The scan segment (SOS) ends
    the walk: entropy-coded data follows it up to the EOI marker that
    read_source already checked sits at the very end.
    """
    pos = 2
    size = None
    while pos + 9 <= len(blob):
        if blob[pos] != 0xFF:
            die("entry.png has a malformed JPEG segment")
        marker = blob[pos + 1]
        if marker in FRAME:
            height, width = struct.unpack(">HH", blob[pos + 5:pos + 9])
            size = (width, height)
        if marker == 0xD9 or marker == 0xDA:
            break
        if marker == 0x01 or 0xD0 <= marker <= 0xD7:
            pos += 2  # standalone marker, no length field
            continue
        length = struct.unpack(">H", blob[pos + 2:pos + 4])[0]
        if pos + 2 + length > len(blob):
            die("entry.png has a truncated JPEG segment")
        pos += 2 + length
    if size is None:
        die("entry.png has no JPEG frame header")
    if size[0] == 0 or size[1] == 0:
        die("entry.png has a zero dimension")
    return size


def main():
    """Validate the picture and hand it over to the output folder."""
    blob = read_source()
    width, height = jpeg_size(blob)
    if width > MAX_SIDE or height > MAX_SIDE:
        die("entry.png is larger than 1024 by 1024")
    out_dir = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.png").write_bytes(blob)


if __name__ == "__main__":
    main()
