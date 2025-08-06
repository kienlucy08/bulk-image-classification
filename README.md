# Bulk Image Classification to COCO

## Purpose
This utility tool allows users to **bulk classify folders of images** into categories like `monopole`, `lattice-s`, and `lattice-g`, then automatically generates a **COCO-sytle annotations file** that can be uploaded directly into **Roboflow** for classification training.

---

## What it Does
- Takes in multiple folders of images
- Each folder is labeled by the user with a tower type
- Outputs a single `classification_annotations.json` file in **COCO Format** that maps each image to its category.
- Supports `.jpg`, `.jpeg`, `.png` image formats

---

## How to Use
1. Install all requirenments
```bash
pip install pillow
```
2. Run the script!
3. Follow the prompts
    You will be asked to:
    - Enter one or more folder paths containing images
    - Assign a label (`monopole`, `lattice-s`, `lattice-g`) to each folder
    Type `done` when done adding folders
### Example Prompt Flow
```typescript
Enter image folder path (or type 'done'): /Users/lucy/images/monopole
Enter label for this folder (monopole, lattice-s, lattice-g): monopole
Added /Users/lucy/images/monopole as 'monopole'

Enter image folder path (or type 'done'): /Users/lucy/images/lattice
Enter label for this folder (monopole, lattice-s, lattice-g): lattice-s
Added /Users/lucy/images/lattice as 'lattice-s'

Enter image folder path (or type 'done'): done
```
4. Output
A file named `classification_annotations.json` will be created in the current directory, containing the images and annotations in the following format:

```json
{
  "images": [
    {
      "id": 1,
      "file_name": "image001.jpg",
      "width": 640,
      "height": 480
    }
  ],
  "annotations": [
    {
      "id": 1,
      "image_id": 1,
      "category_id": 0
    }
  ],
  "categories": [
    {
      "id": 0,
      "name": "monopole"
    }
  ]
}
```

---

## Accepted Labels
The following labels are supported and mapped to COCO category IDs
| Label     | COCO Category ID |
| --------- | ---------------- |
| monopole  | 0                |
| lattice-s | 1                |
| lattice-g | 2                |

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