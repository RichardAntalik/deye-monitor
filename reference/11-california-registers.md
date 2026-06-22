# California Registers

California-specific grid compliance registers for voltage/frequency ride-through and reactive power control.

## California Low Voltage/High Voltage Ride-Through (Registers 330-340)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 330 | CA_LHVRT Enable | R/W | [0, 1] | — | California low voltage/high voltage ride-through enable |
| 331 | CA_HV2 | R/W | [1000, 3000] | 0.1V | High voltage threshold 2 |
| 332 | CA_HV1 | R/W | [1000, 3000] | 0.1V | High voltage threshold 1 |
| 333 | CA_LV1 | R/W | [0, 300] | — | Low voltage threshold 1 |
| 334 | CA_LV2 | R/W | [0, 300] | — | Low voltage threshold 2 |
| 335 | CA_LV3 | R/W | [0, 300] | — | Low voltage threshold 3 |
| 336 | CA_HV2_Time | R/W | — | 0.16s | 0 = 0.16s |
| 337 | CA_HV1_Time | R/W | — | 0.16s | — |
| 338 | CA_LV1_Time | R/W | — | 0.16s | — |
| 339 | CA_LV2_Time | R/W | — | 0.16s | — |
| 340 | CA_LV3_Time | R/W | — | 0.16s | — |

## California Low Frequency/High Frequency Ride-Through (Registers 341-350)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 341 | CA_LHFRT Enable | R/W | — | — | California low frequency/high frequency ride-through enable |
| 342 | CA_HF2 | R/W | [4500, 6500] | 0.01Hz | High frequency threshold 2 |
| 343 | CA_HF1 | R/W | [4500, 6500] | 0.01Hz | High frequency threshold 1 |
| 344 | CA_LF1 | R/W | [4500, 6500] | 0.01Hz | Low frequency threshold 1 |
| 345 | CA_LF2 | R/W | [4500, 6500] | 0.01Hz | Low frequency threshold 2 |
| 346 | CA_HF2_Time | R/W | [0, 300] | — | High frequency time threshold 2 |
| 347 | CA_HF1_Time | R/W | [0, 300] | — | High frequency time threshold 1 |
| 348 | CA_LF1_Time | R/W | — | — | Low frequency time threshold 1 |
| 349 | CA_LF2_Time | R/W | — | — | Low frequency time threshold 2 |

## California CA_QV Reactive Power Control (Registers 350-357)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 350 | CA_QV Enable | R/W | — | — | California CA_QV reactive power-voltage curve enable |
| 351 | CA_QV_V1 | R/W | [1000, 3000] | 0.01V | Voltage point 1 |
| 352 | CA_QV_V2 | R/W | [1000, 3000] | 0.01V | Voltage point 2 |
| 353 | CA_QV_V3 | R/W | [1000, 3000] | 0.01V | Voltage point 3 |
| 354 | CA_QV_V4 | R/W | [1000, 3000] | 0.01V | Voltage point 4 |
| 355 | CA_QV_Q1 | R/W | [-44, +44] | 0.01 | Reactive power factor 1 |
| 356 | CA_QV_Q2 | R/W | [-44, +44] | 0.01 | Reactive power factor 2 |
| 357 | CA_QV_Q3 | R/W | [-44, +44] | 0.01 | Reactive power factor 3 |
| 358 | CA_QV_Q4 | R/W | [-44, +44] | 0.01 | Reactive power factor 4 |
| 359 | QV Response Time | R/W | [1, 100] | 1% | QV response time |

## California CA_FW Frequency-Active Power Control (Registers 360-361)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 360 | CA_FW Enable | R/W | — | — | California CA_FW frequency-active power curve enable |
| 361 | CA_Fstart | R/W | [1, 100] | 1% | Frequency active power start point |
| 362 | CA_Fstop | R/W | [1, 100] | 1% | Frequency active power stop point |
| 363 | FW Response Time | R/W | [0, 90] | S | FW response time |

## California CA_VW Voltage-Active Power Control (Registers 364-365)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 364 | CA_VW Enable | R/W | — | — | California CA_VW voltage-active power curve enable |
| 365 | CA_Vstart | R/W | [0, 60] | S | Voltage active power start point |
| 366 | CA_Vstop | R/W | — | S | Voltage active power stop point |
| 367 | VW Response Time | R/W | — | S | VW response time |

## Normal Upward Slope (Register 368)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 368 | Normal Upward Slope | R/W | — | — | Default 100% |

## Soft Start Rise Rate (Register 369)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 369 | Soft Start Rise Rate | R/W | — | — | — |

## Reserved Registers

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 370 | Reserved | R/W | — | — | — |
| 371 | Reserved | R/W | — | — | — |
| 372 | Reserved | R/W | — | — | — |
| 373 | Reserved | R/W | — | — | — |
| 374 | Reserved | R/W | — | — | — |

## Grid Current Registers

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 375 | Grid1_I | R | — | — | Grid current 1 |
| 376 | Grid2_I | R | — | — | Grid current 2 |

## Battery Protocol Selection (Registers 377-378)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 377 | Jielisi 485 Protocol | R/W | — | — | Jielisi battery 485 protocol |
| 378 | Sunwoda 485 Protocol | R/W | — | — | Sunwoda battery 485 protocol |
| 379 | Xinruienergy 485 Protocol | R/W | — | — | Xinruienergy battery 485 protocol |
| 380 | Tianbangda 485 Protocol | R/W | — | — | Tianbangda battery 485 protocol |
| 381 | Shenggao Electric CAN Protocol | R/W | — | — | Shenggao Electric CAN protocol |
