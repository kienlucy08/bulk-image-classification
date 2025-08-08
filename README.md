# Bulk Image Classification to COCO

## Purpose
This utility tool allows users to **bulk classify folders of images** into categories like `monopole`, `lattice-s`, and `lattice-g`, then automatically generates a **COCO-sytle annotations file** that can be uploaded directly into **Roboflow** for classification training.

---

## What it Does
- Processes all images in a single folder (using recursion)
- Lets you choose on elabel for the entire folder via:
  - `--label` argument (non-interactive)
  - Interactive prompt (if no `--label` provided)
- Outputs a single `coco_annotations.json` file in **COCO Format** that maps each image to its category.
- Supports `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tif`, `.tiff`, `.webp` image formats
- Automatically records image dimentions and assigns a  **full-image bounding box** (required by many COCO readers)

---

## How to Use
1. Install all requirenments
```bash
pip install pillow
```
2. Run the script!
Option A - Specify label directly (non-interactive)
```bash
python bulk_image_classification_utli.py /path/to/images --label monopole --out /path/to/images/coco_annotations.json
```
Option B - Let the script prompt you
```bash
python bulk_image_classification_utli.py 
```
Example Prompt:
```css
Enter the path to your folder of images: path/to/images

Choose a label:
  1) monopole
  2) lattice-s
  3) lattice-g
Enter 1/2/3: 1
Wrote path\to\images\coco_annotations.json with X images
```
3. Output
A file named `coco_annotations.json` will be created in the current directory, containing the images and annotations in the following format:

```json
{
  "info": {
    "description": "All images labeled 'monopole'",
    "version": "1.0",
    "year": 2025
  },
  "licenses": [],
  "categories": [
    { "id": 1, "name": "monopole", "supercategory": "" },
    { "id": 2, "name": "lattice-s", "supercategory": "" },
    { "id": 3, "name": "lattice-g", "supercategory": "" }
  ],
  "images": [
    { "id": 1, "file_name": "tower1.jpg", "width": 640, "height": 480 }
  ],
  "annotations": [
    {
      "id": 1,
      "image_id": 1,
      "category_id": 1,
      "iscrowd": 0,
      "bbox": [0, 0, 640, 480],
      "area": 307200
    }
  ]
}
```

---

## Accepted Labels
The following labels are supported and mapped to COCO category IDs
| Label     | COCO Category ID |
| --------- | ---------------- |
| monopole  | 1                |
| lattice-s | 2                |
| lattice-g | 3                |

---

## Upload to Roboflow
Once the JSON is generated:
1. Create a folder with the folder of images you have labeled that includes the JSON file.
2. Go to your Roboflow project.
3. Select 'Upload Dataset'.
4. Choose select folder and pick the folder with all information.
5. Wait for items to upload.
6. Briefly skim annotations to make sure everything is how it should be.

---