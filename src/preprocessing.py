"""
Week 1: Receipt image preprocessing pipeline.

Goal: take a raw phone/scan photo of a receipt and produce a clean,
OCR-ready image. Three steps, each fixing a specific real-world problem:

1. Deskew   -> receipt was photographed at an angle, text isn't horizontal
2. Denoise  -> phone camera noise / JPEG artifacts blur character edges
3. Contrast -> uneven lighting/shadows make text hard to separate from background

Run:
    python preprocessing.py --input data/raw --output data/processed
"""

import cv2
import numpy as np
import argparse
from pathlib import Path


def deskew(image: np.ndarray) -> np.ndarray:
    """
    Detect the dominant text angle and rotate the image to straighten it.

    How: threshold the image to get foreground pixels (text/edges), find
    the minimum-area rectangle that bounds all of them, and use its angle
    to rotate the image back to horizontal.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Invert so text (usually dark) becomes the "foreground" (white) for thresholding
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    coords = np.column_stack(np.where(thresh > 0))
    if len(coords) < 10:
        return image  # not enough signal to estimate an angle safely

    angle = cv2.minAreaRect(coords)[-1]
    # cv2.minAreaRect returns angle in [-90, 0); normalize to a small rotation
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # Skip rotation if it's negligible (avoid introducing artifacts on already-straight images)
    if abs(angle) < 0.5:
        return image

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )
    return rotated


def denoise(image: np.ndarray) -> np.ndarray:
    """
    Remove camera/JPEG noise while preserving text edges.
    fastNlMeansDenoisingColored is slower than a simple blur but preserves
    edges much better -- important since OCR depends on sharp character edges.
    """
    return cv2.fastNlMeansDenoisingColored(image, None, h=10, hColor=10,
                                            templateWindowSize=7, searchWindowSize=21)


def enhance_contrast(image: np.ndarray) -> np.ndarray:
    """
    Even out lighting (shadows, glare) using CLAHE (Contrast Limited Adaptive
    Histogram Equalization) on the luminance channel only, so colors aren't
    distorted. This helps a lot with phone photos taken in uneven light.
    """
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    merged = cv2.merge((l, a, b))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


def binarize_for_ocr(image: np.ndarray) -> np.ndarray:
    """
    Final step: adaptive thresholding to produce a clean black-text-on-white
    image. Adaptive (not global) thresholding matters because receipts often
    have uneven lighting across the page.
    NOTE: this is the version you'll feed to Tesseract/EasyOCR in Week 2.
    Keep the non-binarized version too -- some OCR engines do better on
    grayscale/color input.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 15
    )


def preprocess_image(image_path: Path) -> dict:
    """Run the full pipeline on one image. Returns intermediate + final results
    so you can inspect where things go wrong."""
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    deskewed = deskew(image)
    denoised = denoise(deskewed)
    contrast_enhanced = enhance_contrast(denoised)
    binarized = binarize_for_ocr(contrast_enhanced)

    return {
        "original": image,
        "deskewed": deskewed,
        "denoised": denoised,
        "contrast_enhanced": contrast_enhanced,
        "binarized": binarized,  # this is what Week 2 OCR will consume
    }


def process_directory(input_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    extensions = {".jpg", ".jpeg", ".png"}
    image_paths = [p for p in input_dir.rglob("*") if p.suffix.lower() in extensions]

    if not image_paths:
        print(f"No images found in {input_dir}")
        return

    print(f"Processing {len(image_paths)} images...")
    failures = []
    for path in image_paths:
        try:
            results = preprocess_image(path)
            out_path = output_dir / f"{path.stem}_processed.png"
            cv2.imwrite(str(out_path), results["binarized"])
            # Also save the contrast-enhanced (non-binary) version -- try both in Week 2
            out_path_gray = output_dir / f"{path.stem}_enhanced.png"
            cv2.imwrite(str(out_path_gray), results["contrast_enhanced"])
        except Exception as e:
            failures.append((path.name, str(e)))

    print(f"Done. {len(image_paths) - len(failures)} succeeded, {len(failures)} failed.")
    if failures:
        print("Failures:")
        for name, err in failures:
            print(f"  {name}: {err}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess receipt images for OCR")
    parser.add_argument("--input", type=str, default="data/raw", help="Input directory")
    parser.add_argument("--output", type=str, default="data/processed", help="Output directory")
    args = parser.parse_args()

    process_directory(Path(args.input), Path(args.output))
