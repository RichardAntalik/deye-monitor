# Real-time Data Area

These registers contain live operational data from the inverter.

## Run State & Daily Energy

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 059 | Run State | R | [0, 5] | — | `0x0000`: Standby, `0x0001`: Self-check, `0x0002`: Normal, `0x0003`: Warning, `0x0004`: Fault |
| 060 | Day Active Power Wh | R | [-32768, 32767] | 0.1kWh | Signed int. MI |
| 061 | Day Reactive Power Wh | R | [-32768, 32767] | 0.1kVarh | Signed int |
| 062 | Today Gen Power Wh | R | [0, 65535] | 0.1kWh | — |
| 063 | Total Active Power Wh (Low Word) | R | [0, 0xFFFF] | 0.1kWh | Combined with 064 for 32-bit value |
| 064 | Total Active Power Wh (High Word) | R | [0, 0xFFFF] | 0.1kWh | — |
| 065 | Total Reactive Power Wh (Low Word) | R | [0, 0xFFFF] | 0.1kVarh | — |
| 066 | Total Reactive Power Wh (High Word) | R | [0, 0xFFFF] | 0.1kVarh | — |
| 067 | Month PV Power Wh (SG) | R | [0, 0xFFFF] | 0.1kWh | LCD statistics, DLN high/low reversed |
| 068 | Month Load Power Wh | R | [0, 0xFFFF] | 1kWh | — |
| 069 | Month Grid Power Wh (Hybrid) | R | [0, 0xFFFF] | 1kWh | SG: Grid当月卖电量 |
| 070 | Total Work Time (Low Word) | R | [0, 0xFFFF] | 0.1h | — |
| 071 | Total Work Time (High Word) | R | [0, 0xFFFF] | 0.1h | — |
| 072 | Year PV Power Wh (Low Word) | R | [0, 0xFFFF] | 0.1kWh | — |
| 073 | Year PV Power Wh (High Word) | R | [0, 0xFFFF] | 0.1kWh | — |

## Battery Data (Hybrid Inverters)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| — | Hybrid Battery 1 Current | R | — | 0.01A | MI |
| — | Hybrid Battery 2 Current | R | — | 0.01A | MI |
| 074 | Day Batt Charge Power Wh | R | [0, 9999] | 0.1kWh | — |
| 075 | Day Batt Discharge Power Wh | R | [0, 9999] | 0.1kWh | — |
| 076 | Total Batt Charge Power Wh (Low) | R | [0, 9999] | 0.1kWh | Hybrid |
| 077 | Total Batt Charge Power Wh (High) | R | [0, 9999] | 0.1kWh | Hybrid |
| 078 | Total Batt Discharge Power Wh (Low) | R | [0, 9999] | 0.1kWh | Hybrid |
| 079 | Total Batt Discharge Power Wh (High) | R | [0, 9999] | 0.1kWh | Hybrid |
| 080 | Day Grid Buy Power Wh | R | [0, 65535] | 0.1kWh | Hybrid |
| 081 | Day Grid Sell Power Wh | R | [0, 65535] | 0.1kWh | Hybrid |
| 082 | Total Grid Buy Power Wh (Low) | R | [0, 65535] | 0.1kWh | Hybrid |
| 083 | Total Grid Buy Power Wh (High) | R | [0, 65535] | 0.1kWh | Hybrid |
| 084 | Total Grid Sell Power Wh (Low) | R | [0, 65535] | 0.1kWh | Hybrid |
| 085 | Total Grid Sell Power Wh (High) | R | [0, 65535] | 0.1kWh | Hybrid |
| 086 | Day Load Power Wh | R | [0, 65535] | 0.1kWh | Hybrid / SG |
| 087 | Total Load Power Wh (Low) | R | [0, 0xFFFF] | 0.1kWh | Hybrid |
| 088 | Total Load Power Wh (High) | R | [0, 0xFFFF] | 0.1kWh | Hybrid |
| 089 | Year Load Power Wh (Low) | R | [0, 0xFFFF] | 0.1kWh | Hybrid |
| 090 | Year Load Power Wh (High) | R | [0, 0xFFFF] | 0.1kWh | Hybrid |
| 091 | Year Grid Sell Power Wh (Low) | R | [0, 65535] | 0.1kWh | Hybrid |
| 092 | Year Grid Sell Power Wh (High) | R | [0, 65535] | 0.1kWh | Hybrid |

## DC Inputs

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 112 | DC Voltage 1 | R | [0, 65535] | 0.1V | MI |
| 113 | DC Current 1 | R | [0, 65535] | 0.1A | MI |
| 114 | DC Voltage 2 | R | [0, 65535] | 0.1V | MI |
| 115 | DC Current 2 | R | [0, 65535] | 0.1A | MI |
| 116 | DC Voltage 3 | R | [0, 65535] | 0.1V | MI |
| 117 | DC Current 3 | R | [0, 65535] | 0.1A | MI |
| 118 | DC Voltage 4 | R | [0, 65535] | 0.1V | MI |
| 119 | DC Current 4 | R | [0, 65535] | 0.1A | MI |
| 120 | DC Voltage 5 | R | [0, 65535] | 0.1V | — |
| 121 | DC Current 5 | R | [0, 65535] | 0.1A | — |
| 122 | DC Voltage 6 | R | [0, 65535] | 0.1V | — |
| 123 | DC Current 6 | R | [0, 65535] | 0.1A | — |
| 124 | DC Voltage 7 | R | [0, 65535] | 0.1V | — |
| 125 | DC Current 7 | R | [0, 65535] | 0.1A | — |
| 126 | DC Voltage 8 | R | [0, 65535] | 0.1V | — |
| 127 | DC Current 8 | R | [0, 65535] | 0.1A | — |

## AC Output & Grid

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 093 | Power Factor | R | [0, 1000] | — | 1000 = SD fault, 2000 = normal |
| 094 | SD Card Status | R | [0, 0xFFFF] | — | — |
| — | Total Generator Power Wh (Low) | R | [0, 65535] | 0.1kWh | — |
| — | Total Generator Power Wh (High) | R | [0, 65535] | 0.1kWh | — |
| — | Grid Voltage AB | R | [0, 65535] | 0.1V | String inverter |
| — | Grid Voltage BC | R | [0, 65535] | 0.1V | String inverter |
| — | Grid Voltage AC | R | [0, 65535] | 0.1V | String inverter |
| — | Grid Voltage A | R | [0, 65535] | 0.1V | String inverter |
| — | Grid Voltage B | R | [0, 65535] | 0.1V | String inverter |
| — | Grid Voltage C | R | [0, 65535] | 0.1V | String inverter |
| — | Grid Current A | R | [0, 65535] | 0.1A | String inverter |
| — | Grid Current B | R | [0, 65535] | 0.1A | String inverter |
| — | Grid Current C | R | [0, 65535] | 0.1A | String inverter |
| — | Grid Frequency | R | [0, 65535] | 0.01Hz | — |

## Power Output

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| — | Display Power High Bytes | R | 0x0000 | 0.1W | — |
| — | Display Power Low Bytes | R | 0x0000 | 0.1W | — |
| — | Input Active Power (Low) | R | [0, 0xFFFF] | 0.1W | String inverter |
| — | Input Active Power (High) | R | [0, 0xFFFF] | 0.1W | String inverter |
| — | Output Apparent Power (Low) | R | [0, 0xFFFF] | 0.1VA | String inverter |
| — | Output Apparent Power (High) | R | [0, 0xFFFF] | 0.1VA | String inverter |
| — | Output Active Power (Low) | R | [0, 0xFFFF] | 0.1W | String inverter |
| — | Output Active Power (High) | R | [0, 0xFFFF] | 0.1W | String inverter |
| — | Output Reactive Power (Low) | R | [0, 0xFFFF] | 0.1Var | String inverter |
| — | Output Reactive Power (High) | R | [0, 0xFFFF] | 0.1Var | String inverter |
| — | Generator Daily Operating Time | R | [0, 65535] | 0.1h | 240 = 24 hours |
| — | Limiter Power | R | 0x0000 | 1W | String inverter |

## Temperatures

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| — | Radiator Temperature (DC Transformer) | R | [0, 3000] | 0.1°C | -56.2°C = 438, 0°C = 1000, 50.5°C = 1505 |
| — | IGBT Temperature (Radiator) | R | [0, 3000] | 0.1°C | Same scale as above |

## Energy per String/Component

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| — | Component 1 Day Power Wh | R | [0, 65535] | 0.1kWh | MI |
| — | Component 2 Day Power Wh | R | [0, 65535] | 0.1kWh | MI |
| — | Component 3 Day Power Wh | R | [0, 65535] | 0.1kWh | MI |
| — | Component 4 Day Power Wh | R | [0, 65535] | 0.1kWh | MI |
| — | Component 1 Total Power (Low) | R | [0, 65535] | 0.1kWh | MI |
| — | Component 1 Total Power (High) | R | [0, 65535] | 0.1kWh | MI |
| — | Component 2 Total Power (Low) | R | [0, 65535] | 0.1kWh | MI |
| — | Component 2 Total Power (High) | R | [0, 65535] | 0.1kWh | MI |
| — | Component 3 Total Power (Low) | R | [0, 65535] | 0.1kWh | MI |
| — | Component 3 Total Power (High) | R | [0, 65535] | 0.1kWh | MI |
| — | Component 4 Total Power (Low) | R | [0, 65535] | 0.1kWh | MI |
| — | Component 4 Total Power (High) | R | [0, 65535] | 0.1kWh | MI |
| — | Inverter Efficiency | R | [0, 1000] | 0.1% | — |
| — | History PV Power Wh (Low) | R | [0, 0xFFFFFFFF] | 0.1kWh | 32-bit combined |
| — | History PV Power Wh (High) | R | [0, 0xFFFFFFFF] | 0.1kWh | — |

## Status Flags

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 098 | Alarms Status 1 | R | [0, 65535] | — | See alarm coding table |
| 099 | Alarms Status 2 | R | [0, 65535] | — | See alarm coding table |
| 100 | Fault Information Word 1 | R | [0, 65535] | — | See fault coding table. MI |
| 101 | Fault Information Word 2 | R | [0, 65535] | — | See fault coding table |
| 102 | Fault Information Word 3 | R | [0, 65535] | — | See fault coding table |
| 103 | Fault Information Word 4 | R | [0, 65535] | — | See fault coding table |
| 104 | Corrected Battery AH | R | [0, 65535] | 1AH | 100 = 100AH |
| 105 | Day PV Power Wh | R | [0, 65535] | 0.1kWh | — |
| 106 | Other Test Flag Bits | R | 0x0000 | — | Bit0: Arc communication sign<br>Bit1: Parallel CAN communication (1 = normal)<br>Bit8: Li-ion battery interface RS485<br>Bit9: Li-ion battery interface CAN<br>Bit10: Buttons 1-2-3-4<br>Bit11: LCD interrupt status (1 = normal) |

## RCD

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| — | String Inverter RCD Leak Current | R | [0, 65535] | 0.01A | — |
