import os
import shutil

# ============================================================
# FOLDERS - edit this
# ============================================================

# The DATASET ROOT folder - the one that CONTAINS "images" and "labels"
# (do NOT point this at the "images" folder itself)
# Example: if your files are at
#   C:\...\uiis10k test0001 to test1500 final\images\train
#   C:\...\uiis10k test0001 to test1500 final\labels\train
# then DATASET_ROOT should be:
#   C:\...\uiis10k test0001 to test1500 final
DATASET_ROOT = r"REPLACE WITH YOUR ACTUAL PATH TO THE DATASET ROOT FOLDER"  # <-- EDIT THIS

IMAGES_FOLDER = os.path.join(DATASET_ROOT, "images", "train")
LABELS_FOLDER = os.path.join(DATASET_ROOT, "labels", "train")

# Unlabelled images get moved here (created automatically, inside images/)
UNLABELLED_FOLDER = os.path.join(DATASET_ROOT, "images", "unlabelled")

# ============================================================

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def main():

    print("Looking for images in:")
    print(IMAGES_FOLDER)
    print("Looking for labels in:")
    print(LABELS_FOLDER)
    print()

    if not os.path.exists(IMAGES_FOLDER):
        print("ERROR: Images folder not found:")
        print(IMAGES_FOLDER)
        return

    if not os.path.exists(LABELS_FOLDER):
        print("ERROR: Labels folder not found:")
        print(LABELS_FOLDER)
        return

    os.makedirs(UNLABELLED_FOLDER, exist_ok=True)

    # Get all images in images/train
    images = []

    for file in os.listdir(IMAGES_FOLDER):
        extension = os.path.splitext(file)[1].lower()

        if extension in IMAGE_EXTENSIONS:
            images.append(file)

    total_images = len(images)
    moved = 0
    labelled = 0

    print(f"Found {total_images} images.")
    print("Checking for missing annotations...\n")

    for image_name in images:

        # Get filename without extension
        image_stem = os.path.splitext(image_name)[0]

        # Corresponding YOLO annotation
        label_name = image_stem + ".txt"
        label_path = os.path.join(LABELS_FOLDER, label_name)

        image_path = os.path.join(IMAGES_FOLDER, image_name)

        # Check labels/train first: is there a .txt file for this image?
        is_unlabelled = not os.path.exists(label_path)

        if is_unlabelled:
            shutil.move(image_path, os.path.join(UNLABELLED_FOLDER, image_name))
            moved += 1
            print(f"MOVED (unlabelled): {image_name}")
        else:
            labelled += 1

    print("\n===================================")
    print("Finished!")
    print("===================================")
    print(f"Total images checked: {total_images}")
    print(f"Labelled (left in place): {labelled}")
    print(f"Unlabelled (moved):        {moved}")
    print()
    print("Unlabelled images moved to:")
    print(UNLABELLED_FOLDER)


if __name__ == "__main__":
    main()