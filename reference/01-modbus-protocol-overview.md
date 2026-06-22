# Modbus RTU Protocol Overview

## Communication Parameters

- **Baud rate:** 9600bps
- **Interface:** RS232 or RS485

## General Notes

- Reserved words, reserved bytes, reserved bits, and unsupported registers are all filled with `0x00`.
- This protocol is for Microinverter, String Inverter, and Storage Inverter.

---

## Function Codes

The following table lists only the function codes used in this protocol.

| Function Code | Type | Description |
|:---:|---|---|
| `0x03` | Public function code | Read register — contains reads to a single register and multiple registers |
| `0x10` | Public function code | Write register — contains writes to a single register and multiple registers |

---

## 0x03 — Read Register

### Request PDU

| Data Structure | Data Length | Data Range |
|---|---|---|
| Function code | 1 byte | `0x03` |
| Starting register address | 2 bytes | `0x0000` ~ `0xFFFF` |
| Number of registers | 2 bytes | `0x0001` ~ `0x007D` |

### Normal Response PDU

| Data Structure | Data Length | Data Range |
|---|---|---|
| Function code | 1 byte | `0x03` |
| Byte count | 1 byte | `0x0001` ~ `0x007D` |
| Register values | N × 2 bytes | `0x0000` ~ `0xFFFF` |

> **Note:** N = number of registers

### Abnormal Response PDU

| Data Structure | Data Length | Data Range |
|---|---|---|
| Function code | 1 byte | `0x83` |
| Exception code | 1 byte | See exception codes |

### Example — Read 3 consecutive registers starting at address 107

**Request:**

| Field Name | Field Value |
|---|---|
| Function code | `0x03` |
| Starting address Hi | `0x00` |
| Starting address Lo | `0x6B` |
| Number of registers Hi | `0x00` |
| Number of registers Lo | `0x03` |

**Normal Response:**

| Field Name | Field Value |
|---|---|
| Function code | `0x03` |
| Byte count | `0x06` |
| Register [107] Hi | `0x00` |
| Register [107] Lo | `0x00` |
| Register [108] Hi | `0x00` |
| Register [108] Lo | `0x64` |
| Register [109] Hi | `0x00` |
| Register [109] Lo | `0x00` |

**Abnormal Response:**

| Field Name | Field Value |
|---|---|
| Function code | `0x83` |
| Exception code | `0x04` |

---

## 0x10 — Write Register

### Request PDU

| Data Structure | Data Length | Data Range |
|---|---|---|
| Function code | 1 byte | `0x10` |
| Starting register address | 2 bytes | `0x0000` ~ `0xFFFF` |
| Number of registers | 2 bytes | `0x0001` ~ `0x007B` |
| Byte count | 1 byte | N × 2 bytes |
| Register values | N × 2 bytes | — |

> **Note:** N = number of registers

### Normal Response PDU

| Data Structure | Data Length | Data Range |
|---|---|---|
| Function code | 1 byte | `0x10` |
| Starting register address | 2 bytes | `0x0000` ~ `0xFFFF` |
| Number of registers | 2 bytes | `0x0001` ~ `0x007B` |

### Abnormal Response PDU

| Data Structure | Data Length | Data Range |
|---|---|---|
| Function code | 1 byte | `0x90` |
| Exception code | 1 byte | See exception codes |

### Example — Write `0x000A` and `0x0102` to 2 registers starting at address 1

**Request:**

| Field Name | Field Value |
|---|---|
| Function code | `0x10` |
| Starting address Hi | `0x00` |
| Starting address Lo | `0x01` |
| Number of registers Hi | `0x00` |
| Number of registers Lo | `0x02` |
| Byte count | `0x04` |
| Register value Hi (first) | `0x00` |
| Register value Lo (first) | `0x0A` |
| Register value Hi (second) | `0x01` |
| Register value Lo (second) | `0x02` |

**Normal Response:**

| Field Name | Field Value |
|---|---|
| Function code | `0x10` |
| Starting address Hi | `0x00` |
| Starting address Lo | `0x01` |
| Number of registers Hi | `0x00` |
| Number of registers Lo | `0x02` |

**Abnormal Response:**

| Field Name | Field Value |
|---|---|
| Function code | `0x90` |
| Exception code | `0x04` |
