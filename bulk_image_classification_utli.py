# build_coco_from_site.py
# Create COCO multi-label annotations from a site folder with section subfolders.
# Layout expected:
#   site_root/
#     top/            -> section = top
#     bottom/         -> section = bottom
#     unclassified/   -> section = unclassified

import json, argparse, re
from pathlib import Path
from PIL import Image

# Supported file types
IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}

# Flat category space (multi-label)
CATEGORY_IDS = {
    # tower types
    "monopole": 1,
    "lattice-s": 2,
    "lattice-g": 3,
    # sections
    "top": 4,
    "bottom": 5,
    "unclassified": 6,
}
TOWER_CHOICES = ["monopole", "lattice-s", "lattice-g"]
SECTION_CHOICES = ["top", "bottom", "unclassified"]

# Optional synonyms to infer tower type from folder name
TOWER_SYNONYMS = {
    "monopole": "monopole",
    "mono": "monopole",
    "self-support": "lattice-s",
    "selfsupport": "lattice-s",
    "lattice-s": "lattice-s",
    "lattices": "lattice-s",
    "guyed": "lattice-g",
    "guyedtower": "lattice-g",
    "lattice-g": "lattice-g",
    "latticeg": "lattice-g",
    "guy": "lattice-g",
}

def get_size(p: Path):
    with Image.open(p) as im:
        return im.size  # (w, h)

def infer_tower_from_name(name: str) -> str | None:
    n = name.lower()
    for k, v in TOWER_SYNONYMS.items():
        if re.search(rf"\b{k}\b", n) or k in n:
            return v
    return None

def find_section_from_path(root: Path, file_path: Path) -> str | None:
    # first path segment under root that matches a known section
    rel_parts = file_path.resolve().relative_to(root.resolve()).parts
    for part in rel_parts:
        p = part.lower()
        if p in SECTION_CHOICES:
            return p
    return None

def build_coco(site_root: str, out: str, tower_label: str | None = None):
    root = Path(site_root.strip().strip('"')).resolve()
    if not root.exists():
        raise SystemExit(f"Root folder not found: {root}")

    # Decide tower label
    tower = tower_label or infer_tower_from_name(root.name)
    if tower not in TOWER_CHOICES:
        print("\nCould not infer tower type from folder name.")
        print("Choose a tower label:")
        for i, k in enumerate(TOWER_CHOICES, start=1):
            print(f"  {i}) {k}")
        try:
            tower = TOWER_CHOICES[int(input("Enter 1/2/3: ").strip()) - 1]
        except Exception:
            raise SystemExit("Invalid choice for tower label.")
    tower_cid = CATEGORY_IDS[tower]

    images, annotations = [], []
    img_id = 1
    ann_id = 1

    files = sorted([p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in IMG_EXTS])
    if not files:
        raise SystemExit(f"No images found under {root}")

    counts = {"top": 0, "bottom": 0, "unclassified": 0}
    for p in files:
        section = find_section_from_path(root, p)
        if section not in SECTION_CHOICES:
            # ignore files that aren't inside top/bottom/unclassified
            continue

        w, h = get_size(p)
        rel = p.relative_to(root).as_posix()

        images.append({"id": img_id, "file_name": rel, "width": w, "height": h})

        # Annotation 1: tower type (full image)
        annotations.append({
            "id": ann_id,
            "image_id": img_id,
            "category_id": tower_cid,
            "iscrowd": 0,
            "bbox": [0, 0, w, h],
            "area": float(w * h),
        })
        ann_id += 1

        # Annotation 2: section (full image)
        section_cid = CATEGORY_IDS[section]
        annotations.append({
            "id": ann_id,
            "image_id": img_id,
            "category_id": section_cid,
            "iscrowd": 0,
            "bbox": [0, 0, w, h],
            "area": float(w * h),
        })
        ann_id += 1
        img_id += 1
        counts[section] += 1

    if not images:
        raise SystemExit("No images found under recognized section folders (top/bottom/unclassified).")

    categories = [
        {"id": CATEGORY_IDS["monopole"], "name": "monopole", "supercategory": "tower"},
        {"id": CATEGORY_IDS["lattice-s"], "name": "lattice-s", "supercategory": "tower"},
        {"id": CATEGORY_IDS["lattice-g"], "name": "lattice-g", "supercategory": "tower"},
        {"id": CATEGORY_IDS["top"], "name": "top", "supercategory": "section"},
        {"id": CATEGORY_IDS["bottom"], "name": "bottom", "supercategory": "section"},
        {"id": CATEGORY_IDS["unclassified"], "name": "unclassified", "supercategory": "section"},
    ]

    coco = {
        "info": {"description": f"Site '{root.name}' labeled tower={tower}, section from subfolders",
                 "version": "1.0", "year": 2025},
        "licenses": [],
        "categories": categories,
        "images": images,
        "annotations": annotations,
    }

    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(coco, indent=2), encoding="utf-8")

    print(f"\n✅ Wrote {out_path} with {len(images)} images from {root}")
    print(f"   Tower label: {tower}")
    print(f"   Sections -> top: {counts['top']}, bottom: {counts['bottom']}, unclassified: {counts['unclassified']}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build COCO from site root with top/bottom/unclassified subfolders.")
    ap.add_argument("site_root", nargs="?", help="Path to site root (e.g., C:/data/guyedtower1)")
    ap.add_argument("--tower", choices=TOWER_CHOICES, help="Tower type (overrides inference).")
    ap.add_argument("--out", default="data/coco_annotations.json", help="Output JSON path.")
    args = ap.parse_args()

    root = args.site_root or input("\nEnter path to site root (e.g., C:\\data\\guyedtower1): ").strip()
    build_coco(root, args.out, args.tower)


