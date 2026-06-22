# Battery Pack Registers

This section covers registers for up to 15 battery packs. Each pack uses 30 registers (some packs use 8 registers for SN + 22 for data).

## Pack Identification (Registers 500-599)

Each pack has 12-15 bytes of ASCII serial number.

### Pack 1 SN (Registers 500-511)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 500 | Pack 1 Byte 01 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 501 | Pack 1 Byte 02 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 502 | Pack 1 Byte 03 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 503 | Pack 1 Byte 04 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 504 | Pack 1 Byte 05 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 505 | Pack 1 Byte 06 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 506 | Pack 1 Byte 07 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 507 | Pack 1 Byte 08 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 508 | Pack 1 Byte 09 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 509 | Pack 1 Byte 10 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 510 | Pack 1 Byte 11 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 511 | Pack 1 Byte 12 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |

### Pack 2 SN (Registers 512-523)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 512 | Pack 2 Byte 01 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 513 | Pack 2 Byte 02 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 514 | Pack 2 Byte 03 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 515 | Pack 2 Byte 04 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 516 | Pack 2 Byte 05 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 517 | Pack 2 Byte 06 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 518 | Pack 2 Byte 07 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 519 | Pack 2 Byte 08 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 520 | Pack 2 Byte 09 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 521 | Pack 2 Byte 10 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 522 | Pack 2 Byte 11 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 523 | Pack 2 Byte 12 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |

### Packs 3-15 SN

Same pattern continues for Packs 3-15, with each pack occupying 12 consecutive register addresses.

## Pack Data Registers

Each pack has the following data registers (30 registers per pack, 8 for SN + 22 for data for some packs).

### Pack 1 Data (Registers 600-629)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 600 | Pack 1 — Module Voltage | R | — | 0.01V | — |
| 601 | Pack 1 — Module Current | R | — | 0.1A | — |
| 602 | Pack 1 — Temperature AVE | R | — | — | 1250 = 25.0°C |
| 603 | Pack 1 — SOC | R | — | 0.1 | — |
| 604 | Pack 1 — Remaining Capacity | R | — | 0.1Ah | — |
| 605 | Pack 1 — Total Capacity | R | — | 0.1Ah | — |
| 606 | Pack 1 — Charge Voltage | R | — | 0.01V | — |
| 607 | Pack 1 — Charge Current | R | — | 0.1A | — |
| 608 | Pack 1 — Discharge Current | R | — | 0.1A | — |
| 609 | Pack 1 — Max Cell Voltage | R | — | 0.01V | — |
| 610 | Pack 1 — Min Cell Voltage | R | — | 0.01V | — |
| 611 | Pack 1 — Cycle Number | R | — | 1 | — |
| 612 | Pack 1 — Warning | R | — | — | — |
| 613 | Pack 1 — Fault | R | — | — | — |

### Pack 2 Data (Registers 614-627)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 614 | Pack 2 — Module Voltage | R | — | 0.01V | — |
| 615 | Pack 2 — Module Current | R | — | 0.1A | — |
| 616 | Pack 2 — Temperature AVE | R | — | — | 1250 = 25.0°C |
| 617 | Pack 2 — SOC | R | — | 0.1 | — |
| 618 | Pack 2 — Remaining Capacity | R | — | 0.1Ah | — |
| 619 | Pack 2 — Total Capacity | R | — | 0.1Ah | — |
| 620 | Pack 2 — Charge Voltage | R | — | 0.01V | — |
| 621 | Pack 2 — Charge Current | R | — | 0.1A | — |
| 622 | Pack 2 — Discharge Current | R | — | 0.1A | — |
| 623 | Pack 2 — Max Cell Voltage | R | — | 0.01V | — |
| 624 | Pack 2 — Min Cell Voltage | R | — | 0.01V | — |
| 625 | Pack 2 — Cycle Number | R | — | 1 | — |
| 626 | Pack 2 — Warning | R | — | — | — |
| 627 | Pack 2 — Fault | R | — | — | — |

### Packs 3-15 Data

Same pattern continues for Packs 3-15, each with 14 data registers.

## Deye Battery Read-Only Area (Registers 10000+)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 10000 | Device Type | R | — | — | Deye battery |
| 10001 | Protocol Version | R | — | — | — |
| 10002 | Packnum Number | R | 1 | — | — |
| 10003 | Battery Voltage | R | — | 0.1V | — |
| 10004 | Battery Current | R | — | 0.1A | — |
| 10005 | Battery SOC | R | — | 1% | — |
| 10006 | Battery SOH | R | — | 1% | — |
| 10007 | Battery CapAH | R | — | 1Ah | — |
| 10008 | Battery Temp | R | — | 0.1°C | — |
| 10009 | Charge Voltage | R | — | 0.1V | — |
| 10010 | Discharge Voltage | R | — | 0.1V | — |
| 10011 | Charge End Voltage | R | — | 1V | — |
| 10012 | Discharge End Voltage | R | — | 1V | — |
| 10013 | Charge Limit Current | R | — | 1A | — |
| 10014 | Discharge Limit Current | R | — | 1A | — |
| 10015 | Off-grid Charge Limit Current | R | — | 1A | — |
| 10016 | Off-grid Discharge Limit Current | R | — | 1A | — |
| 10017 | Force Charge Flag | R | — | — | — |
| 10018 | Check SOC Flag | R | — | — | — |
| 10019 | Battery Fault 1 | R | — | — | — |
| 10020 | Battery Fault 2 | R | — | — | — |
| 10021 | Battery Alarm 1 | R | — | — | — |
| 10022 | Battery Alarm 2 | R | — | — | — |
| 10023-10029 | Reserved 1-9 | R | — | — | — |

## Deye Battery Pack SN (Registers 10030-10044)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 10030 | Pack 1 Byte 01 | R | '0'-'9', 'A'-'Z' | — | ASCII |
| 10031 | Pack 1 Byte 02 | R | '0'-'9', 'A'-'Z' | — | ASCII |
| 10032 | Pack 1 Byte 03 | R | '0'-'9', 'A'-'Z' | — | ASCII |
| 10033 | Pack 1 Byte 04 | R | '0'-'9', 'A'-'Z' | — | ASCII |
| 10034 | Pack 1 Byte 05 | R | '0'-'9', 'A'-'Z' | — | ASCII |
| 10035 | Pack 1 Byte 06 | R | '0'-'9', 'A'-'Z' | — | ASCII |
| 10036 | Pack 1 Byte 07 | R | '0'-'9', 'A'-'Z' | — | ASCII |
| 10037 | Pack 1 Byte 08 | R | '0'-'9', 'A'-'Z' | — | ASCII |
| 10038 | Pack 1 Byte 09 | R | '0'-'9', 'A'-'Z' | — | ASCII |
| 10039 | Pack 1 Byte 10 | R | '0'-'9', 'A'-'Z' | — | ASCII |
| 10040 | Pack 1 Byte 11 | R | '0'-'9', 'A'-'Z' | — | ASCII |
| 10041 | Pack 1 Byte 12 | R | '0'-'9', 'A'-'Z' | — | ASCII |
| 10042 | Pack 1 Byte 13 | R | '0'-'9', 'A'-'Z' | — | ASCII |
| 10043 | Pack 1 Byte 14 | R | '0'-'9', 'A'-'Z' | — | ASCII |
| 10044 | Pack 1 Byte 15 | R | '0'-'9', 'A'-'Z' | — | ASCII |

## Deye Battery Pack Data (Registers 10040+)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 10040 | Pack 1 — Module Voltage | R | — | 0.1V | — |
| 10041 | Pack 1 — Module Current | R | — | 0.1A | — |
| 10042 | Pack 1 — Temperature AVE | R | — | — | 1250 = 25.0°C |
| 10043 | Pack 1 — Temperature Cell Max | R | — | — | 1250 = 25.0°C |
| 10044 | Pack 1 — Temperature Cell Min | R | — | — | 1250 = 25.0°C |
| 10045 | Pack 1 — Temperature MOS Max | R | — | — | 1250 = 25.0°C |
| 10046 | Pack 1 — Temperature Heat Mem | R | — | — | 1250 = 25.0°C |
| 10047 | Pack 1 — SOC | R | — | 0.1 | — |
| 10048 | Pack 1 — SOH | R | — | 0.1 | — |
| 10049 | Pack 1 — Remaining Capacity | R | — | 0.1Ah | — |
| 10050 | Pack 1 — Total Capacity | R | — | 0.1Ah | — |
| 10051 | Pack 1 — Charge Voltage | R | — | 0.01V | — |
| 10052 | Pack 1 — Discharge Voltage | R | — | 0.01V | — |
| 10053 | Pack 1 — Charge Current | R | — | 0.1A | — |
| 10054 | Pack 1 — Discharge Current | R | — | 0.1A | — |
| 10055 | Pack 1 — Max Cell Voltage | R | — | 0.01V | — |
| 10056 | Pack 1 — Min Cell Voltage | R | — | 0.01V | — |
| 10057 | Pack 1 — Cycle Number | R | — | 1 | — |
| 10058 | Pack 1 — MOS Status | R | — | 1 | — |
| 10059 | Pack 1 — Warning 1 | R | — | — | — |
| 10060 | Pack 1 — Warning 2 | R | — | — | — |
| 10061 | Pack 1 — Fault 1 | R | — | — | — |
| 10062 | Pack 1 — Fault 2 | R | — | — | — |
| 10063 | Software Version | R | — | — | — |
| 10064 | Hardware Version | R | — | — | — |
| 10065-10070 | Reserved 1-6 | R | — | — | — |

> **Note:** 8 registers for SN + 22 data registers = 30 registers per battery pack. Subsequent packs follow the same pattern.
