#!/usr/bin/env python3
"""
svg2png.py — resolve CSS custom properties in a keymap-drawer SVG,
             inject an explicit background rect, then export via cairosvg.

Usage:  python3 svg2png.py input.svg output.png [scale]
"""
import re, sys

def collect_vars(svg: str) -> dict:
    """Return --name: value declarations from the light-theme scope only.
    The @media (prefers-color-scheme: dark) block is stripped first so its
    variable definitions don't overwrite the light ones."""
    light_svg = re.sub(r'@media\s*\([^)]*prefers-color-scheme[^)]*\)\s*\{[^}]*\}',
                       '', svg, flags=re.DOTALL)
    defs = {}
    for m in re.finditer(r'--([\w-]+)\s*:\s*([^;}\n]+)', light_svg):
        defs[f'--{m.group(1)}'] = m.group(2).strip()
    return defs

def resolve_vars(svg: str, defs: dict) -> str:
    """Replace all var(--name) with the resolved colour value."""
    def sub(m):
        return defs.get(m.group(1), m.group(0))
    return re.sub(r'var\((--[\w-]+)\)', sub, svg)

def inject_bg_rect(svg: str, defs: dict) -> str:
    """Insert a background <rect> right after the opening <svg> tag so
    cairosvg renders the background colour (it ignores CSS background-color)."""
    bg = defs.get('--color-bg', '#ffffff')
    w  = re.search(r'<svg[^>]+width="([^"]+)"',  svg)
    h  = re.search(r'<svg[^>]+height="([^"]+)"', svg)
    if not w or not h:
        return svg
    rect = f'<rect width="{w.group(1)}" height="{h.group(1)}" fill="{bg}"/>'
    return re.sub(r'(<svg[^>]*>)', rf'\1{rect}', svg, count=1)

if len(sys.argv) < 3:
    print(f'Usage: {sys.argv[0]} input.svg output.png [scale]', file=sys.stderr)
    sys.exit(1)

src   = sys.argv[1]
dst   = sys.argv[2]
scale = sys.argv[3] if len(sys.argv) > 3 else '4'

svg  = open(src).read()
defs = collect_vars(svg)
svg  = resolve_vars(svg, defs)
svg  = inject_bg_rect(svg, defs)

try:
    import cairosvg
    cairosvg.svg2png(bytestring=svg.encode('utf-8'), write_to=dst, scale=float(scale))
except ImportError:
    # cairosvg not importable (e.g. installed via pipx) — fall back to CLI
    import subprocess, tempfile, os
    with tempfile.NamedTemporaryFile(suffix='.svg', mode='w', delete=False, encoding='utf-8') as tmp:
        tmp.write(svg)
        tmp_path = tmp.name
    try:
        r = subprocess.run(['cairosvg', tmp_path, '-o', dst, '-s', scale])
        sys.exit(r.returncode)
    finally:
        os.unlink(tmp_path)
