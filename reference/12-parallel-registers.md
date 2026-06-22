# Parallel Registers

Registers for parallel/inverter system operation.

## Force Off-Grid Operation (Register 416)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 416 | Force Off-Grid Operation | R/W | [0, 1] | — | 0 = Disable, 1 = Enable |

## Parallel Register 1 (Register 417)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 417 | Parallel Register 1 | R/W | — | — | See bit mapping below |

**Register 417 Bit Mapping:**

| Bits | Function | Description |
|:---:|---|---|
| Bit0 | Parallel Enable | 1 = Parallel Enable, 0 = Parallel Disable |
| Bit1 | Master/Slave | 1 = Master, 0 = Slave |
| Bit2-7 | Void | — |
| Bit8-9 | Phase | 00 = A, 01 = B, 10 = C, 11 = Void |
| Bit10-15 | Modbus SN | 0-63 |

## Parallel Register 2 (Register 418)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 418 | Parallel Register 2 | R/W | [0-200] | — | See bit mapping below |

**Register 418 Bit Mapping:**

| Bits | Function | Description |
|:---:|---|---|
| Bit0-4 | A Phase Inverter Num | Number of A phase inverters |
| Bit5-9 | B Phase Inverter Num | Number of B phase inverters |
| Bit10-14 | C Phase Inverter Num | Number of C phase inverters |
| Bit15 | Void | — |

> **Note:** For multi-inverter parallel systems, only the last inverter's register 418 is readable.

## Battery Version Registers

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| — | Lithium Battery Version Low Word | R/W | — | — | — |
| — | Lithium Battery Version High Word | R/W | — | — | — |

## System Time Registers (Registers 419-424)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 419 | System Time Byte 01 | R/W | — | — | — |
| 420 | System Time Byte 02 | R/W | — | — | — |
| 421 | System Time Byte 03 | R/W | — | — | — |
| 422 | System Time Byte 04 | R/W | — | — | — |
| 423 | System Time Byte 05 | R/W | — | — | — |
| 424 | System Time Byte 06 | R/W | — | — | — |

> **Note:** If LCD is set to slave mode and time is detected here, time synchronization will be performed.

## Year/Month/Day/Hour/Minute/Second Registers

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| — | Year | R/W | — | — | — |
| — | Month | R/W | — | — | — |
| — | Day | R/W | — | — | — |
| — | Hour | R/W | — | — | — |
| — | Minute | R/W | — | — | — |
| — | Second | R/W | — | — | — |

## Hybrid Inverter Real-time Data 3 (Registers 425-438)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 425 | Grid_V_L1 | R | — | — | Grid voltage L1 |
| 426 | Grid_V_L2 | R | — | — | Grid voltage L2 |
| 427 | Limit1_I | R | — | — | Limit current 1 |
| 428 | Limit2_I | R | — | — | Limit current 2 |
| 429 | PV1_V | R | — | — | PV1 voltage |
| 430 | PV1_I | R | — | — | PV1 current |
| 431 | PV2_V | R | — | — | PV2 voltage |
| 432 | PV2_I | R | — | — | PV2 current |
| 433 | INV_I | R | — | — | Inverter current |
| 434 | INV_V | R | — | — | Inverter voltage |
| 435 | BAT_I | R | — | — | Battery current |
| 436 | BAT_V | R | — | — | Battery voltage |
| 437 | Solar1 Wind Input Enable | R/W | — | — | Solar1 as wind input enable |
| 438 | Solar2 Wind Input Enable | R/W | — | — | Solar2 as wind input enable |

## PV Voltage/Current Registers (Registers 439-450)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 439 | PV Voltage 1 | R | — | — | PV voltage channel 1 |
| 440 | PV Voltage 2 | R | — | — | PV voltage channel 2 |
| 441 | PV Voltage 3 | R | — | — | PV voltage channel 3 |
| 442 | PV Voltage 4 | R | — | — | PV voltage channel 4 |
| 443 | PV Voltage 5 | R | — | — | PV voltage channel 5 |
| 444 | PV Voltage 6 | R | — | — | PV voltage channel 6 |
| 445 | PV Voltage 7 | R | — | — | PV voltage channel 7 |
| 446 | PV Voltage 8 | R | — | — | PV voltage channel 8 |
| 447 | PV Voltage 9 | R | — | — | PV voltage channel 9 |
| 448 | PV Voltage 10 | R | — | — | PV voltage channel 10 |
| 449 | PV Voltage 11 | R | — | — | PV voltage channel 11 |
| 450 | PV Voltage 12 | R | — | — | PV voltage channel 12 |

## PV Current Registers (Registers 451-462)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 451 | PV Current 1 | R | — | — | PV current channel 1 |
| 452 | PV Current 2 | R | — | — | PV current channel 2 |
| 453 | PV Current 3 | R | — | — | PV current channel 3 |
| 454 | PV Current 4 | R | — | — | PV current channel 4 |
| 455 | PV Current 5 | R | — | — | PV current channel 5 |
| 456 | PV Current 6 | R | — | — | PV current channel 6 |
| 457 | PV Current 7 | R | — | — | PV current channel 7 |
| 458 | PV Current 8 | R | — | — | PV current channel 8 |
| 459 | PV Current 9 | R | — | — | PV current channel 9 |
| 460 | PV Current 10 | R | — | — | PV current channel 10 |
| 461 | PV Current 11 | R | — | — | PV current channel 11 |
| 462 | PV Current 12 | R | — | — | PV current channel 12 |

## Battery ID Registers (Registers 500-513)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 500 | Battery ID Byte 01 | R | '0'-'9', 'A'-'Z' | — | Saintyang battery ASCII |
| 501 | Battery ID Byte 02 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 502 | Battery ID Byte 03 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 503 | Battery ID Byte 04 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 504 | Battery ID Byte 05 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 505 | Battery ID Byte 06 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 506 | Battery ID Byte 07 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 507 | Battery ID Byte 08 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 508 | Battery ID Byte 09 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 509 | Battery ID Byte 10 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 510 | Battery ID Byte 11 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 511 | Battery ID Byte 12 | R | '0'-'9', 'A'-'Z' | — | ASCII characters |
| 512 | Packnum Number | R | 1 | — | Number of battery packs |
| 513 | Fifteen Battery Packs ID Num | R | — | — | Only for TIAN-POWER |
