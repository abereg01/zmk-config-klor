# KLOR — ZMK Firmware Config

Personal ZMK firmware configuration for the **KLOR** split ergonomic keyboard.

![Keymap Overview](draw/base.svg)

---

## Hardware

| Component | Choice |
|-----------|--------|
| Keyboard  | KLOR (Saegewerk) — 42-key column-stagger split |
| MCU       | nice!nano v2 (both halves) |
| Connection | TRRS cable (wired split) |
| Encoders  | Rotary encoder on each half |
| Firmware  | [ZMK](https://zmk.dev) |

---

## Layers

| # | Name    | Activated by |
|---|---------|-------------|
| 0 | BASE    | Default |
| 1 | LOWER   | Hold `LOWER` thumb |
| 2 | RAISE   | Hold right thumb (`SPC/CW`) |
| 3 | ADJUST  | `LOWER` + `RAISE` simultaneously |
| 4 | NAV     | Hold `NAV/NUM` thumb (single tap) |
| 5 | NUM     | Double-tap `NAV/NUM` thumb → Smart-Num |
| 6 | SCROLL  | Hold right encoder button |

---

## Key Features

### Homerow Mods
Tap for the letter, hold for a modifier — no extra keys needed.

| Key | Tap | Hold |
|-----|-----|------|
| A   | A   | GUI  |
| S   | S   | Alt  |
| D   | D   | Shift |
| F   | F   | Ctrl |
| J   | J   | GUI  |
| K   | K   | Shift |
| L   | L   | Alt  |
| ;   | ;   | Ctrl |

### Mod-Morphs
Two characters on one key, split by whether Shift is held.

| Key | Tap | Shift |
|-----|-----|-------|
| `,` | `,` | `;`   |
| `.` | `.` | `:`   |
| `/` | `?` | `!`   |
| Right-space | Space | Caps Word |

> Forward slash `/` is still reachable via the **K + ,** combo.

### Tap Dances

| Key | Single tap | Double tap |
|-----|-----------|------------|
| `A` | `A` / hold → GUI | `Ä` |
| `S+X` combo | `'` | `` ` `` |
| NAV/NUM thumb | Hold → NAV layer | Double-tap → Smart-Num |

### Smart-Num (auto-layer)
Double-tapping the NAV/NUM thumb activates the NUM layer via [urob's zmk-auto-layer](https://github.com/urob/zmk-auto-layer). The layer stays active as long as you type numbers or any of `BSPC DEL . , + - * / =`. It deactivates automatically on any other keypress — space, enter, letters, `?`, `!` all close it. No manual exit needed.

### Caps Word
Hold Shift and tap the right thumb space key to activate Caps Word. Types in ALL CAPS and auto-deactivates on any key outside `A–Z`, `_`, `BSPC`, or `DEL`.

### Encoders

| Encoder | Rotate | While holding button |
|---------|--------|----------------------|
| Left    | Scroll up / down | — |
| Right   | Scroll up / down | Scroll left / right |

Horizontal scroll uses ZMK's pointing layer (`msc SCRL_LEFT/RIGHT`) for reliable cross-app support.

### Combos
All combos use a 50 ms timeout with a 100 ms prior-idle guard. See `combos.dtsi` for the full position map.

**Navigation / editing**
- `W + E` → Escape  &ensp; `S + D` → Tab
- `R + T` → Delete  &ensp; `Y + I` → Delete
- `F + G` → Backspace  &ensp; `H + J` → Backspace

**Clipboard**
- `X + C` → Copy &ensp; `C + V` → Paste &ensp; `X + V` → Cut

**Symbols — left side**
- `W+S` → `@` &ensp; `E+D` → `#` &ensp; `R+F` → `$` &ensp; `T+G` → `%`
- `S+X` → `'`/`` ` `` &ensp; `D+C` → `\` &ensp; `F+V` → `=` &ensp; `G+B` → `~`

**Symbols — right side**
- `Y+H` → `^` &ensp; `I+J` → `+` &ensp; `O+K` → `*` &ensp; `P+L` → `&`
- `H+N` → `_` &ensp; `J+M` → `-` &ensp; `K+,` → `/` &ensp; `L+.` → `|`

**Brackets**
- Top row: `I+O` → `(` &ensp; `O+P` → `)`
- Home row: `J+K` → `(` &ensp; `K+L` → `)`
- Bottom row: `M+,` → `[` &ensp; `,+.` → `]`

**Special characters**
- `A + S` → `Å`

---

## Repository Structure

```
config/
├── west.yml                          # ZMK + module dependencies
├── klor.conf                         # Board-level config flags
└── boards/shields/klor/
    ├── klor.keymap                   # Layer bindings (clean, no inline behaviors)
    ├── combos.dtsi                   # All combo definitions
    ├── macros.dtsi                   # Macro definitions
    ├── behaviors.dtsi                # Homerow-mod hold-tap
    ├── tapdance.dtsi                 # Tap-dance behaviors
    └── morphs.dtsi                   # Mod-morphs + scroll encoder
draw/
├── overview.svg                      # All-layers keymap visualization
├── base.svg                          # Base layer only
├── klor.svg                          # Hardware layout
└── keymap.png                        # Full keymap, all layers (high-res)
```

---

## ZMK Modules

| Module | Purpose |
|--------|---------|
| [zmk-auto-layer](https://github.com/urob/zmk-auto-layer) | Smart-Num auto-exit behavior (`num_word`) |

Modules are declared in `config/west.yml` and fetched automatically by `west update`.

---

## Building

Firmware is built automatically via **GitHub Actions** on every push. Download the `.uf2` artifacts from the **Actions** tab.

### Local build

```bash
west init -l config
west update
west build -s zmk/app -b nice_nano_v2 -- -DSHIELD=klor_left
west build -s zmk/app -b nice_nano_v2 -- -DSHIELD=klor_right
```

### Flashing

Double-tap the reset button to put the nice!nano into bootloader mode, then drag the `.uf2` file onto the `NICENANO` drive that appears.
