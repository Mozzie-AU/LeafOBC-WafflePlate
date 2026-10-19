# Overview

## Subject

- **Vehicle:** 2012 Nissan Leaf (ZE0)
- **Assembly:** on-board charger (OBC)
- **Part:** internal power module, nicknamed the "waffle plate"
- **Original part number / markings:** _TBD_

## Observations so far (top side)

From the stitched image in [`images/stitched/waffle-plate-top.jpg`](../images/stitched/waffle-plate-top.jpg):

- The power semiconductors are **bare dies, wire-bonded** onto copper pads, rather than packaged parts. Each sits on a copper "tab" carrier with leads, in a package-like footprint.
- The substrate is divided into several distinct copper regions, which suggests separate power stages. The groupings are listed below.
- Lead frames / press-fit pins run along the left and right edges.
- There is a round feature (blue centre, dark surround) between the upper-right and lower-right regions. Its purpose is _TBD_ (mounting point? sensor?).
- The lower-right region has fine-pitch traces and small passives that look like gate-drive or sensing circuitry.

### Regions (provisional)

| Region | Contents | Notes |
|---|---|---|
| Upper left | 4 die carriers, 2 bridging links | |
| Middle left | 3 die carriers, small-signal parts | |
| Lower left | 2 die carriers | |
| Upper right | 10 die carriers | |
| Lower right | ~8 die carriers, passives, fine traces | Possible drive/sense |

_The die counts are from a first visual pass and need checking._

## Open questions

- [ ] What is each die (MOSFET, IGBT, diode)? Are there markings on the die?
- [ ] What topology does the module implement (PFC boost, full bridge, rectifier…)?
- [ ] What is the pinout of the edge connectors to the rest of the charger?
- [ ] How is the module cooled and mounted, and what thermal interface does it use?
- [ ] What voltage and current ratings does each stage need?
- [ ] What are the known failure modes in the field?

## Replica approach (draft)

Replace each bare die with a packaged discrete part of equal or better rating (for example TO-247 or D2PAK). Mount them on a PCB or IMS board that matches the original module's footprint and connector positions, so it can drop into the existing charger housing.
