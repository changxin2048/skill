#!/usr/bin/env python3
"""Render an SVG to a PNG preview image.

Usage:
    python3 render_preview.py <input.svg> [output.png] [--width 1100]

Behavior:
    1. Tries to import cairosvg directly. If available, renders immediately.
    2. If missing, creates a throwaway virtualenv next to the input file
       (named .svgcheck-venv) and installs cairosvg into it. This avoids
       writing to the global/user site-packages, which may be blocked by
       the environment's file sandbox (PEP 668 / read-only user site).

Notes:
    - The preview uses fallback fonts (cairosvg does not fetch web fonts),
      so the PNG may differ slightly from the SVG opened in a browser.
    - Prints the output path on success; exits non-zero on failure.
"""
import argparse
import os
import subprocess
import sys

RENDER_CODE = (
    "import cairosvg, os\n"
    "cairosvg.svg2png(url=os.environ['SVG'], write_to=os.environ['PNG'], "
    "output_width=int(os.environ['W']))\n"
    "print('OK:', os.environ['PNG'])\n"
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("svg", help="input .svg file")
    ap.add_argument("png", nargs="?", default=None, help="output .png (default: <svg name>_预览.png)")
    ap.add_argument("--width", type=int, default=1100, help="output width in px")
    args = ap.parse_args()

    if not os.path.exists(args.svg):
        print(f"error: input not found: {args.svg}", file=sys.stderr)
        return 1

    png = args.png or (os.path.splitext(args.svg)[0] + "_预览.png")
    env = dict(os.environ, SVG=os.path.abspath(args.svg), PNG=os.path.abspath(png), W=str(args.width))

    # Fast path: cairosvg already installed
    try:
        import cairosvg  # noqa: F401
        subprocess.run([sys.executable, "-c", RENDER_CODE], env=env, check=True)
        return 0
    except ImportError:
        pass

    # Slow path: provision a venv next to the input file
    venv_dir = os.path.join(os.path.dirname(os.path.abspath(args.svg)), ".svgcheck-venv")
    py = os.path.join(venv_dir, "bin", "python")
    if not os.path.exists(py):
        print("cairosvg not found; provisioning venv (one-time)...", file=sys.stderr)
        try:
            subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
            subprocess.run([py, "-m", "pip", "install", "--quiet", "cairosvg"], check=True)
        except (subprocess.CalledProcessError, OSError) as e:
            print(f"error: could not provision cairosvg: {e}", file=sys.stderr)
            print("tip: install cairosvg manually, or just deliver the SVG.", file=sys.stderr)
            return 1

    try:
        subprocess.run([py, "-c", RENDER_CODE], env=env, check=True)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"error: rendering failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
