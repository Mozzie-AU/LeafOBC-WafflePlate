#!/usr/bin/env python3
"""Stitch a folder of flat microscope tiles into one high-resolution mosaic.

Designed for top-down microscope scans of a flat PCB, where tiles differ by
X/Y translation (plus tiny rotation/scale) rather than by camera rotation as
in a normal panorama.

Pipeline:
  1. Hugin `pto_gen` + `cpfind` find control points between every tile pair.
  2. Each pair is filtered to points that agree on one consistent shift
     (rejects false matches on repeated features such as identical MOSFETs).
  3. A robust least-squares solve finds a similarity transform per tile
     (translation + small rotation + scale).
  4. Tiles are warped and blended with `enblend`.

Requires: hugin-tools, enblend, python3 with numpy, scipy, opencv-python.
  sudo apt install hugin-tools enblend
  pip install numpy scipy opencv-python

Usage:
  stitch_mosaic.py INPUT_DIR OUTPUT.tif [--anchor N] [--min-inliers 8]
"""
import argparse
import collections
import glob
import os
import re
import subprocess
import sys
import tempfile

import cv2
import numpy as np
from scipy.optimize import least_squares

EXTS = ("*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG", "*.tif", "*.TIF")


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd)}\n{r.stderr[-2000:]}")
    return r


def find_control_points(files, work):
    a, b = os.path.join(work, "a.pto"), os.path.join(work, "b.pto")
    run(["pto_gen", "-o", a, "-p", "0", "-f", "10"] + files)
    run(["cpfind", "--fullscale", "--sieve2size", "5", "-o", b, a])
    pairs = collections.defaultdict(list)
    for line in open(b):
        if line.startswith("c "):
            d = {k: float(v) for k, v in re.findall(r" ([nNxyXY])(-?[\d.]+)", line)}
            pairs[(int(d["n"]), int(d["N"]))].append((d["x"], d["y"], d["X"], d["Y"]))
    return pairs


def filter_pairs(pairs, min_inliers, tol=10.0):
    """Keep, per pair, the largest set of points agreeing on one translation."""
    I, J, A, B, kept = [], [], [], [], []
    for (i, j), pts in pairs.items():
        pts = np.array(pts)
        off = pts[:, :2] - pts[:, 2:]
        best = None
        for c in off:
            inl = np.linalg.norm(off - c, axis=1) < tol
            if best is None or inl.sum() > best.sum():
                best = inl
        if best.sum() >= min_inliers:
            kept.append((i, j, int(best.sum())))
            for p in pts[best]:
                I.append(i); J.append(j); A.append(p[:2]); B.append(p[2:])
    return np.array(I), np.array(J), np.array(A), np.array(B), kept


def check_connected(n, kept):
    adj = collections.defaultdict(set)
    for i, j, _ in kept:
        adj[i].add(j); adj[j].add(i)
    seen, stack = {0}, [0]
    while stack:
        for k in adj[stack.pop()] - seen:
            seen.add(k); stack.append(k)
    return sorted(set(range(n)) - seen)


def solve(n, I, J, A, B, anchor, w, h):
    c = np.array([w / 2, h / 2])
    A, B = A - c, B - c
    # Initial translation-only linear solve.
    rows, rhs = [], []
    for i, j, a, b in zip(I, J, A, B):
        r = np.zeros(n); r[j] = 1; r[i] = -1
        rows.append(r); rhs.append(a - b)
    r = np.zeros(n); r[anchor] = 1
    rows.append(r * 1e3); rhs.append([0, 0])
    t0 = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)[0]
    q0 = np.c_[t0, np.zeros(n), np.zeros(n)].ravel()

    def warp(q, idx, p):
        q = q.reshape(n, 4)
        s = np.exp(q[idx, 3]); co = np.cos(q[idx, 2]) * s; si = np.sin(q[idx, 2]) * s
        return np.stack([co * p[:, 0] - si * p[:, 1] + q[idx, 0],
                         si * p[:, 0] + co * p[:, 1] + q[idx, 1]], 1)

    keep = np.ones(len(I), bool)
    q = q0
    for _ in range(3):
        def f(q):
            res = (warp(q, I[keep], A[keep]) - warp(q, J[keep], B[keep])).ravel()
            return np.r_[res, (q.reshape(n, 4)[anchor] - q0.reshape(n, 4)[anchor]) * 1e4]
        q = least_squares(f, q, loss="soft_l1", f_scale=3).x
        err = np.linalg.norm(warp(q, I, A) - warp(q, J, B), axis=1)
        keep = err < 12
    e = err[keep]
    print(f"residual: median {np.median(e):.2f}px  rms {np.sqrt((e**2).mean()):.2f}px  "
          f"p95 {np.percentile(e, 95):.2f}px  ({keep.sum()} points)")

    q = q.reshape(n, 4)
    T = []
    for tx, ty, th, ls in q:
        s = np.exp(ls)
        M = np.array([[np.cos(th) * s, -np.sin(th) * s, tx], [np.sin(th) * s, np.cos(th) * s, ty]])
        M[:, 2] -= M[:, :2] @ c
        T.append(M)
    T = np.array(T)
    corners = np.array([[0, 0, 1], [w, 0, 1], [0, h, 1], [w, h, 1]])
    allc = np.concatenate([corners @ M.T for M in T])
    T[:, :, 2] -= allc.min(0)
    size = tuple((allc.max(0) - allc.min(0)).astype(int) + 2)
    return T, size


def render(files, T, size, out, work, trim):
    names = []
    kernel = np.ones((trim, trim), np.uint8) if trim > 1 else None
    for k, (f, M) in enumerate(zip(files, T)):
        im = cv2.imread(f)
        a = np.full(im.shape[:2], 255, np.uint8)
        if kernel is not None:
            a = cv2.erode(a, kernel)
        wi = cv2.warpAffine(im, M, size, flags=cv2.INTER_LANCZOS4)
        wa = cv2.warpAffine(a, M, size, flags=cv2.INTER_NEAREST)
        n = os.path.join(work, f"t{k:03d}.tif")
        cv2.imwrite(n, np.dstack([wi, wa]))
        names.append(n)
    run(["enblend", "--compression=LZW", "-o", out] + names)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input_dir")
    ap.add_argument("output")
    ap.add_argument("--anchor", type=int, default=None, help="tile index held fixed (default: best-connected)")
    ap.add_argument("--min-inliers", type=int, default=8, help="min consistent points to trust a tile pair")
    ap.add_argument("--trim", type=int, default=25, help="pixels eroded off tile edges before blending")
    args = ap.parse_args()

    files = sorted({f for e in EXTS for f in glob.glob(os.path.join(args.input_dir, e))})
    if len(files) < 2:
        sys.exit("need at least two images")
    h, w = cv2.imread(files[0]).shape[:2]
    print(f"{len(files)} tiles, {w}x{h}")

    with tempfile.TemporaryDirectory() as work:
        pairs = find_control_points(files, work)
        I, J, A, B, kept = filter_pairs(pairs, args.min_inliers)
        missing = check_connected(len(files), kept)
        if missing:
            sys.exit("not connected to the rest: " + ", ".join(os.path.basename(files[m]) for m in missing)
                     + "\nTry --min-inliers lower, or shoot more overlap.")
        deg = collections.Counter()
        for i, j, c in kept:
            deg[i] += c; deg[j] += c
        anchor = args.anchor if args.anchor is not None else deg.most_common(1)[0][0]
        T, size = solve(len(files), I, J, A, B, anchor, w, h)
        render(files, T, size, args.output, work, args.trim)
    print(f"wrote {args.output} ({size[0]}x{size[1]})")


if __name__ == "__main__":
    main()
