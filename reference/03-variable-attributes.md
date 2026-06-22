# Variable Attribute Region

These registers are configurable settings for device operation.

## Protection & Grid Settings

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 027 | Minimum Insulation Impedance | R/W | [100, 20000] | 0.1KΩ | MI |
| 028 | DC Voltage Upper Limit | R/W | [2000, 10000] | 0.1V | — |
| 029 | Grid Voltage Upper Limit | R/W | [1600, 5500] | 0.1V | — |
| 030 | Grid Frequency Upper Limit | R/W | [4500, 6500] | 0.01Hz | — |
| 031 | Grid Frequency Lower Limit | R/W | [4500, 6500] | 0.01Hz | — |
| 032 | Grid Current Upper Limit | R/W | [10, 20000] | 0.1A | — |
| 033 | Starting Voltage Upper Limit | R/W | [7000, 9000] | 0.1V | — |
| 034 | Starting Voltage Lower Limit | R/W | [4500, 9000] | 0.1V | — |

**Register 030 bits:**
- Bit0: ATS Enable
- Bit1: ATS Status
- Bit2: Low Power Mode < Low Batt
- Bit5: MPPT Multi-Point Scanning

**Register 032 bits:**
- Bit0: Control board power calculation flag
- Bit2: LCD board power calculation method flag — `1`: LCD calculates itself; `0`: read register directly without calculation

## Low Noise & Power Limiter

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 034 | Low Noise Mode | R/W | [0, 1] | — | `0`: disable, `1`: enable |
| 035 | Over-Frequency De-rate Percentage | R/W | [0, 100] | 0.1%/1% | If 800 → adjust to 80.0% |
| 036 | Import Power Limiter | R/W | [0, 0xFFFF] | — | Value offset by +1000. E.g. -0.852 = 148, 0 = 1000, 0.982 = 1982 |

## Communication Settings

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 037 | Communication Address | R | [0, 2000] | — | — |
| 038 | Communication Baud Rate | R | [0, 1200] | — | 0.1% |
| 039 | MI: Zigbee or PLC | R | 0x0000 | — | `0`: Zigbee, `1`: PLC |

## Power Regulation

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 040 | Power Factor Regulation | R/W | [0, 1200] | 0.1% | If 800 → adjust to 80.0%. MI |
| 041 | Active Power Regulation | R/W | [0, 1200] | 0.1% | If 800 → adjust to 80.0% |
| 042 | Reactive Power Regulation | R/W | [0, 1200] | 0.1% | If 800 → adjust to 80.0% |
| 043 | Apparent Power Regulation | R/W | [0, 0xFFFF] | — | — |

## Switch & Reset

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 044 | Switch On/Off Enable | R/W | [0, 1] | — | `0`: power off, `1`: power on |
| 045 | Factory Reset Enable | R/W | [0, 1] | — | — |
| 046 | Self-checking Time | R/W | [0, 1] | — | 0-360 seconds. MI |
| 047 | Absorption Charge Time | R/W | — | — | — |

## MPPT & Startup

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 048 | MPPT Number | R/W | — | — | — |
| 049 | Slow Start Enable (MI) | R/W | [0, 1] | — | `0`: disable, `1`: enable |

## Country Standards & Protocols

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 050 | CEI Self-check Enable | R/W | [0, 1] | — | `0`: disable, `1`: enable |
| 051 | RCD Enable | R/W | [0, 1] | — | `0`: disable, `1`: enable |
| 052 | Over-frequency De-rate Enable (MI) | R/W | [0, 1] | — | `0`: disable, `1`: enable |
| 053 | RISO Enable | R/W | [0, 1] | — | `0`: disable, `1`: enable |
| 054 | Grid Standard | R/W | [0, 20] | — | `1`: INMETRO, `2`: EN50549, `3`: EN50438, `4`: IEC61727, `5`: CUSTOM, `6`: VDE_AR_N_4105, `7`: UTE_C15_712_1, `8`: RD_1699, `9`: CEI_0_21, `10`: G98_G99, `11`: AS4777 |
| 055 | PV Curve Enable | R/W | [0, 1] | — | `0`: disable, `1`: enable |

## CT & Calibration

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 056 | CT Ratio | R/W | [1, 5000] | — | — |
| 057 | Max Solar Power (Old) | R/W | [0, 65536] | 10W or 1W | `10`: registers 167-190, value × 10W<br>`1`: registers 167-190, value × 1W |
| 058 | AC Power Ratio | R | [0, 2] | — | `100` = 1.00, `111` = 1.11 |
| 059 | Factory Test Command 1 | R/W | 0x0000 | — | Factory only |

**Register 059 bits:**
- Bit0: Enable test (subsequent bits take effect)
- Bit1: Enable all inverter fans
- Bit2: Flash all LEDs on display board, buzzer, backlight — red/yellow/blue
- Bit3: Enable lithium battery interface test
- Bit4: Enable Gen signal relay
- Bit5: Restart LCD program

## General Settings

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 060 | Limiter Function Enable | R/W | [0, 3] | — | — |
| 061 | Power WH Factor | R/W | 0x0000 | — | -0.01 |
| 062 | RSD Enable | R/W | 0x0001 | — | — |
| 063 | General Settings | R/W | 0x0001 | — | Bit0-1: `01` = show 16 strings + string current; `00` = don't show 16 strings<br>Bit2-3: `01` = show protection params 3-level settings; others = don't show |
