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
}

# get the image size - width and hiehgt 
def get_size(p):
    with Image.open(p) as im:
        return im.size

# function to build COCO-format JSON annotatio file
def build_coco(folder, out, label):
    # gets absolute path
    folder = Path(folder).resolve()
    # stores images and annotations
    images, annotations = [], []
    # incremental id for image and annotation, category ID on chosen label
    img_id = 1
    ann_id = 1
    cat_id = CATEGORY_IDS[label]

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
        # bounding box that covers the entire image for classification
        annotations.append({
            "id": ann_id,
            "image_id": img_id,
            "category_id": cat_id,
            "iscrowd": 0,
            "bbox": [0, 0, w, h],
            "area": float(w*h)
        })

        # increment
        img_id += 1
        ann_id += 1

    # final COCO build
    coco = {
        "info": {"description": f"All images labeled '{label}'","version": "1.0", "year": 2025},
        "licenses": [],
        "categories": [{"id": CATEGORY_IDS["monopole"], "name": "monopole", "supercategory": ""},
                       {"id": CATEGORY_IDS["lattice-s"], "name": "lattice-s", "supercategory": ""},
                       {"id": CATEGORY_IDS["lattice-g"], "name": "lattice-g", "supercategory": ""}],
        "images": images,
        "annotations": annotations
    }

    # output folder if needed to save JSON file
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(coco, f, indent=2)
    # confirm for debug
    print(f"Wrote {out} with {len(images)} images.")

if __name__ == "__main__":
    # cli arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", help="Folder containing images (will recurse)")
    ap.add_argument("--label", choices=list(CATEGORY_IDS.keys()),
                    help="Label to apply to all images in the folder")
    ap.add_argument("--out", default="annotations/coco_annotations.json")
    args = ap.parse_args()
    
    # if no label ask user
    if not args.label:
        print("Choose a label:")
        for i, k in enumerate(CATEGORY_IDS.keys(), start=1):
            print(f"  {i}) {k}")
        choice = input("Enter 1/2/3: ").strip()
        try:
            args.label = list(CATEGORY_IDS.keys())[int(choice)-1]
        except Exception:
            raise SystemExit("Invalid choice. Please rerun and select a valid label.")

    build_coco(args.folder, args.out, args.label)

