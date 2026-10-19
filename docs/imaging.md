# Imaging and stitching method

## Capture

- Digital microscope looking straight down at the module, tiles at 1920 × 1080.
- Tiles were shot in four quadrant groups: top-left, then down the left side, then top-right, then lower-right.
- 21 tiles cover the top side: [`images/raw/waffle-plate-top/`](../images/raw/waffle-plate-top/).

Tips for later capture sets:

- Overlap neighbouring tiles by about 30%.
- Lock exposure, white balance and focus. Varying exposure leaves visible brightness differences between tiles.
- Keep the module flat and square to the optics.
- Two small areas of the current top-side set have no coverage (black notches in the mosaic). Extra tiles there would fill them.

## Stitching

The tiles are a flat scan (translation), not a rotating-camera panorama. A normal Hugin panorama solve finds false matches between the many identical-looking die carriers, and these can pull the tiles tens of degrees out of square. [`tools/stitch/stitch_mosaic.py`](../tools/stitch/stitch_mosaic.py) avoids this:

1. Hugin `cpfind` finds control points between all tile pairs.
2. For each pair, only the points that agree on a single shift are kept. Pairs with fewer than 8 such points are discarded.
3. A robust least-squares solve finds each tile's translation, small rotation and scale.
4. Tiles are warped and blended with `enblend`.

On the top-side set this gives a median control-point error of about 1.8 px. The tiles needed less than 1° of rotation.

```bash
sudo apt install hugin-tools enblend
pip install numpy scipy opencv-python
python3 tools/stitch/stitch_mosaic.py images/raw/waffle-plate-top out.tif
```

### Doing it in the Hugin GUI instead

- Lens: rectilinear, HFOV about 10°. The exact value doesn't matter much at narrow FOV.
- Optimiser → custom parameters: tick **X, Y (translation)** only. Leave yaw, pitch, roll, FOV and distortion unticked.
- Delete control points between tiles that don't actually overlap before you optimise.
