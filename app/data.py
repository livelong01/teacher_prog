from pathlib import Path
import json
import os
import shutil
import sys
from PIL import Image


def _app_dir() -> Path:
    """Return a writable application data directory.

    - When running from source, this is the project root (two levels up).
    - When frozen (PyInstaller), return the folder containing the executable
      so that data files are stored next to the .exe (persistent).
    """
    if getattr(sys, "frozen", False):
        # Running in a bundle: use a per-user writable folder (LOCALAPPDATA)
        local = os.getenv("LOCALAPPDATA") or os.getenv("APPDATA")
        if local:
            return Path(local) / "MeetsDosAlunos"
        # fallback to executable folder if no appdata found
        return Path(sys.executable).resolve().parent
    # Running in normal (source) mode: project root
    return Path(__file__).resolve().parent.parent


PROJECT_ROOT = _app_dir()

# Paths for data files (alunos.json) and photos directory
ARQUIVO = str(PROJECT_ROOT / "alunos.json")
PASTA_FOTOS = str(PROJECT_ROOT / "fotos")
FOTO_PADRAO = str(Path(PASTA_FOTOS) / "padrao.png")


def ensure_photos_dir():
    os.makedirs(PASTA_FOTOS, exist_ok=True)


def _ensure_resources_copied():
    """When running from a bundle, copy bundled resource files (fotos, alunos.json)
    into the user data directory so they are writable and persistent.
    """
    # Determine where the original resources live inside the bundle or source tree
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        resource_root = Path(sys._MEIPASS)
    else:
        resource_root = Path(__file__).resolve().parent.parent

    # Copy fotos if target folder is empty
    try:
        os.makedirs(PASTA_FOTOS, exist_ok=True)
        # if target fotos folder is empty, copy bundled ones
        if not any(Path(PASTA_FOTOS).iterdir()):
            src_photos = resource_root / "fotos"
            if src_photos.exists():
                for item in src_photos.iterdir():
                    if item.is_file():
                        shutil.copy(item, Path(PASTA_FOTOS) / item.name)

        # If alunos.json doesn't exist in data dir but exists in resources, copy it
        target_json = Path(ARQUIVO)
        src_json = resource_root / "alunos.json"
        if not target_json.exists() and src_json.exists():
            shutil.copy(src_json, target_json)
    except Exception:
        # Best-effort copy; ignore failures so app still runs
        pass


ensure_photos_dir()
_ensure_resources_copied()

def carregar_alunos():
    if not os.path.exists(ARQUIVO):
        return []
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def salvar_alunos(alunos):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(alunos, f, ensure_ascii=False, indent=2)

def copy_photo(src_path, dest_name):
    """Copy and optimize image to the photos folder.

    Strategy:
    - Save images as JPEG to reduce size (flatten alpha if present).
    - Resize to a max dimension (e.g. 800x800) keeping aspect ratio.
    - Use quality/compression settings to keep files small.
    """
    # Ensure destination filename has .jpg extension for efficient compression
    base, _ = os.path.splitext(dest_name)
    dest_name_jpg = f"{base}.jpg"
    dest = os.path.join(PASTA_FOTOS, dest_name_jpg)

    try:
        with Image.open(src_path) as im:
            # Convert RGBA/LA to RGB (flatten transparency on white)
            if im.mode in ("RGBA", "LA"):
                bg = Image.new("RGB", im.size, (255, 255, 255))
                bg.paste(im, mask=im.split()[-1])
                im = bg
            else:
                im = im.convert("RGB")

            # Resize keeping aspect ratio
            max_size = (800, 800)
            im.thumbnail(max_size, Image.LANCZOS)

            # Save as optimized JPEG
            im.save(dest, format="JPEG", quality=75, optimize=True)
            return dest
    except Exception:
        # Fallback: copy raw file if image processing fails
        try:
            shutil.copy(src_path, dest)
            return dest
        except Exception:
            # Last resort: return original path
            return src_path
