#!/usr/bin/env python3
"""Render a minimal flat-style status badge as a standalone SVG.

Offline by design: no network access, no third-party package (shields.io,
badge-maker, ...) -- this is what lets CI badges avoid depending on any
external server. Width is estimated per character rather than measured via a
real font metrics table, which is fine for the short label/value strings CI
badges use; it will not pixel-match shields.io.
"""
import sys

COLORS = {
    "brightgreen": "#4c1",
    "green": "#97ca00",
    "yellowgreen": "#a4a61d",
    "yellow": "#dfb317",
    "orange": "#fe7d37",
    "red": "#e05d44",
    "lightgrey": "#9f9f9f",
    "blue": "#007ec6",
}

CHAR_WIDTH = 6.5
PAD = 10
HEIGHT = 20


def text_width(text):
    return round(len(text) * CHAR_WIDTH) + 2 * PAD


def render(label, value, color):
    fill = COLORS.get(color, color if color.startswith("#") else COLORS["lightgrey"])
    label_w = text_width(label)
    value_w = text_width(value)
    total_w = label_w + value_w
    label_x = label_w / 2
    value_x = label_w + value_w / 2
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{HEIGHT}" role="img" aria-label="{label}: {value}">
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="r">
    <rect width="{total_w}" height="{HEIGHT}" rx="3" fill="#fff"/>
  </clipPath>
  <g clip-path="url(#r)">
    <rect width="{label_w}" height="{HEIGHT}" fill="#555"/>
    <rect x="{label_w}" width="{value_w}" height="{HEIGHT}" fill="{fill}"/>
    <rect width="{total_w}" height="{HEIGHT}" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">
    <text x="{label_x}" y="14">{label}</text>
    <text x="{value_x}" y="14">{value}</text>
  </g>
</svg>
"""


def main(argv):
    if len(argv) != 5:
        print(f"usage: {argv[0]} <label> <value> <color> <output.svg>", file=sys.stderr)
        print(f"colors: {', '.join(COLORS)} (or a #rrggbb hex value)", file=sys.stderr)
        return 1
    _, label, value, color, output_path = argv
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(render(label, value, color))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
