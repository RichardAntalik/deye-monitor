# Deye Battery Registers

This section covers Deye-specific battery registers including monthly/yearly energy data and battery configuration.

## Monthly/Yearly Energy Data Registers

### PV Generation Data (Registers 066-068)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 066 | Month_Load_PowerWh | R | — | 1kWh | Signed int (MI) |
| 067 | SG:Month_PV_PowerWh | R | — | 0.1kWh | — |
| 068 | SG:Month_Grid_PowerWh | R | — | 0.1kWh | Grid sell monthly |

### PV Yearly Generation Data (Registers 069-070)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 069 | Year_PV_PowerWh Low word | R | [0, 0xFFFF] | 0.1kWh | Low word |
| 070 | Year_PV_PowerWh High word | R | [0, 0xFFFF] | 0.1kWh | High word (LCD statistics) |

> **Note:** LCD statistics, DLN high/low status reversed. Combine low and high words for full value.

### Load Yearly Energy Data (Registers 088-089)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 088 | Year_Load_PowerWh Low word | R | [0, 0xFFFF] | 0.1kWh | Low word (MI) |
| 089 | Year_Load_PowerWh High word | R | [0, 0xFFFF] | 0.1kWh | High word (MI) |

### Grid Sell Yearly Data (Registers 098-099)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 098 | Year_GridSell_PowerWh Low word | R | [0, 0xFFFF] | 0.1kWh | Low word |
| 099 | Year_GridSell_PowerWh High word | R | [0, 0xFFFF] | 0.1kWh | High word |

## Deye Battery Configuration Registers

### Battery Configuration (Registers 300-325)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 300 | ARC_facTory_D high word | R/W | [0, 65535] | — | — |
| 301 | ARC_facTory_D low word | R/W | [0, 65535] | — | — |
| 302 | ARC_facTory_T high word | R/W | [0, 65535] | — | — |
| 303 | ARC_facTory_T low word | R/W | [0, 65535] | — | — |
| 304 | ARC_facTory_C high word | R/W | [0, 65535] | — | — |
| 305 | ARC_facTory_C low word | R/W | [0, 65535] | — | — |
| 306 | ARC_facTory_Frz high word | R/W | [0, 65535] | — | — |
| 307 | ARC_facTory_Frz low word | R/W | [0, 65535] | — | — |
| 308 | Ups_time | R/W | [0, 65535] | 1S | — |

### Battery Settings (Registers 309-325)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 309 | Charging Voltage | R/W | — | 0.01V | — |
| 310 | Discharge Voltage | R/W | — | 0.01V | — |
| 311 | Charging Current Limit | R/W | — | 1A | — |
| 312 | Discharge Current Limit | R/W | — | 1A | — |
| 313 | Real-time Capacity | R/W | — | 1% | — |
| 314 | Real-time Voltage | R/W | — | 0.01V | — |
| 315 | Real-time Current | R/W | — | 1A | — |
| 316 | Real-time Temperature | R/W | — | 0.1°C | — |
| 317 | Maximum Charge Current Limit | R/W | — | 1A | — |
| 318 | Maximum Discharge Current Limit | R/W | — | 1A | — |
| 319 | Lithium Battery Alarm Position | R/W | — | — | — |
| 320 | Lithium Battery Fault Location | R/W | — | — | — |
| 321 | Lithium Battery Symbol 2 | R/W | — | — | — |
| 322 | Lithium Battery Type | R/W | — | — | — |
| 323-325 | Reserved | R/W | — | — | — |

### Lithium Battery Type Codes (Register 322)

| Value | Battery Type |
|:---:|---|
| 0x0000 | PYLON |
| 0x0001 | SOLAX |
| 0x0002 | General CAN Protocol |
| 0x0003 | Keith |
| 0x0004 | Topband Protocol |
| 0x0005 | Pylontech 485 Protocol |
| 0x0006 | — |
| 0x0007 | — |
| 0x0008 | — |
| 0x0009 | — |
| 0x000A | — |

### CT Configuration (Register 326)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 326 | CT Ratio | R/W | 200-8000 | — | External CT multiplier |

### Special Function Bits (Register 327)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 327 | Special Function Bits | R/W | — | — | See bit mapping below |

**Register 327 Bit Mapping:**

| Bits | Function | Description |
|:---:|---|---|
| Bit0 | Meter1 CT Enable | 1 = Enable, 0 = Disable |
| Bit1 | Phase A Enable | — |
| Bit2 | Phase B Enable | — |
| Bit3 | Phase C Enable | — |
| Bit6 | ActoGrid Enable | 1 = Enable, 0 = Disable |
| Bit7 | ActoLoad Enable | 1 = Enable, 0 = Disable |
| Bit8-11 | Meter1/2 Type | 1 = SDM630 (3-phase), 2 = CHINT DTSU666 (3-phase), 3 = SD230 (single-phase), 4 = CHINT DDSU666 (single-phase) |
| Bit12 | Meter2 CT Enable | 1 = Enable, 0 = Disable |
| Bit13 | Generator Force Enable | 1 = Enable, 0 = Disable |
| Bit14 | Reserved | — |
| Bit15 | Reserved | — |

### AC Couple Frequency (Register 328)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 328 | AC Couple Frequency Upper Limit | R/W | 5000-6500 | 0.01Hz | — |

### Communication Board Settings (Register 329)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 329 | Communication Board Settings | R/W | — | — | See bit mapping below |

**Register 329 Bit Mapping:**

| Bits | Function | Description |
|:---:|---|---|
| Bit0-1 | Time Calibration | — |
| Bit2-3 | Beep Control | — |
| Bit4-5 | AM/PM | — |
| Bit6-7 | Auto Dim | — |
| Bit8-9 | Solar Discern | — |
| Bit10-11 | Li-ion Battery Packet Display | 11 = Hide, 10 = Show |

### US Version Ground Fault (Register 330)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 330 | US Version Ground Fault Stop | R/W | — | — | 0 = Stop on fault, 1 = Do not stop |
