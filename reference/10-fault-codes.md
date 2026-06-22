# Fault Codes

Fault codes, descriptions, and troubleshooting solutions.

| Code | Description | Solutions |
|:---|---|---|
| F07 | DC/DC Softstart Fault | 1. Check the battery fuse<br>2. Restart and check whether it is normal<br>3. Seek help from us if it cannot return to normal state |
| F10 | Auxiliary Power Supply Failure | 1. Wait for minutes then check<br>2. Remove WiFi plug or other communicator<br>3. Seek help from us if it cannot return to normal state |
| F13 | Working Mode Change (Mode Switching) | 1. Wait for a minute and check<br>2. Seek help from us if it cannot return to normal state |
| F17 | Active_Battery_Hold | — |
| F18 | AC Over Current Fault of Hardware | 1. Check whether backup load power and common load power are within range<br>2. Restart and check whether it is normal<br>3. Seek help from us if it cannot return to normal state |
| F20 | DC Over Current Fault of Hardware | 1. Check PV module connection and battery connection<br>2. Turn off DC switch and AC switch, wait one minute, then turn on DC/AC switch again<br>3. Seek help from us if it cannot return to normal state |
| F22 | Tz_EmergSStop_Fault (Emergency Stop — Inverter Locked) | Seek help from us. This failure hardly happens. |
| F23 | AC Leakage Current Transient Over Current | 1. Check the cable of PV module and inverter<br>2. Restart inverter<br>3. Seek help from us if it cannot return to normal state |
| F24 | DC Insulation Impedance Failure | 1. Check the connection of PV panels and inverter is firm and correct<br>2. Check whether the PE cable of inverter is connected to ground<br>3. Seek help from us if it cannot return to normal state |
| F25 | AC_Active_Batt_Fault | — |
| F26 | DC Busbar Unbalanced | 1. Please wait for a while and check whether it is normal<br>2. If still the same, turn off DC switch and AC switch, wait one minute, then turn on DC/AC switch<br>3. Seek help from us if it cannot return to normal state |
| F29 | Parallel CANBus Fault | Only for inverters working in parallel mode. 1. Check the parallel setting according to instructions<br>2. Check the connection of the CANBus<br>3. Seek help from us |
| F31 | Soft_Start_Failed | — |
| F35 | No AC Grid / No Utility | 1. Please confirm grid is lost or not<br>2. Check the grid connection is good or not<br>3. Check the switch between inverter and grid is on or not<br>4. Seek help from us if it cannot return to normal state |
| F37 | DCLLC_Soft_Over_Cur | — |
| F39 | DCLLC_Over_Current | — |
| F40 | Batt_Over_Current | — |
| F41 | Parallel System Stop | In parallel system, due to other inverter faults. 1. Wait for minutes then check all inverters in this parallel system<br>2. If inverter cannot return to normal, record fault codes of all inverters, then seek help from us |
| F42 | AC Line Low Voltage | 1. Check the AC voltage is in the range of standard voltage in specification<br>2. Check whether grid AC cables are firmly and correctly connected<br>3. Seek help from us if it cannot return to normal state |
| F46/F49 | Backup Battery Fault | 1. Check the battery capacity<br>2. Check the connection between batteries and inverters<br>3. If inverter cannot return to normal after load reduction, seek help from us |
| F47 | AC Over Frequency | 1. Check the frequency is in the range of specification or not<br>2. Check whether AC cables are firmly and correctly connected<br>3. Seek help from us if it cannot return to normal state |
| F48 | AC Lower Frequency | 1. Check the frequency is in the range of specification or not<br>2. Check whether AC cables are firmly and correctly connected<br>3. Seek help from us if it cannot return to normal state |
| F56 | DC Busbar Voltage Too Low | 1. Check whether battery voltage is too low<br>2. If battery voltage is too low, use PV or grid to charge the battery<br>3. Seek help from us if it cannot return to normal state |
| F58 | BMS Communication Fault | — |
| F60 | Gen_Volt_or_Fre_Fault | — |
| F61 | Button_Manual_OFF | — |
| F63 | ARC Fault | 1. ARC fault detection is only for US market<br>2. Check PV module cable connection and clear the fault<br>3. Seek help from us if it cannot return to normal state |
| F64 | Heat Sink High Temperature Failure | 1. Check whether the work environment temperature is too high<br>2. Turn off the inverter for 10 minutes and restart<br>3. Seek help from us if it cannot return to normal state |

> See the fault information coding tables (registers 100-103) for the full fault bit mapping.
