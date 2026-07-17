"""
Downscale images by a specified factor.
AI generated.
"""


import cv2

from pathlib import Path
from tqdm import tqdm
from fire import Fire


IMAGE_EXTENSIONS = {
    ".bmp",
    ".dib",
    ".jpeg",
    ".jpg",
    ".jpe",
    ".jp2",
    ".png",
    ".pbm",
    ".pgm",
    ".ppm",
    ".pxm",
    ".pnm",
    ".sr",
    ".ras",
    ".tiff",
    ".tif",
    ".webp",
}


def _image_paths(input_folder: Path) -> list[Path]:
    return sorted(
        path
        for path in input_folder.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def _read_image_size(path: Path) -> tuple[int, int] | None:
    image = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if image is None:
        return None
    height, width = image.shape[:2]
    return width, height


def _output_size(width: int, height: int, scale_factor: float) -> tuple[int, int]:
    return (
        max(1, int(round(width / scale_factor))),
        max(1, int(round(height / scale_factor))),
    )


def downscale_images(input_folder: str, output_folder: str, scale_factor: float = 2.0) -> None:
    """ Downscale images from input_folder into output_folder.

    Args:
        input_folder: Folder containing input images.
        output_folder: Folder where resized images will be saved.
        scale_factor: Factor to divide width and height by. Defaults to 2.
    """
    input_path = Path(input_folder).expanduser().resolve()
    output_path = Path(output_folder).expanduser().resolve()

    if not input_path.is_dir():
        raise ValueError(f"Input folder does not exist or is not a directory: {input_path}")
    if scale_factor <= 0:
        raise ValueError("scale_factor must be greater than 0")
    if input_path == output_path:
        raise ValueError("Input and output folders must be different to avoid overwriting files")

    output_path.mkdir(parents=True, exist_ok=True)

    paths = _image_paths(input_path)
    image_sizes: dict[Path, tuple[int, int]] = {}
    unreadable_paths: list[Path] = []

    for path in paths:
        size = _read_image_size(path)
        if size is None:
            unreadable_paths.append(path)
        else:
            image_sizes[path] = size

    if not image_sizes:
        print("Number of images: 0")
        print("No readable images found.")
        return

    first_path, (first_width, first_height) = next(iter(image_sizes.items()))
    first_out_width, first_out_height = _output_size(first_width, first_height, scale_factor)
    unique_sizes = set(image_sizes.values())

    print(f"Number of images: {len(image_sizes)}")
    print(f"Image size: {first_width}x{first_height}")
    print(f"Output image size: {first_out_width}x{first_out_height}")
    if len(unique_sizes) > 1:
        print(f"Note: input images have {len(unique_sizes)} different sizes; each image is scaled individually.")
    if unreadable_paths:
        print(f"Skipped unreadable image files: {len(unreadable_paths)}")

    for path, (width, height) in tqdm(image_sizes.items(), desc="Downscaling images", unit="image"):
        image = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
        if image is None:
            tqdm.write(f"Skipping unreadable image: {path}")
            continue

        out_width, out_height = _output_size(width, height, scale_factor)
        resized = cv2.resize(image, (out_width, out_height), interpolation=cv2.INTER_AREA)
        output_file = output_path / path.name

        if not cv2.imwrite(str(output_file), resized):
            raise RuntimeError(f"Failed to write output image: {output_file}")


if __name__ == "__main__":
    Fire(downscale_images)
