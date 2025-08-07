import os
import json
from PIL import Image

# Map folder names to label classes
VALID_CLASSES = ["monopole", "lattice-s", "lattice-g"]

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
        if label not in VALID_CLASSES:
            print("Invalid label. Must be one of:", ", ".join(VALID_CLASSES))
            continue

        folder_to_label_map[folder] = label
        print(f"Added {folder} as '{label}'\n")

    return folder_to_label_map

def generate_roboflow_classification_json(folder_to_label_map, output_file="roboflow_classification.json"):
    classification_data = []

    for folder, label in folder_to_label_map.items():
        for fname in os.listdir(folder):
            if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue

            classification_data.append({
                "image": fname,
                "class": label
            })

    with open(output_file, 'w') as f:
        json.dump(classification_data, f, indent=2)

    print(f"\nRoboflow-style classification file saved to: {output_file}")

if __name__ == "__main__":
    folder_label_map = prompt_for_folders()
    if folder_label_map:
        generate_roboflow_classification_json(folder_label_map)
    else:
        print("No folders were provided. Exiting.")

