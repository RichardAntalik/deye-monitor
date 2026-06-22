# Hybrid Inverter Registers

This section covers registers specific to hybrid (storage) inverters, including battery configuration, generator settings, and advanced energy management.

## Battery Configuration (Registers 200-240)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 200 | Control Mode | R/W | — | — | `0x0000`: Lead-acid battery, four-stage charging; `0x0001`: Lithium battery |
| 201 | Equalization Voltage | R/W | [3800, 6100] | 0.01V | 1480 = 14.8V |
| 202 | Absorption Voltage | R/W | [3800, 6100] | 0.01V | 1440 = 14.4V |
| 203 | Float Voltage | R/W | [3800, 6100] | 0.01V | 1440 = 14.4V |
| 204 | Battery Capacity | R/W | [0, 2000] | 1Ah | 200 = 200Ah |
| 205 | Empty Voltage | R/W | — | 0.01V | — |
| 206 | Zero Export Power | R/W | — | — | — |
| 207 | Minimum Limter Active Power | R/W | — | — | — |
| 208 | Equalization Day Cycle | R/W | [0, 90] | Day | — |
| 209 | Equalization Time | R/W | [0, 20] | 0.5h | Resolution 0.5h. [0-20] = 0-10h, sent to MCU as [0-100] |
| 210 | TEMPCO (Temperature Compensation) | R/W | — | mV/°C | Signed int |
| 211 | Max Charge Current | R/W | [0, 185] | 1A | 0-185A |
| 212 | Max Discharge Current | R/W | [0, 185] | 1A | 0-185A |
| 213 | Undefined | R/W | 0, 1, 2 | — | — |
| 214 | Battery Operation Mode | R/W | — | — | According to voltage / According to capacity / No battery |
| 215 | Lithium Battery Wake Up | R/W | [0, 6000] | mΩ | `0`: enabled, `1`: disabled |
| 216 | Battery Resistance Value | R/W | [0, 6000] | mΩ | — |
| 217 | Battery Charging Efficiency | R/W | [0, 100] | 0.1% | 983 = 98.3% |
| 218 | Battery Capacity ShutDown | R/W | [0, 100] | 1% | Low capacity cutoff point |
| 219 | Battery Capacity Restart | R/W | [0, 100] | 1% | Protection recovery point |
| 220 | Battery Capacity LowBatt | R/W | [0, 100] | 1% | — |
| 221 | Battery Voltage ShutDown | R/W | [3800, 6100] | 0.01V | Low protection cutoff ~41V |
| 222 | Battery Voltage Restart | R/W | [3800, 6100] | 0.01V | Reboot/recover ~52V |
| 223 | Battery Voltage LowBatt | R/W | [3800, 6100] | 0.01V | — |
| 224 | Generator Max Operating Time | R/W | [0, 6300] | 0.1h | — |
| 225 | Generator Cooling Time | R/W | [0, 6300] | 1% | — |
| 226 | Generator Charging Start Voltage | R/W | [0, 6300] | 0.01V | Battery voltage below this → generator charges |
| 227 | Generator Charging Start Capacity | R/W | [0, 6300] | 1% | Battery capacity below this → generator charges |
| 228 | Generator Charge Battery Current | R/W | [0, 185] | 1A | — |
| 229 | Grid Charging Start Voltage | R/W | [0, 6300] | 0.01V | — |
| 230 | Grid Charging Start Capacity | R/W | [0, 6300] | 1% | — |
| 231 | Grid Charge Battery Current | R/W | [0, 185] | 1A | — |
| 232 | Generator Charge Enable | R/W | [0, 1] | — | — |
| 233 | Grid Charge Enable | R/W | [0, 1] | — | — |
| 234 | Solar Input as PSU | R/W | — | — | `0`: solar, `1`: PSU |
| 235 | Force Generator as Load | R/W | — | — | `0`: don't force; `1`: force |
| 236 | Generator Input as Load Output Enable | R/W | — | — | `0`: disable gen input; `1`: enable gen as load output; `2`: enable as inverter input |
| 237 | SmartLoad OFF Batt Voltage | R/W | [3800, 6300] | 0.01V | 46V |
| 238 | SmartLoad OFF Batt Capacity | R/W | [0, 100] | 1% | — |
| 239 | SmartLoad ON Batt Voltage | R/W | [3800, 6300] | 0.01V | 46V |
| 240 | SmartLoad ON Batt Capacity | R/W | [0, 100] | 1% | 120 = 12 hours |

## Advanced Energy Management (Registers 241-279)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 241 | Min Solar Power to Start Gen | R/W | [0, 8000] | 1W | Represents total power |
| 242 | Gen_Grid_Signal On | R/W | — | — | — |
| 243 | Energy Management Model | R/W | — | — | `0`: Battery priority mode; `1`: Load first mode |
| 244 | Limiter Control Function | R/W | [0, 00] | 1W | `0x00`: sell electricity enabled; `0x01`: built-in enabled; `0x02`: external enabled |
| 245 | Limit Max Grid Export Power | R/W | [0, 8000] | 1W | — |
| 246 | External CT Sensor Direction | R/W | — | — | — |
| 247 | Solar Sell | R/W | — | — | `0x00`: solar don't sell; `0x01`: solar sell |
| 248 | Time of Use Selling Enabled | R/W | [0, 1] | — | Bit0: disable/enable; Bit1-7: Mon-Sun enable; Bit8: Mode 3 (Spain customer) |

### Sell Mode Time Points (249-273)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 249 | Sell Mode Time Point 1 | R/W | [0, 2359] | — | 2359 = 23:59 |
| 250 | Sell Mode Time Point 2 | R/W | [0, 2359] | — | MCU range 0-287, sent as 2355 |
| 251 | Sell Mode Time Point 3 | R/W | [0, 2359] | — | — |
| 252 | Sell Mode Time Point 4 | R/W | [0, 2359] | — | — |
| 253 | Sell Mode Time Point 5 | R/W | [0, 2359] | — | — |
| 254 | Sell Mode Time Point 6 | R/W | [0, 2359] | — | — |
| 255 | Sell Mode Time Point 1 Power | R/W | [0, 8000] | 1W | Affected by max battery discharge power |
| 256 | Sell Mode Time Point 2 Power | R/W | [0, 8000] | 1W | — |
| 257 | Sell Mode Time Point 3 Power | R/W | [0, 8000] | 1W | — |
| 258 | Sell Mode Time Point 4 Power | R/W | [0, 8000] | 1W | — |
| 259 | Sell Mode Time Point 5 Power | R/W | [0, 8000] | 1W | — |
| 260 | Sell Mode Time Point 6 Power | R/W | [0, 8000] | 1W | — |
| 261 | Sell Mode Time Point 1 Voltage | R/W | [0, 6300] | 0.01V | Affected by battery voltage |
| 262 | Sell Mode Time Point 2 Voltage | R/W | [0, 6300] | 0.01V | — |
| 263 | Sell Mode Time Point 3 Voltage | R/W | [0, 6300] | 0.01V | — |
| 264 | Sell Mode Time Point 4 Voltage | R/W | [0, 6300] | 0.01V | — |
| 265 | Sell Mode Time Point 5 Voltage | R/W | [0, 6300] | 0.01V | — |
| 266 | Sell Mode Time Point 6 Voltage | R/W | [0, 6300] | 0.01V | — |
| 267 | Capacity 1 | R/W | [0, 100] | 1% | — |
| 268 | Capacity 2 | R/W | [0, 100] | 1% | — |
| 269 | Capacity 3 | R/W | [0, 100] | 1% | — |
| 270 | Capacity 4 | R/W | [0, 100] | 1% | — |
| 271 | Capacity 5 | R/W | [0, 100] | 1% | — |
| 272 | Capacity 6 | R/W | [0, 100] | 1% | — |

### Charge Enable Bits (273-278)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 273 | Time Point 1 Charge Enable | R/W | [0, 1] | — | Bit0: grid charge enable; Bit1: gen charge enable; Bit2: GM mode; Bit3: BU mode; Bit4: CH mode |
| 274 | Time Point 2 Charge Enable | R/W | [0, 1] | — | Same as above |
| 275 | Time Point 3 Charge Enable | R/W | [0, 1] | — | Same as above |
| 276 | Time Point 4 Charge Enable | R/W | [0, 1] | — | Same as above |
| 277 | Time Point 5 Charge Enable | R/W | [0, 1] | — | Same as above |
| 278 | Time Point 6 Charge Enable | R/W | [0, 1] | — | Same as above |

## System Configuration (Registers 279-310)

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 279 | Microinverter Export to Grid Cutoff | R/W | [0, 1] | — | — |
| 280 | External Sensor Auto-Detect Direction Enable | R/W | — | — | — |
| 281 | Restore Connection Time | R/W | [10, 300] | — | — |
| 282 | Solar Arc Fault Mode | R/W | [0, 1] | — | `0`: close, `1`: open, `0x02`: arc fault reset |
| 283 | Grid Mode | R/W | [0, 1] | — | `0`: general standard, `1`: UL1741&IEEE1547, `2`: CPUC Rule21, `3`: SRD-UL1741, `4`: CEI 0-21 |
| 284 | Grid Frequency | R/W | [0, 1] | — | `0`: 50Hz, `1`: 60Hz |
| 285 | Grid Type | R/W | [0, 3] | — | `0`: single-phase; `1`: two-phase 120V/240V; `2`: three-phase 208V 120°; `3`: 120V single-phase |
| 286 | Inverter Output Voltage Config | R/W | — | — | If 286==0: `0`:230V, `1`:220V, `2`:240V, `3`:200V<br>If 286==1: `0`:120/240V, `1`:110/220V, `2`:120/240V, `3`:110/200V<br>If 286==2: `0`:120/208V, `1`:127/220V |

**Register 286 additional bits:**
- Bit4-7: `0`: Gen peak-shaving disable; `1`: Gen peak-shaving enable
- Bit8-11: `0`: Grid peak-shaving disable; `1`: Grid peak-shaving enable
- Bit12: On-grid always on
- Bit13: External relay
- Bit14: Lithium battery loss fault enable
- Bit15: DRM enable

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 287 | Grid Vol High | R/W | [1800, 2700] | 0.1V | — |
| 288 | Grid Vol Low | R/W | [1800, 2700] | 0.1V | — |
| 289 | Grid Hz High | R/W | [4500, 6500] | 0.01Hz | — |
| 290 | Grid Hz Low | R/W | [4500, 6500] | 0.01Hz | — |
| 291 | Gen Connected to Grid Input | R/W | [1, 0] | — | — |
| 292 | Gen Peak Shaving Power | R/W | [0, 16000] | 1W | — |
| 293 | Grid Peak Shaving Power | R/W | [0, 16000] | 1W | — |
| 294 | SmartLoad Open Delay | R/W | [1, 120] | 1 Minute | — |
| 295 | Output PF Value Setting | R/W | [800, 1200] | — | 800 = 80%, 1200 = 120% |
| 296 | External Relay Bits | R/W | [0, 0xFFFF] | — | Bit0-8 correspond to 8 relay bits |
| 297-310 | ARC_Factory registers (B, I, F, D, T, C, Frz) | R/W | [0, 65535] | — | High word + Low word pairs |
| 311 | UPS Time | R/W | [0, 65535] | 1S | — |

## Hybrid Inverter Real-Time Data (Registers 150-195)

### Three-Phase Voltages

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 150 | Grid Side Voltage L1-N | R | — | 0.1V | — |
| 151 | Grid Side Voltage L2-N | R | — | 0.1V | — |
| 152 | Grid Side Voltage L1-L2 | R | — | 0.1V | — |
| 153 | Relay Middle Side Voltage L1-L2 | R | — | 0.1V | — |
| 154 | Inverter Output Voltage L1-N | R | — | 0.1V | — |
| 155 | Inverter Output Voltage L2-N | R | — | 0.1V | — |
| 156 | Inverter Output Voltage L1-L2 | R | — | 0.1V | — |
| 157 | Load Voltage L1 | R | — | 0.1V | — |
| 158 | Load Voltage L2 | R | — | 0.1V | — |
| 159 | Reserved | R | — | 0.1V | — |

### Currents

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 160 | Grid Side Current L1 | R | — | 0.01A | Signed int |
| 161 | Grid Side Current L2 | R | — | 0.01A | Signed int |
| 162 | Grid External Limter Current L1 | R | — | 0.01A | Signed int |
| 163 | Grid External Limter Current L2 | R | — | 0.01A | Signed int |
| 164 | Inverter Output Current L1 | R | — | 0.01A | Signed int |
| 165 | Inverter Output Current L2 | R | — | 0.01A | Signed int |
| 166 | Gen as Microinverter Input Power | R | — | Signed int | Output to storage = negative |
| 167 | Grid Side L1 Power | R | — | 1W | 10W: if reg54=0 |
| 168 | Grid Side L2 Power | R | — | 1W | 10W: if reg54=0 |
| 169 | Grid Power | R | — | 1W | >0: buy, <0: sell. 10W: if reg54=0 |
| 170 | Grid External Limter1 Power | R | — | 1W | 10W: if reg54=0 |
| 171 | Grid External Limter2 Power | R | — | 1W | 10W: if reg54=0 |
| 172 | Grid External Total Power | R | — | 1W | 10W: if reg54=0 |
| 173 | Inverter Output L1 Power | R | — | 1W | 10W: if reg54=0 |
| 174 | Inverter Output L2 Power | R | — | 1W | 10W: if reg54=0 |
| 175 | Inverter Output Total Power | R | — | 1W | 10W: if reg54=0 |
| 176 | Load Side L1 Power | R | — | 1W | 10W: if reg54=0 |
| 177 | Load Side L2 Power | R | — | 1W | 10W: if reg54=0 |
| 178 | Load Side Total Power | R | — | 1W | Signed int |

### Battery & Generator

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 179 | Load Current L1 | R | — | 0.01A | — |
| 180 | Load Current L2 | R | — | 0.01A | — |
| 181 | Gen Port Voltage | R | — | — | — |
| 182 | Battery Temperature | R | [0, 3000] | 0.1°C | Offset +1000: 1200 = 20.0°C |
| 183 | Battery Voltage | R | — | 0.01V | 4100 = 41.0V |
| 184 | Battery Capacity (SOC) | R | [0, 100] | 1% | — |
| 185 | Battery Status | R | — | — | — |
| 186 | PV1 Input Power | R | — | 1W | Signed int |
| 187 | PV2 Input Power | R | — | 1W | Signed int |
| 188 | PV3 Input Power | R | — | 1W | Signed int |
| 189 | PV4 Input Power | R | — | 1W | Signed int |
| 190 | Battery Output Power | R | — | 1W | Signed int |
| 191 | Battery Output Current | R | — | 0.01A | Signed int |
| 192 | Load Frequency | R | — | 0.01Hz | — |
| 193 | Inverter Output Frequency | R | — | 0.01Hz | — |
| 194 | Grid Side Relay Status | R | — | — | `0`: disconnect, `1`: closed |
| 195 | Generator Side Relay Status | R | — | — | Bit0-3: gen relay; Bit4-7: switch signal; Bit8-11: gen signal |

| Addr | Register Name | R/W | Data Range | Unit | Note |
|:---:|---|:---:|---|---|---|
| 196 | Gen Port Frequency | R | — | 0.01Hz | — |
