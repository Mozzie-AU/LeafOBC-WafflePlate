# Schematic notes: original module

Schematic: [`hardware/original-module/waffle-plate.kicad_sch`](../hardware/original-module/waffle-plate.kicad_sch) (KiCad 7 format, opens in KiCad 7 or later). There is a PDF copy alongside it.
Component map: [`images/annotated/component-map.jpg`](../images/annotated/component-map.jpg)

> **Status: first pass, unverified.** The topology comes from the community draft schematic (mynissanleaf.com thread *"Onboard charger failed 2012 but cannot find cause"*), plus part numbers identified on the module and a visual read of the stitched image. Nothing has been confirmed with a meter yet. Every part has a hidden `Verified` field set to `no`. Change it to `yes` once that part's connections are confirmed.

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
               VREC- ─► RS1 shunt ─► PGND        Q1-Q3 (parallel) ──┤ to PGND
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
| D1–D4 | DF25V60 | 4 | AC input bridge | Part: confirmed. Role per position: TBD |
| Q1–Q3 | RJP6012 | 3 | PFC switch, paralleled | Part: confirmed |
| R1–R3 | ? | 3 | PFC gate resistors | From draft |
| Q4, Q5 | NPN / PNP | 2 | PFC gate-driver totem pole | From draft. Parts and location TBD |
| D5, D6 | ? | 2 | PFC boost diodes, paralleled | Part number TBD |
| Q6–Q13 | RJP6012 | 8 | Full bridge, 2 per switch | Part: confirmed. Pair-to-switch assignment TBD |
| D7–D10 | ? | 4 | Freewheel diode, one per switch | Part number TBD |
| D11–D20 | DF20L60U | 10 | Output rectifier (draft URD1–URD10) | Part: confirmed. Topology from draft |
| RS1–RS3 | shunt | 3 | Current sense with Kelvin connections | Values TBD. RS2 function TBD |

## Upper-right physical mapping (hypothesis)

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

1. Pad J1 (L) and J4 (N) to the bridge: one DF25V60 drop (~0.5 V) to J7, and to the input shunt.
2. Pick one pair of each IGBT group and confirm C–C and E–E continuity, which shows they are in parallel.
3. Find which full-bridge group connects to P (J27/J28) on its collectors. Those are the high-side switches.
4. Confirm p23 (T1) and p25 (T4) are the two bridge midpoints.
5. Confirm the rectifier table above, then fill in h, i, j.
6. Trace both sense pins of each shunt to a module pad.
7. Map the remaining pads: J8, J12/J13, J15, J30/J31, p27, p29, p31, p32, p33. These are probably gate drive and sense pairs.
8. Record the gate and gate-emitter resistor values around Q6–Q13.

## Things noticed

- The dies of Q8 and Q9 (bottom-left full-bridge pair) each have a round spot in the centre, and their leads look disturbed compared with the other six. This could be failure damage or an artefact of the laser stripping. It needs a closer look.
