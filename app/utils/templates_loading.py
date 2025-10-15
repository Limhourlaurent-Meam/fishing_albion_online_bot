import cv2
from pathlib import Path

def loadTemplates(folder_path, scale=1):
    """
    Load all images in the given folder as grayscale templates.
    Returns list of (template, width, height, filename)
    """
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder.resolve()}")

    templates = []
    for file in folder.glob("*.*"):
        if file.suffix.lower() not in [".png", ".jpg", ".jpeg", ".bmp"]:
            continue

        template = cv2.imread(str(file), cv2.IMREAD_GRAYSCALE)
        if template is None:
            print(f"⚠️ Skipped unreadable file: {file.name}")
            continue

        # Resize
        if scale != 1:
            width = int(template.shape[1] * scale)
            height = int(template.shape[0] * scale)
            template = cv2.resize(template, (width, height), interpolation=cv2.INTER_AREA)

        w, h = template.shape[::-1]
        templates.append((template, w, h, file.name))

    print(f"✅ Loaded {len(templates)} templates from '{folder}'")
    return templates

# # Example
# if __name__ == "__main__":
#     templates = loadTemplates("./app/data/bobber", scale=0.8)
#     for tpl, w, h, name in templates:
#         print(f"{name}: {w}x{h}")
