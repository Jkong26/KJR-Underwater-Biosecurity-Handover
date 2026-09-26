import os
import shutil
import random
import time

# ============================================================
# FOLDERS — point this at your existing train folders
# ============================================================

IMAGES_TRAIN_FOLDER = r"REPLACE WITH YOUR ACTUAL PATH TO IMAGES/TRAIN" 
LABELS_TRAIN_FOLDER = r"REPLACE WITH YOUR ACTUAL PATH TO LABELS/TRAIN"

# ============================================================
# SPLIT SETTINGS
# ============================================================

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15  # should sum to 1.0 with the two above

RANDOM_SEED = 42  # fixed seed so the split is reproducible

# ============================================================

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 1.5


def move_with_retry(src, dst):
    """Move a file, retrying a few times if it's transiently locked"""
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            shutil.move(src, dst)
            return True, None
        except PermissionError as e:
            last_error = e
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY_SECONDS)
    return False, last_error


def main():

    if not os.path.exists(IMAGES_TRAIN_FOLDER):
        print("ERROR: Images train folder not found:")
        print(IMAGES_TRAIN_FOLDER)
        return

    if not os.path.exists(LABELS_TRAIN_FOLDER):
        print("ERROR: Labels train folder not found:")
        print(LABELS_TRAIN_FOLDER)
        return

    ratio_sum = round(TRAIN_RATIO + VAL_RATIO + TEST_RATIO, 5)
    if ratio_sum != 1.0:
        print(f"ERROR: Split ratios must sum to 1.0 (currently {ratio_sum})")
        return

    # images/ and labels/ are the parent folders of the "train" subfolders
    images_root = os.path.dirname(IMAGES_TRAIN_FOLDER)
    labels_root = os.path.dirname(LABELS_TRAIN_FOLDER)

    images_val_dir = os.path.join(images_root, "val")
    images_test_dir = os.path.join(images_root, "test")
    labels_val_dir = os.path.join(labels_root, "val")
    labels_test_dir = os.path.join(labels_root, "test")

    for d in (images_val_dir, images_test_dir, labels_val_dir, labels_test_dir):
        if os.path.exists(d) and os.listdir(d):
            print(f"WARNING: '{d}' already exists and is not empty.")
            print("This script will add to it, which may cause a skewed split if run twice.")
            print("Consider clearing val/test folders first if you want a clean re-split.\n")
        os.makedirs(d, exist_ok=True)

    # --- Gather all images in train that have a matching label file ---
    images = []
    for file in os.listdir(IMAGES_TRAIN_FOLDER):
        extension = os.path.splitext(file)[1].lower()
        if extension in IMAGE_EXTENSIONS:
            images.append(file)

    paired = []
    missing_labels = []

    for image_name in images:
        image_stem = os.path.splitext(image_name)[0]
        label_name = image_stem + ".txt"
        label_path = os.path.join(LABELS_TRAIN_FOLDER, label_name)

        if os.path.exists(label_path):
            paired.append((image_name, label_name))
        else:
            missing_labels.append(image_name)

    print(f"Found {len(images)} images in train folder.")
    print(f"  -> {len(paired)} have a matching label file (eligible for split).")
    print(f"  -> {len(missing_labels)} are missing a label file (left untouched in train).\n")

    # --- Shuffle deterministically, then decide who moves to val/test ---
    random.seed(RANDOM_SEED)
    random.shuffle(paired)

    total = len(paired)
    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)

    # Everything from train_end onwards MOVES out of train
    to_val = paired[train_end:val_end]
    to_test = paired[val_end:]
    stays_in_train = paired[:train_end]

    failed = []

    def move_batch(pairs, img_dest, lbl_dest, label):
        print(f"Moving {len(pairs)} pairs to '{label}'...")
        for image_name, label_name in pairs:
            img_ok, img_err = move_with_retry(
                os.path.join(IMAGES_TRAIN_FOLDER, image_name),
                os.path.join(img_dest, image_name),
            )
            if not img_ok:
                print(f"  FAILED (image): {image_name} — {img_err}")
                failed.append(image_name)
                continue

            lbl_ok, lbl_err = move_with_retry(
                os.path.join(LABELS_TRAIN_FOLDER, label_name),
                os.path.join(lbl_dest, label_name),
            )
            if not lbl_ok:
                print(f"  FAILED (label): {label_name} — {lbl_err}")
                failed.append(label_name)
                continue

    move_batch(to_val, images_val_dir, labels_val_dir, "val")
    move_batch(to_test, images_test_dir, labels_test_dir, "test")

    print("\n===================================")
    print("Finished!")
    print("===================================")
    print(f"Total eligible pairs: {total}")
    print(f"  Train (remaining in place): {len(stays_in_train)} ({TRAIN_RATIO*100:.0f}%)")
    print(f"  Val (moved):                {len(to_val)} ({VAL_RATIO*100:.0f}%)")
    print(f"  Test (moved):               {len(to_test)} ({TEST_RATIO*100:.0f}%)")
    print(f"Missing labels (left in train, excluded from split): {len(missing_labels)}")
    print(f"Failed moves (locked/permission): {len(failed)}")
    if failed:
        print("\nFailed files (re-run to retry, once unlocked):")
        for f in failed:
            print(" -", f)
    print()
    print("Result:")
    print(f"  {images_root}\\train, \\val, \\test")
    print(f"  {labels_root}\\train, \\val, \\test")


if __name__ == "__main__":
    main()
