# Intrinsic Attribute Region

These registers contain fixed device information that is read-only (R) unless otherwise noted.

## Device Identification

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 000 | Device Type | R | — | — | `0x0200` = String inverter<br>`0x0300` = Single-phase low-voltage storage inverter<br>`0x0400` = Microinverter<br>`0x0500` = Three-phase low-voltage storage inverter<br>`0x0600` = Three-phase high-voltage storage inverter |
| 001 | Modbus Address | R | [1, 247] | — | MI |
| 002 | Communication Protocol Version | R | '0'-'9', 'A'-'Z' | — | Firmware protocol version, e.g. `0x0102` = version 1.2. MI |

## Serial Number (10 ASCII bytes)

The serial number is 10 ASCII characters. Example: "AH12345678" → Byte 01 = `0x41` (A), Byte 02 = `0x48` (H), …, Byte 09 = `0x37` (7), Byte 10 = `0x38` (8).

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 003 | SN Byte 01 | R | '0'-'9', 'A'-'Z' | — | MI |
| 004 | SN Byte 02 | R | '0'-'9', 'A'-'Z' | — | MI |
| 005 | SN Byte 03 | R | '0'-'9', 'A'-'Z' | — | MI |
| 006 | SN Byte 04 | R | '0'-'9', 'A'-'Z' | — | MI |
| 007 | SN Byte 05 | R | '0'-'9', 'A'-'Z' | — | MI |
| 008 | SN Byte 06 | R | '0'-'9', 'A'-'Z' | — | MI |
| 009 | SN Byte 07 | R | '0'-'9', 'A'-'Z' | — | MI |
| 010 | SN Byte 08 | R | '0'-'9', 'A'-'Z' | — | MI |
| 011 | SN Byte 09 | R | '0'-'9', 'A'-'Z' | — | MI |
| 012 | SN Byte 10 | R | '0'-'9', 'A'-'Z' | — | MI |

## Hardware Information

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 013 | Rated Power | R | [0, 1000] | 0.1W | MI |
| 014 | Rated Power (High Word) | R | [0, 255] | 0.1W | MI |
| 015 | MPPT Number & Phases | R/W | [1, 8] / [1, 3] | — | MI `0x0503`: five-MPPT three-phase |
| 016 | Chip Type | R | 0x0000 | — | Low 4 bits: `0x1` = AT32F403A_DEVICE, `0x2` = SXX32F103_DEVICE, `0x3` = GD32F103_DEVICE, `0x4` = GD32F303_DEVICE |
| 017 | Control Board Auxiliary Program Version | R | — | — | MI |
| 018 | Control Board Firmware Version (Field 2) | R | — | — | MI |
| 019 | Control Board Firmware Version | R | — | — | — |
| 020 | Communication Board Firmware Version | R | — | — | MI |
| 021 | Communication Board Firmware Version (Field 2) | R | — | — | MI |
| 022 | Safety Type | R/W | [0, 3] | — | `<3`: 48V battery, `=3`: 24V battery |
| 023 | Grid Voltage Level | R/W | [0, 3] | — | `0`: 127/220V, `1`: 220/380V, `2`: Open, `3`: Close |
| 024 | Remote Lock Enable | R/W | [0, 1] | — | `0`: disable, `1`: enable |
| 025 | Self-check Time (Power-on) | R/W | [0, 1000] | S | MI |

## System Time (6 bytes)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 021 | System Time Byte 01 (Year) | R/W | [0, 99] | — | Based on year 2000 |
| 022 | System Time Byte 02 (Month) | R/W | [1, 12] | — | — |
| 023 | System Time Byte 03 (Day) | R/W | [1, 31] | — | — |
| 024 | System Time Byte 04 (Hour) | R/W | [0, 23] | — | — |
| 025 | System Time Byte 05 (Minute) | R/W | [0, 59] | — | — |
| 026 | System Time Byte 06 (Second) | R/W | [0, 59] | — | — |
