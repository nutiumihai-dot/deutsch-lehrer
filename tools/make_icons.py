"""Generate the PWA icons without external libraries.

Design: a dark rounded square with three bars in the article colors
used throughout the app (der = blue, die = red, das = green).
Run: python -I tools/make_icons.py  (from the app folder)
"""
import struct
import sys
import zlib
from pathlib import Path

BG = (24, 28, 44)
BARS = [(59, 130, 246), (230, 72, 72), (34, 170, 110)]  # der, die, das


def rounded(x, y, size, r):
    cx = min(max(x, r), size - 1 - r)
    cy = min(max(y, r), size - 1 - r)
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r


def pixel(x, y, size, maskable):
    if not maskable and not rounded(x, y, size, int(size * 0.22)):
        return (0, 0, 0, 0)
    # bars live inside the central safe zone so maskable crops keep them
    left, right = int(size * 0.28), int(size * 0.72)
    bar_h = int(size * 0.09)
    gap = int(size * 0.05)
    top = (size - (3 * bar_h + 2 * gap)) // 2
    widths = [1.0, 0.78, 0.9]
    for i, color in enumerate(BARS):
        y0 = top + i * (bar_h + gap)
        x1 = left + int((right - left) * widths[i])
        if y0 <= y < y0 + bar_h and left <= x < x1:
            return color + (255,)
    return BG + (255,)


def png(size, maskable=False):
    rows = bytearray()
    for y in range(size):
        rows.append(0)
        for x in range(size):
            rows.extend(pixel(x, y, size, maskable))

    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)

    return (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(bytes(rows), 9))
            + chunk(b'IEND', b''))


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    (out / 'icon-192.png').write_bytes(png(192))
    (out / 'icon-512.png').write_bytes(png(512))
    (out / 'icon-maskable-512.png').write_bytes(png(512, maskable=True))
    print('icons written to', out)


if __name__ == '__main__':
    main()
