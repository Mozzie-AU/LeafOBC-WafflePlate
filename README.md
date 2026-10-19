# LeafOBC-WafflePlate

Reverse engineering the "waffle plate" power module from the **2012 Nissan Leaf on-board charger (OBC)**, with the goal of building a **functional replica from regular, off-the-shelf components**.

The original module looks like a hybrid power assembly: bare semiconductor dies wire-bonded onto a copper substrate and mounted in a moulded frame. When one fails, the charger is usually written off. A drop-in replacement made from discrete, readily available parts would let these chargers be repaired.

![Waffle plate, top side, stitched from 21 microscope images](images/stitched/waffle-plate-top.jpg)

> ⚠️ **High voltage.** The OBC works from mains AC and charges a traction battery of several hundred volts DC. Capacitors in the charger can hold a lethal charge after it is disconnected. Anything in this repo is provided for documentation and research, with no warranty. See the licence.

## Status

| Stage | State |
|---|---|
| Top-side imaging | ✅ Stitched (21 tiles, ~5300 × 4800 px) |
| Bottom side / connector pinout | ⬜ Not started |
| Component identification | ⬜ Not started |
| Circuit topology / schematic | ⬜ Not started |
| Replica schematic | ⬜ Not started |
| Replica PCB (KiCad) | ⬜ Not started |
| Bench test | ⬜ Not started |

## Repository layout

```
docs/              Notes, findings, component inventory, imaging method
images/raw/        Original microscope tiles, one folder per capture set
images/stitched/   Stitched mosaics
hardware/          Replica design files (KiCad), when they exist
tools/stitch/      Script that stitches microscope tiles into a mosaic
```

## Documents

- [Overview and open questions](docs/overview.md)
- [Component inventory](docs/component-inventory.md)
- [Imaging and stitching method](docs/imaging.md)

## Contributing

Information from anyone who has worked on Leaf (ZE0) chargers is very welcome. This includes failure modes, part markings, service documents and photos. Please open an issue or pull request.

## Licence

Hardware designs and documentation are released under the **CERN Open Hardware Licence v2 – Strongly Reciprocal** ([CERN-OHL-S-2.0](LICENSE)).

Nissan and Leaf are trademarks of Nissan Motor Co., Ltd. This project is independent and is not affiliated with or endorsed by Nissan.
