# LeafOBC-WafflePlate

Reverse engineering the "waffle plate" power module from the **2012 Nissan Leaf on-board charger (OBC)**, with the goal of building a **functional replica from regular, off-the-shelf components**.

The original module is a hybrid power assembly. It is a single-sided copper circuit on a ceramic substrate, bonded to an aluminium base plate, with bare semiconductor dies wire-bonded onto it and mounted in a moulded frame. When one fails, the charger is usually written off. A drop-in replacement made from discrete, readily available parts would let these chargers be repaired.

![Waffle plate, top side, stitched from 21 microscope images](images/stitched/waffle-plate-top.jpg)

> ⚠️ **High voltage.** The OBC works from mains AC and charges a traction battery of several hundred volts DC. Capacitors in the charger can hold a lethal charge after it is disconnected. Anything in this repo is provided for documentation and research, with no warranty. See the licence.

## Status

| Stage | State |
|---|---|
| Imaging | ✅ Stitched (21 tiles, ~5300 × 4800 px). The bottom is a plain aluminium plate, so it isn't imaged |
| Connector pinout | ⬜ Not started |
| Component identification | 🟡 Main semiconductors and shunts located ([map](images/annotated/component-map.jpg)) |
| Circuit topology / schematic | 🟡 First-pass KiCad schematic, unverified ([notes](docs/schematic-notes.md)) |
| Replica schematic | ⬜ Not started |
| Replica PCB (KiCad) | ⬜ Not started |
| Bench test | ⬜ Not started |

## Repository layout

```
docs/              Notes, findings, component inventory, imaging method
images/raw/        Original microscope tiles, one folder per capture set
images/stitched/   Stitched mosaics
hardware/          KiCad projects: original-module/ (reverse-engineered), replica later
tools/stitch/      Script that stitches microscope tiles into a mosaic
```

## Documents

- [Overview and open questions](docs/overview.md)
- [Schematic notes and verification checklist](docs/schematic-notes.md)
- [Component inventory](docs/component-inventory.md)
- [Imaging and stitching method](docs/imaging.md)

## Contributing

Information from anyone who has worked on Leaf (ZE0) chargers is very welcome. This includes failure modes, part markings, service documents and photos. Please open an issue or pull request.

## Licence

Hardware designs and documentation are released under the **CERN Open Hardware Licence v2 – Strongly Reciprocal** ([CERN-OHL-S-2.0](LICENSE)).

Nissan and Leaf are trademarks of Nissan Motor Co., Ltd. This project is independent and is not affiliated with or endorsed by Nissan.
