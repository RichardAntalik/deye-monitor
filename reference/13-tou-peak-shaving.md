# TOU and Peak Shaving Registers

Time of Use (TOU) selling and peak shaving configuration registers.

## Solar Sell / TOU Selling Enable (Register 247)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 247 | Time of Use Selling Enabled | R/W | [0, 1] | — | Bit mapping below |

**Register 247 Bit Mapping:**

| Bits | Function | Description |
|:---:|---|---|
| Bit0 | Solar Sell | 0 = Solar Don't Sell, 1 = Solar Sell |
| Bit1 | Monday | 0 = Disable, 1 = Enable |
| Bit2 | Tuesday | 0 = Disable, 1 = Enable |
| Bit3 | Wednesday | 0 = Disable, 1 = Enable |
| Bit4 | Thursday | 0 = Disable, 1 = Enable |
| Bit5 | Friday | 0 = Disable, 1 = Enable |
| Bit6 | Saturday | 0 = Disable, 1 = Enable |
| Bit7 | Sunday | 0 = Disable, 1 = Enable |
| Bit8 | Working Mode 3 | Spain customer requirement |

## Sell Mode Time Points (Registers 248-251)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 248 | Sell Mode Time Point 1 | R/W | [0000, 2359] | — | 2359 means time 23:59 |
| 249 | Sell Mode Time Point 2 | R/W | [0000, 2359] | — | — |
| 250 | Sell Mode Time Point 3 | R/W | [0000, 2359] | — | — |
| 251 | Sell Mode Time Point 4 | R/W | [0000, 2359] | — | — |
| 252 | Sell Mode Time Point 5 | R/W | [0000, 2359] | — | — |
| 253 | Sell Mode Time Point 6 | R/W | [0000, 2359] | — | — |

## Sell Mode Power Points (Registers 254-261)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 254 | Sell Mode Time Point 1 Power | R/W | [0000, 8000] | 1W | Affected by max battery discharge power |
| 255 | Sell Mode Time Point 2 Power | R/W | [0000, 8000] | 1W | Affected by max battery discharge power |
| 256 | Sell Mode Time Point 3 Power | R/W | [0000, 8000] | 1W | Affected by max battery discharge power |
| 257 | Sell Mode Time Point 4 Power | R/W | [0000, 8000] | 1W | Affected by max battery discharge power |
| 258 | Sell Mode Time Point 5 Power | R/W | [0000, 8000] | 1W | Affected by max battery discharge power |
| 259 | Sell Mode Time Point 6 Power | R/W | [0000, 8000] | 1W | Affected by max battery discharge power |

## Sell Mode Voltage Points (Registers 262-267)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 262 | Sell Mode Time Point 1 Voltage | R/W | [0000, 6300] | 0.01V | Affected by battery voltage |
| 263 | Sell Mode Time Point 2 Voltage | R/W | [0000, 6300] | 0.01V | Affected by battery voltage |
| 264 | Sell Mode Time Point 3 Voltage | R/W | [0000, 6300] | 0.01V | Affected by battery voltage |
| 265 | Sell Mode Time Point 4 Voltage | R/W | [0000, 6300] | 0.01V | Affected by battery voltage |
| 266 | Sell Mode Time Point 5 Voltage | R/W | [0000, 6300] | 0.01V | Affected by battery voltage |
| 267 | Sell Mode Time Point 6 Voltage | R/W | [0000, 6300] | 0.01V | Affected by battery voltage |

## Battery Capacity Settings (Registers 268-273)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 268 | Capacity 1 | R/W | [0, 100] | 1% | — |
| 269 | Capacity 2 | R/W | [0, 100] | 1% | — |
| 270 | Capacity 3 | R/W | [0, 100] | 1% | — |
| 271 | Capacity 4 | R/W | [0, 100] | 1% | — |
| 272 | Capacity 5 | R/W | [0, 100] | 1% | — |
| 273 | Capacity 6 | R/W | [0, 100] | 1% | — |

## Time Point Charge Enable (Registers 274-279)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 274 | Time Point 1 Charge Enable | R/W | [0, 1] | — | See bit mapping below |
| 275 | Time Point 2 Charge Enable | R/W | [0, 1] | — | Same as above |
| 276 | Time Point 3 Charge Enable | R/W | [0, 1] | — | Same as above |
| 277 | Time Point 4 Charge Enable | R/W | [0, 1] | — | Same as above |
| 278 | Time Point 5 Charge Enable | R/W | [0, 1] | — | Same as above |
| 279 | Time Point 6 Charge Enable | R/W | [0, 1] | — | Same as above |

**Register 274-279 Bit Mapping (same for all time point charge enable registers):**

| Bits | Function | Description |
|:---:|---|---|
| Bit0 | Grid Charge Enable | 0 = Disable, 1 = Enable |
| Bit1 | Generator Charge Enable | 0 = Disable, 1 = Enable |
| Bit2 | GM Mode | Generator-Main mode |
| Bit3 | BU Mode | Backup mode |
| Bit4 | CH Mode | Charge mode |

## Advanced Configuration Registers (Registers 280-286)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 280 | Microinverter Export | R/W | [0, 1] | — | — |
| 281 | External Sensor Auto Detect Direction Enable | R/W | — | — | — |
| 282 | Restore Connection Time | R/W | [10, 300] | — | — |
| 283 | Solar Arc Fault Mode Turned On | R/W | [0, 1] | — | 0 = Close, 1 = Open, 2 = Arc fault reset |
| 284 | Grid Mode | R/W | [0, 1] | — | — |
| 285 | Grid Frequency | R/W | [0, 1] | — | 0 = 50Hz, 1 = 60Hz |
| 286 | Grid Type | R/W | [0, 3] | — | See bit mapping below |

**Register 283 Arc Fault Values:**

| Value | Description |
|:---:|---|
| 0 | Close |
| 1 | Open |
| 2 | Arc fault reset — inverter receives 02 indicating LCD issued clear mark, then auto returns to 01 |

**Register 286 Grid Type Bit Mapping:**

| Bits | Function | Description |
|:---:|---|---|
| Bit0-3 | Inverter Output Voltage | If 286==0: 0=230V, 1=220V, 2=240V, 3=200V<br>If 286==1: 0=120/240V, 1=110/220V, 2=120/240V, 3=110/200V<br>If 286==2: 0=120/208V, 1=127/220V |
| Bit4-7 | Generator Peak Shaving | 0 = Gen peak-shaving disable, 1 = Gen peak-shaving enable |
| Bit8-11 | Grid Peak Shaving | 0 = Grid peak-shaving disable, 1 = Grid peak-shaving enable |
| Bit12 | On Grid Always On | — |
| Bit13 | External Relay | — |
| Bit14 | Li-ion Battery Lost Fault Enable | — |
| Bit15 | DRM Enable | — |

## Grid Protection Settings (Registers 287-292)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 287 | Grid Vol High | R/W | [1800, 2700] | 0.1V | Grid over-voltage protection point |
| 288 | Grid Vol Low | R/W | [1800, 2700] | 0.1V | Grid under-voltage protection point |
| 289 | Grid Hz High | R/W | [4500, 6500] | 0.01Hz | Grid over-frequency protection point |
| 290 | Grid Hz Low | R/W | [4500, 6500] | 0.01Hz | Grid under-frequency protection point |
| 291 | Generator Connected to Grid Input | R/W | [1, 0] | — | — |
| 292 | GEN Peak Shaving Power | R/W | [0, 16000] | 1W | — |

## Additional Peak Shaving and Control Registers (Registers 293-307)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 293 | GRID Peak Shaving Power | R/W | — | — | — |
| 294 | SmartLoad Open Delay | R/W | [1, 120] | 1Minute | — |
| 295 | Output PF Value Setting (Active Power Regulation) | R/W | [800, 1200] | — | 800 = 80%, 1200 = 120% |
| 296 | External Relay Bits | R/W | [0, 65535] | — | Bit0-8 correspond to 8 relay bits |
| 297 | ARC_facTory_B High Word | R/W | [0, 65535] | — | — |
| 298 | ARC_facTory_B Low Word | R/W | [0, 65535] | — | — |
| 299 | ARC_facTory_I High Word | R/W | [0, 65535] | — | — |
| 300 | ARC_facTory_I Low Word | R/W | [0, 65535] | — | — |
| 301 | ARC_facTory_F High Word | R/W | [0, 65535] | — | — |
| 302 | ARC_facTory_F Low Word | R/W | [0, 65535] | — | — |
| 303 | ARC_facTory_D High Word | R/W | [0, 65535] | — | — |
| 304 | ARC_facTory_D Low Word | R/W | [0, 65535] | — | — |
| 305 | ARC_facTory_T High Word | R/W | [0, 65535] | — | — |
| 306 | ARC_facTory_T Low Word | R/W | [0, 65535] | — | — |
| 307 | ARC_facTory_C High Word | R/W | [0, 65535] | — | — |
| 308 | ARC_facTory_C Low Word | R/W | [0, 65535] | — | — |
| 309 | ARC_facTory_Frz High Word | R/W | [0, 65535] | — | — |
| 310 | ARC_facTory_Frz Low Word | R/W | [0, 65535] | — | — |

## UPS Time Register

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| — | Ups_time | R/W | [0, 65535] | 1S | — |
