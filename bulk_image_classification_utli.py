import os
import json
from PIL import Image

# Map folder names to COCO category ids
CATEGORY_MAP = {
    "monopole": 0,
    "lattice-s": 1,
    "lattice-g": 2
}

def get_image_size(image_path):
    try:
        with Image.open(image_path) as img:
            return img.size  # width, height
    except Exception as e:
        print(f"Could not open {image_path}: {e}")
        return 0, 0

def prompt_for_folders():
    folder_to_label_map = {}

    print("Enter folders to process. Type 'done' when finished.\n")
    while True:
        folder = input("Enter image folder path (or type 'done'): ").strip()
        if folder.lower() == 'done':
            break
        if not os.path.isdir(folder):
            print("That folder does not exist. Try again.")
            continue

        label = input("Enter label for this folder (monopole, lattice-s, lattice-g): ").strip().lower()
        if label not in CATEGORY_MAP:
            print("Invalid label. Must be one of: monopole, lattice-s, lattice-g.")
            continue

        folder_to_label_map[folder] = label
        print(f"Added {folder} as '{label}'\n")

    return folder_to_label_map

def generate_coco_classification(folder_to_label_map, output_file="classification_annotations.json"):
    images = []
    annotations = []
    categories = [{"id": v, "name": k} for k, v in CATEGORY_MAP.items()]
    
    annotation_id = 1
    image_id = 1

    for folder, label in folder_to_label_map.items():
        category_id = CATEGORY_MAP[label]
        for fname in os.listdir(folder):
            if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            
            img_path = os.path.join(folder, fname)
            width, height = get_image_size(img_path)

            images.append({
                "id": image_id,
                "file_name": fname,
                "width": width,
                "height": height
            })

            annotations.append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_id
            })

            annotation_id += 1
            image_id += 1

    coco_dict = {
        "images": images,
        "annotations": annotations,
        "categories": categories
    }

    with open(output_file, 'w') as f:
        json.dump(coco_dict, f, indent=2)

    print(f"\nDone! COCO-style classification file saved to: {output_file}")

if __name__ == "__main__":
    folder_label_map = prompt_for_folders()
    if folder_label_map:
        generate_coco_classification(folder_label_map)
    else:
        print("No folders were provided. Exiting.")
