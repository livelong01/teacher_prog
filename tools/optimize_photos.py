"""Batch optimize existing photos in the `fotos/` folder.

This script will replace images in `fotos/` with optimized JPEGs (max 800x800, quality=75).
Run from project root with the venv Python.

Example:
  & E:/prog_prof/venv/Scripts/python.exe tools/optimize_photos.py
"""
import os
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PHOTOS_DIR = ROOT / "fotos"

def optimize_image(path: Path):
    try:
        with Image.open(path) as im:
            if im.mode in ("RGBA", "LA"):
                bg = Image.new("RGB", im.size, (255,255,255))
                bg.paste(im, mask=im.split()[-1])
                im = bg
            else:
                im = im.convert("RGB")
            im.thumbnail((50,55), Image.LANCZOS)
            dest = path.with_suffix('.jpg')
            im.save(dest, format='JPEG', quality=75, optimize=True)
            if dest != path:
                try:
                    os.remove(path)
                except Exception:
                    pass
            print(f"Optimized: {dest}")
    except Exception as e:
        print(f"Skip {path}: {e}")

def main():
    if not PHOTOS_DIR.exists():
        print("No fotos directory found")
        return
    for p in PHOTOS_DIR.iterdir():
        if p.is_file():
            optimize_image(p)

if __name__ == '__main__':
    main()
