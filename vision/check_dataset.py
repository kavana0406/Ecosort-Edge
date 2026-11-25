from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset"

for split in ["train", "val"]:
    split_dir = DATASET_DIR / split

    print(f"\n{split.upper()} DATASET")

    total = 0

    for folder in sorted(split_dir.iterdir()):
        if folder.is_dir():
            images = [
                f for f in folder.iterdir()
                if f.suffix.lower() in [".jpg", ".jpeg", ".png"]
            ]

            print(f"{folder.name}: {len(images)} images")
            total += len(images)

    print("Total images:", total)