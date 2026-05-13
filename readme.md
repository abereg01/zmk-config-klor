# ZMK CONFIG FOR THE KLOR SPLIT KEYBOARD

Custom ZMK firmware configuration for the KLOR split keyboard by Saegewerk.

This repository contains my personal keyboard layout, configuration and build setup for the KLOR keyboard running ZMK firmware.

## Hardware

- Keyboard: KLOR Split Keyboard
- Manufacturer: Saegewerk
- Firmware: ZMK
- MCU Support:
  - nice!nano v2
  - Seeeduino XIAO BLE
  - Prospector builds

## Features

- Split keyboard support
- Layer-based layout
- Custom keymaps
- OLED/display support (if enabled)
- Encoder support (if enabled)
- GitHub Actions automated firmware builds
- Designed for wireless and wired experimentation

## Firmware Builds

Firmware is automatically built through GitHub Actions.

Generated firmware artifacts can be downloaded from the Actions tab after each successful build.

## Repository Structure

```text
config/
├── boards/
├── keymap/
├── overlays/
└── west.yml
