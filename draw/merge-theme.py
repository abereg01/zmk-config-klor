#!/usr/bin/env python3
"""
Merge a base keymap-drawer config with a theme override file.

Uses only the Python standard library — no PyYAML required.

Usage:
    python3 merge-theme.py keymap-drawer.yaml themes/nord.yaml > /tmp/merged.yaml

The theme file's svg_style is *appended* to the base svg_style so that
the theme's CSS custom-property declarations (--color-* variables) override
the base defaults via the normal CSS cascade (last declaration wins).

The theme file may also override draw_config scalars such as dark_mode.
"""

import re
import sys


def read(path: str) -> str:
    with open(path) as fh:
        return fh.read()


def extract_block_scalar(text: str, key: str) -> str:
    """Return the indented content lines of a YAML block-scalar (key: |)."""
    pattern = rf'^\s*{re.escape(key)}:\s*\|\n((?:[ \t]+[^\n]*\n?)*)'
    m = re.search(pattern, text, re.MULTILINE)
    return m.group(1) if m else ""


def override_scalar(text: str, key: str, value: str) -> str:
    """Replace a simple inline YAML scalar: key: <value>  [# optional comment]"""
    return re.sub(
        rf'(^\s*{re.escape(key)}:\s*)\S+',
        rf'\g<1>{value}',
        text,
        count=1,
        flags=re.MULTILINE,
    )


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <base.yaml> <theme.yaml>", file=sys.stderr)
        sys.exit(1)

    base_text  = read(sys.argv[1])
    theme_text = read(sys.argv[2])

    # 1. Append the theme's svg_style CSS so its --color-* vars win via cascade.
    #    svg_style is always the last key in the base file, so appending to the
    #    end of the file is equivalent to appending inside the block scalar —
    #    YAML will read it as continuation of the same indented block.
    theme_style = extract_block_scalar(theme_text, "svg_style")
    if theme_style:
        base_text = base_text.rstrip("\n") + "\n" + theme_style

    # 2. Override dark_mode if the theme specifies it.
    m = re.search(r'^\s*dark_mode:\s*(true|false)', theme_text, re.MULTILINE)
    if m:
        base_text = override_scalar(base_text, "dark_mode", m.group(1))

    print(base_text, end="")


if __name__ == "__main__":
    main()
