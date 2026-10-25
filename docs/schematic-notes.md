# Schematic notes: original module

Schematic: [`hardware/original-module/waffle-plate.kicad_sch`](../hardware/original-module/waffle-plate.kicad_sch) (KiCad 7 format, opens in KiCad 7 or later). There is a PDF copy alongside it.
Component map: [`images/annotated/component-map.jpg`](../images/annotated/component-map.jpg)

> **Status:** Ray has meter-verified the input bridge (D1–D4), the input shunt and its sense connections (RS1, RS2), and the output rectifier (D11–D20) with their pads. These parts are drawn with real wires and have `Verified = yes`.
>
> The PFC stage (section B) is also wired. Its gate driver (Q4, Q5, R4, R8, C4) is meter-verified. The rest of section B (IGBTs, gate resistors, boost diodes) is believed correct but not yet meter-checked, so those parts stay `Verified = no`.
>
> The full bridge (section C), RS3 and the remaining pads are still a first pass that uses net labels.
>
> The unverified topology comes from the community draft schematic (mynissanleaf.com thread *"Onboard charger failed 2012 but cannot find cause"*), plus part numbers identified on the module and a visual read of the stitched image. Nothing has been confirmed with a meter yet. Every part has a hidden `Verified` field set to `no`. Change it to `yes` once that part's connections are confirmed.

## Conventions

- Connectivity is set by **net labels on every pin**. To change a connection, rename the label.
- Hidden fields on each part:
  - `Draft_ref`: the part's name on the community draft (ULQD1, LLQ1, URD3 …)
  - `Location_px`: pixel position in [`images/stitched/waffle-plate-top.jpg`](../images/stitched/waffle-plate-top.jpg)
  - `Verified`: `yes` or `no`
  - `Note`: anything open
- `P1`…`P25` are module pads. Each pad's value is its draft pad name (J1 L, p23 T1 …).
- Off-module parts (PFC inductor, bulk capacitors, transformers) are drawn for context. They are marked not in BOM and not on board.

## Topology

```
AC_L/AC_N ─► D1-D4 bridge ─► VREC+ ─► L1 (295µH, off-module) ─► PFC_SW
                 │                                                  │
               VREC- ─► RS1+RS2 ─► PGND       Q1-Q3 (parallel) ──┤ to PGND
                                                 D5, D6 (parallel) ─┴─► HV_BUS+ (≈350 V, C1-C3 off-module)

HV_BUS+ ─► full bridge: 4 switches × (2 × RJP6012 in parallel + 1 freewheel diode)
           BR_A / BR_B ─► T1 + T2 primaries (off-module) ; return HB_N ─► RS3 shunt ─► PGND

T1 sec (T5,T6) ─► bridge D11,D14,D15,D18 ┐
                                         ├ series-stacked ─► OUT_P (P0) / OUT_N (N0)
T2 sec (T7,T8) ─► bridge D16,D17,D19,D20 ┘   D12, D13 bypass each bridge
```

## Part summary

| Ref | Part | Qty | Function | Confidence |
|---|---|---|---|---|
| D1–D4 | DF25V60 | 4 | AC input bridge | Verified |
| Q1–Q3 | RJP6012 | 3 | PFC switch, paralleled | Part confirmed. Netlist believed correct |
| R1–R3 | ? | 3 | PFC gate resistors, one per IGBT | Netlist believed correct. Values TBD |
| Q4, Q5 | NPN / PNP (BCX56-16 / BCX53-16 type) | 2 | PFC gate-driver emitter follower | Verified. See [PFC gate driver](pfc-gate-driver.md) |
| R8, C4 | 43 Ω, 1 µF | 2 | Driver supply resistor (VDRV to VDRV_F) and decoupling to PGND | Verified. VDRV pad not yet assigned |
| R4 | 10 kΩ | 1 | PFC gate pull-down (PFC_GDRV to PGND) | Verified |
| D5, D6 | ? | 2 | PFC boost diodes, paralleled | Netlist believed correct. Part number TBD |
| Q6–Q13 | RJP6012 | 8 | Full bridge, 2 per switch | Part confirmed. Switch assignment read from the copper (Q6/Q7 AH, Q8/Q9 AL, Q10/Q11 BH, Q12/Q13 BL), matching the schematic. See [full-bridge gate network](full-bridge-gate-drive.md) |
| D7–D10 | ? | 4 | Freewheel diode, one per switch | Part number TBD. Both outer leads are anode, tab is cathode |
| R11–R44, C11–C42 | 10 Ω? / 1 kΩ? / 1 nF? | 24 | Gate network, 6 parts per switch | Topology traced (BH, BL) or by analogy (AH, AL). Values unconfirmed. See [full-bridge gate network](full-bridge-gate-drive.md) |
| D11–D20 | DF20L60U | 10 | Output rectifier (draft URD1–URD10) | Verified |
| RS1, RS2 | shunt | 2 | Input return shunt: two parts in series, Kelvin sense from the outer terminals to J10 and J11 (via net ties NT1, NT2) | Connections verified. Values TBD |
| RS3 | shunt | 1 | Full-bridge return | Unverified. The Ukrainian schematic shows R16 0 Ω, so possibly a link. Drawn in section A |

## Upper-right physical mapping (hypothesis, to be filled in from the verified netlist)

On every DF20L60U the **tab is the cathode**. One outer lead is wire-bonded to the tab (cathode) and the other is bonded to the die (anode). The middle lead is trimmed. Letters refer to [`component-map.jpg`](../images/annotated/component-map.jpg). The copper "islands" are read from the image only.

| Pkg | Cathode island | Anode island | Likely draft ref |
|---|---|---|---|
| d | MID | N0 | URD3 (bypass) |
| g | T-node X | N0 | URD7 or URD10 |
| f | MID | T-node X | URD6 or URD9 |
| c | T-node Y | MID | URD5 or URD8 |
| e | T-node Z | MID | URD5 or URD8 |
| a, b | P0 | (separate islands) | two of URD1, URD2, URD4 |
| h, i, j | not yet read | | |

## Verification checklist (meter, diode-test mode)

1. ~~Input bridge and shunt~~ (verified).
2. Pick one pair of each IGBT group and confirm C–C and E–E continuity, which shows they are in parallel.
3. Find which full-bridge group connects to P (J27/J28) on its collectors. Those are the high-side switches.
4. Confirm p23 (T1) and p25 (T4) are the two bridge midpoints.
5. ~~Rectifier netlist~~ (verified). Still to record: which package letter (a)–(j) is which D11–D20.
6. Trace RS3's sense pins to module pads (RS1/RS2 done).
7. Map the remaining pads: J8, J12/J13, J15, J30/J31, p27, p29, p31, p32, p33. These are probably gate drive and sense pairs.
8. Gate network around Q6–Q13: traced for the right-hand switches, with meter checks listed in [full-bridge-gate-drive.md](full-bridge-gate-drive.md). Values need a second module.

## Things noticed

- The dies of Q8 and Q9 (bottom-left full-bridge pair) each have a round spot in the centre, and their leads look disturbed compared with the other six. This could be failure damage or an artefact of the laser stripping. It needs a closer look.
