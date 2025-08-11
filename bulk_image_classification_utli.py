# bulk image classificatio util for tower types
# use case: labeling an entire folder of images as 'monopole'
import os, json, argparse
from pathlib import Path
from PIL import Image

# supported file exstensions
IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}

# mapping of category names to COCO category IDs
CATEGORY_IDS = {
    "monopole": 1,
    "lattice-s": 2,
    "lattice-g": 3,
    # sections
    "top": 4,
    "bottom": 5,
    "unclassified": 6,
}

TOWER_CHOICES = ["monopole", "lattice-s", "lattice-g"]
SECTION_CHOICES = ["top", "bottom", "unclassifed"]

# get the image size - width and hiehgt 
def get_size(p):
    with Image.open(p) as im:
        return im.size

# function to build COCO-format JSON annotatio file
def build_coco(folder, out, tower_label, section_label):
    # gets absolute path
    folder = Path(folder).resolve()
    # stores images and annotations
    images, annotations = [], []
    # incremental id for image and annotation, category ID on chosen label
    img_id = 1
    ann_id = 1

    # Validate labels
    if tower_label not in TOWER_CHOICES:
        raise SystemExit(f"Invalid tower label: {tower_label}")
    if section_label not in SECTION_CHOICES:
        raise SystemExit(f"Invalid section label: {section_label}")

    tower_cid = CATEGORY_IDS[tower_label]
    section_cid = CATEGORY_IDS[section_label]

    # loop over all files in the folder and subfolders
    for p in sorted(folder.rglob("*")):
        # skip non-image files
        if p.suffix.lower() not in IMG_EXTS or not p.is_file():
            continue

        # get file path relative to dataset folder
        rel = p.relative_to(folder).as_posix()

        # get image width and height
        w, h = get_size(p)

        # add the entry images to COCO images
        images.append({
            "id": img_id, 
            "file_name": rel, 
            "width": w, 
            "height": h})

        # add entry to COCO annotations
        # bounding box that covers the entire image for classification of tower type
        annotations.append({
            "id": ann_id,
            "image_id": img_id,
            "category_id": tower_cid,
            "iscrowd": 0,
            "bbox": [0, 0, w, h],
            "area": float(w*h)
        })
        ann_id += 1

        # annotation number 2 for the tower section
        annotations.append({
            "id": ann_id,
            "image_id": img_id,
            "category_id": section_cid,
            "iscrowd": 0,
            "bbox": [0, 0, w, h],
            "area": float(w*h)
        })

        # increment annotation count and image id
        ann_id += 1
        img_id += 1

    # final COCO build
    coco = {
        "info": {"description": f"All images labeled with '{tower_label}' + '{section_label}'","version": "1.0", "year": 2025},
        "licenses": [],
        "categories": [{"id": CATEGORY_IDS["monopole"], "name": "monopole", "supercategory": "tower"},
                       {"id": CATEGORY_IDS["lattice-s"], "name": "lattice-s", "supercategory": "tower"},
                       {"id": CATEGORY_IDS["lattice-g"], "name": "lattice-g", "supercategory": "tower"},
                       {"id": CATEGORY_IDS["top"], "name": "top", "supercategory": "section"},
                       {"id": CATEGORY_IDS["bottom"], "name": "bottom", "supercategory": "section"},
                       {"id": CATEGORY_IDS["unclassified"], "name": "unclassified", "supercategory": "section"}],
        "images": images,
        "annotations": annotations
    }

    # output folder if needed to save JSON file
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(coco, f, indent=2)
    # confirm for debug
    print(f"\nWrote {out} with {len(images)} images. each image has labels: {tower_label}, {section_label}.")

if __name__ == "__main__":
    # cli arguments
    ap = argparse.ArgumentParser(description="Bulk classify images into COCO format with the tower type and section.")
    ap.add_argument("folder", nargs="?", help="Folder containing images (will recurse)")
    ap.add_argument("--tower", choices=TOWER_CHOICES, help="Tower label for all images.")
    ap.add_argument("--section", choices=SECTION_CHOICES, help="Section label for all images.")
    ap.add_argument("--out", default="data/coco_annotations.json")
    args = ap.parse_args()

    if not args.folder:
        folder = input("\nEnter the path to your folder of images: ").strip()
    else:
        folder = args.folder
    
    # if no label ask user
    if not args.tower:
        print("\nChoose a tower label:")
        for i, k in enumerate(TOWER_CHOICES, start=1):
            print(f"  {i}) {k}")
        try:
            tower_label = TOWER_CHOICES[int(input("\nEnter 1/2/3: ").strip()) - 1]
        except Exception:
            raise SystemExit("Invalid choice for tower label.")
    else:
        tower_label = args.tower

    if not args.section:
        print("\nChoose a section label:")
        for i, k in enumerate(SECTION_CHOICES, start=1):
            print(f"  {i}) {k}")
        try:
            section_label = SECTION_CHOICES[int(input("\nEnter 1/2/3: ").strip()) - 1]
        except Exception:
            raise SystemExit("Invalid choice for section label.")
    else:
        section_label = args.section

    out_path = args.out if args.out else "data/coco_annotations.json"


    build_coco(folder, out_path, tower_label, section_label)

