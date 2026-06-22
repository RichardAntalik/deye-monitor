# String Inverter Registers

This section covers registers specific to string inverters, including variable attributes and real-time data unique to this inverter type.

## Variable Attributes (String Inverter)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 300 | Grid Voltage Upper Limit Stage 2 | R/W | [1600, 5500] | 0.1V | — |
| 301 | Grid Voltage Upper Limit Stage 3 | R/W | [1600, 5500] | 0.1V | — |
| 302 | Grid Voltage Lower Limit Stage 2 | R/W | [1600, 5500] | 0.1V | — |
| 303 | Grid Voltage Lower Limit Stage 3 | R/W | [1600, 5500] | 0.1V | — |
| 304 | Grid Frequency Upper Limit Stage 2 | R/W | [4500, 6500] | 0.01Hz | — |
| 305 | Grid Frequency Upper Limit Stage 3 | R/W | [4500, 6500] | 0.01Hz | — |
| 306 | Grid Frequency Lower Limit Stage 2 | R/W | [4500, 6500] | 0.01Hz | — |
| 307 | Grid Frequency Lower Limit Stage 3 | R/W | [4500, 6500] | 0.01Hz | — |
| 308 | Grid Voltage Upper Trip Time Stage 1 | R/W | [5, 65000] | 10ms | — |
| 309 | Grid Voltage Upper Trip Time Stage 2 | R/W | [5, 65000] | 10ms | — |
| 310 | Grid Voltage Upper Trip Time Stage 3 | R/W | [5, 65000] | 10ms | — |
| 311 | Grid Voltage Lower Trip Time Stage 1 | R/W | [5, 65000] | 10ms | — |
| 312 | Grid Voltage Lower Trip Time Stage 2 | R/W | [5, 65000] | 10ms | — |
| 313 | Grid Voltage Lower Trip Time Stage 3 | R/W | [5, 65000] | 10ms | — |
| 314 | Grid Frequency Upper Trip Time Stage 1 | R/W | [5, 65000] | 10ms | — |
| 315 | Grid Frequency Upper Trip Time Stage 2 | R/W | [5, 65000] | 10ms | — |
| 316 | Grid Frequency Upper Trip Time Stage 3 | R/W | [5, 65000] | 10ms | — |
| 317 | Grid Frequency Lower Trip Time Stage 1 | R/W | [5, 65000] | 10ms | — |
| 318 | Grid Frequency Lower Trip Time Stage 2 | R/W | [5, 65000] | 10ms | — |
| 319 | Grid Frequency Lower Trip Time Stage 3 | R/W | [5, 65000] | 10ms | — |

## String Current & Energy (Registers 150-195)

This range is only for string inverters.

### String Currents (16 strings)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 150 | String 1 Current | R | [0, 65535] | 0.1A | — |
| 151 | String 2 Current | R | [0, 65535] | 0.1A | — |
| 152 | String 3 Current | R | [0, 65535] | 0.1A | — |
| 153 | String 4 Current | R | [0, 65535] | 0.1A | — |
| 154 | String 5 Current | R | [0, 65535] | 0.1A | — |
| 155 | String 6 Current | R | [0, 65535] | 0.1A | — |
| 156 | String 7 Current | R | [0, 65535] | 0.1A | — |
| 157 | String 8 Current | R | [0, 65535] | 0.1A | — |
| 158 | String 9 Current | R | [0, 65535] | 0.1A | — |
| 159 | String 10 Current | R | [0, 65535] | 0.1A | — |
| 160 | String 11 Current | R | [0, 65535] | 0.1A | — |
| 161 | String 12 Current | R | [0, 65535] | 0.1A | — |
| 162 | String 13 Current | R | [0, 65535] | 0.1A | — |
| 163 | String 14 Current | R | [0, 65535] | 0.1A | — |
| 164 | String 15 Current | R | [0, 65535] | 0.1A | — |
| 165 | String 16 Current | R | [0, 65535] | 0.1A | — |

### String Energy (Daily) — Low & High Bytes

Each string has 2 registers (low byte + high byte) for daily energy.

| Addr | Register Name | R/W | Data Range | Unit |
|:---:|---|:---:|---|---|
| 166 | String 1 Energy (Low Byte) | R | [0, 65535] | 0.1kWh |
| 167 | String 1 Energy (High Byte) | R | [0, 65535] | 0.1kWh |
| 168 | String 2 Energy (Low Byte) | R | [0, 65535] | 0.1kWh |
| 169 | String 2 Energy (High Byte) | R | [0, 65535] | 0.1kWh |
| 170 | String 3 Energy (Low Byte) | R | [0, 65535] | 0.1kWh |
| 171 | String 3 Energy (High Byte) | R | [0, 65535] | 0.1kWh |
| 172 | String 4 Energy (Low Byte) | R | [0, 65535] | 0.1kWh |
| 173 | String 4 Energy (High Byte) | R | [0, 65535] | 0.1kWh |
| 174 | String 5 Energy (Low Byte) | R | [0, 65535] | 0.1kWh |
| 175 | String 5 Energy (High Byte) | R | [0, 65535] | 0.1kWh |
| 176 | String 6 Energy (Low Byte) | R | [0, 65535] | 0.1kWh |
| 177 | String 6 Energy (High Byte) | R | [0, 65535] | 0.1kWh |
| 178 | String 7 Energy (Low Byte) | R | [0, 65535] | 0.1kWh |
| 179 | String 7 Energy (High Byte) | R | [0, 65535] | 0.1kWh |
| 180 | String 8 Energy (Low Byte) | R | [0, 65535] | 0.1kWh |
| 181 | String 8 Energy (High Byte) | R | [0, 65535] | 0.1kWh |
| 182 | String 9 Energy (Low Byte) | R | [0, 65535] | 0.1kWh |
| 183 | String 9 Energy (High Byte) | R | [0, 65535] | 0.1kWh |
| 184 | String 10 Energy (Low Byte) | R | [0, 65535] | 0.1kWh |
| 185 | String 10 Energy (High Byte) | R | [0, 65535] | 0.1kWh |
| 186 | String 11 Energy (Low Byte) | R | [0, 65535] | 0.1kWh |
| 187 | String 11 Energy (High Byte) | R | [0, 65535] | 0.1kWh |
| 188 | String 12 Energy (Low Byte) | R | [0, 65535] | 0.1kWh |
| 189 | String 12 Energy (High Byte) | R | [0, 65535] | 0.1kWh |
| 190 | String 13 Energy (Low Byte) | R | [0, 65535] | 0.1kWh |
| 191 | String 13 Energy (High Byte) | R | [0, 65535] | 0.1kWh |
| 192 | String 14 Energy (Low Byte) | R | [0, 65535] | 0.1kWh |
| 193 | String 14 Energy (High Byte) | R | [0, 65535] | 0.1kWh |
| 194 | String 15 Energy (Low Byte) | R | [0, 65535] | 0.1kWh |
| 195 | String 15 Energy (High Byte) | R | [0, 65535] | 0.1kWh |

| Addr | Register Name | R/W | Data Range | Unit |
|:---:|---|---|---|---|
| 196 | String 16 Energy (Low Byte) | R | [0, 65535] | 0.1kWh |
| 197 | String 16 Energy (High Byte) | R | [0, 65535] | 0.1kWh |

## Meter & Load Data (Registers 198-218)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 198 | Load Active Power (Low) | R | [0, 65535] | 1W | Signed int |
| 199 | Load Active Power (High) | R | [0, 65535] | 1W | — |
| 200 | Day Load Power Wh | R | [0, 65535] | 0.01kWh | — |
| 201 | History Load Power Wh (Low) | R | [0, 65535] | 0.1kWh | — |
| 202 | History Load Power Wh (High) | R | [0, 65535] | 0.1kWh | — |
| 203 | Meter Active Power (Low) | R | [0, 65535] | 1W | Signed int, buy = negative, sell = positive |
| 204 | Meter Active Power (High) | R | [0, 65535] | 1W | — |
| 205 | Day Grid Sell Power Wh | R | [0, 65535] | 0.01kWh | — |
| 206 | History Grid Sell Power Wh (Low) | R | [0, 65535] | 0.1kWh | — |
| 207 | History Grid Sell Power Wh (High) | R | [0, 65535] | 0.1kWh | — |
| 208 | Day Grid Buy Power Wh | R | [0, 65535] | 0.01kWh | — |
| 209 | History Grid Buy Power Wh (Low) | R | [0, 65535] | 0.1kWh | — |
| 210 | History Grid Buy Power Wh (High) | R | [0, 65535] | 0.1kWh | — |
