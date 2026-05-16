#!/usr/bin/env python3
"""
Merge a base keymap-drawer config with a theme override file.

Usage:
    python3 merge-theme.py keymap-drawer.yaml themes/nord.yaml > /tmp/merged.yaml

The theme file may override any draw_config key.  Its svg_style is *appended*
to the base svg_style so that the theme's CSS custom-property declarations
(--color-* variables) override the base defaults via the normal CSS cascade.
"""

import sys
import yaml


def merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base (override wins on conflicts)."""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            merge(base[key], value)
        else:
            base[key] = value
    return base


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <base.yaml> <theme.yaml>", file=sys.stderr)
        sys.exit(1)

    base_path, theme_path = sys.argv[1], sys.argv[2]

    with open(base_path) as fh:
        base = yaml.safe_load(fh)
    with open(theme_path) as fh:
        theme = yaml.safe_load(fh)

    if theme is None:
        # Empty theme file — just emit the base unchanged.
        yaml.dump(base, sys.stdout, default_flow_style=False, allow_unicode=True)
        return

    # Special handling for svg_style: *append* the theme CSS rather than
    # replace, so the theme's --color-* declarations win via CSS cascade.
    dc_base  = base.setdefault("draw_config", {})
    dc_theme = (theme or {}).get("draw_config", {})

    if "svg_style" in dc_theme:
        base_style  = dc_base.get("svg_style", "")
        theme_style = dc_theme.pop("svg_style")
        dc_base["svg_style"] = base_style.rstrip() + "\n\n" + theme_style.lstrip()

    # Merge remaining draw_config keys (e.g. dark_mode)
    if dc_theme:
        merge(dc_base, dc_theme)

    # Merge any other top-level sections (parse_config overrides, etc.)
    theme_without_dc = {k: v for k, v in theme.items() if k != "draw_config"}
    if theme_without_dc:
        merge(base, theme_without_dc)

    yaml.dump(base, sys.stdout, default_flow_style=False, allow_unicode=True)


if __name__ == "__main__":
    main()
