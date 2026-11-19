"""news-image-20261119: publish the front page to /output/entry.png.

The entry is "The World in One Day" for Thursday 19 November 2026: a
newspaper front page whose photographs are AI illustrations drawn from
the day's reporting and whose headlines are set in type, so every word
is exactly as reported. The five stories are the GTA VI worldwide
launch, the US-Iran exchange of fire in the Gulf, the Democrats'
251-11 nomination of Hakeem Jeffries for Speaker, the Nvidia chief's
resignation, and Voyager 1's light-day milestone.

The runner does nothing but copy the finished picture: no network, no
clock, no dice, so two runs write identical bytes.
"""

import os
import pathlib
import struct

HERE = pathlib.Path(__file__).resolve().parent
PICTURE = HERE / "entry.png"
JPEG_START = b"\xff\xd8\xff"
JPEG_END = b"\xff\xd9"
MAX_BYTES = 1048576


def jpeg_dimensions(blob: bytes) -> tuple[int, int]:
    """Read width and height from the first SOF marker (stdlib only)."""
    pos = 2  # skip the SOI marker
    while pos + 9 <= len(blob):
        if blob[pos] != 0xFF:
            raise SystemExit("entry.png is not a well-formed JPEG")
        marker = blob[pos + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            height, width = struct.unpack(">HH", blob[pos + 5:pos + 9])
            return width, height
        if marker == 0xD9:
            break
        length = struct.unpack(">H", blob[pos + 2:pos + 4])[0]
        pos += 2 + length
    raise SystemExit("entry.png has no JPEG frame header")


def publish() -> None:
    out_dir = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        blob = PICTURE.read_bytes()
    except FileNotFoundError:
        raise SystemExit("entry.png is missing from the bundle")
    if len(blob) > MAX_BYTES:
        raise SystemExit("entry.png is over the 1 MiB limit")
    if not blob.startswith(JPEG_START) or not blob.endswith(JPEG_END):
        raise SystemExit("entry.png is not a complete JPEG")
    width, height = jpeg_dimensions(blob)
    if width > 1024 or height > 1024:
        raise SystemExit("entry.png is larger than 1024 by 1024")
    target = out_dir / "entry.png"
    target.write_bytes(blob)


if __name__ == "__main__":
    publish()
