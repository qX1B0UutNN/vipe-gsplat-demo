"""
Convert frame sequence into .mp4 video file.
AI generated.
"""

import re
import sys
import cv2

from pathlib import Path
from fire import Fire

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


def natural_sort_key(path: Path):
    """
    Sort filenames naturally:
    frame2.jpg comes before frame10.jpg.
    """
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", path.name)
    ]


def images_to_video(
    input_dir: str,
    output_path: str,
    fps: float = 15.0,
    skip_first_n: int = -1,
) -> None:
    """ Convert image sequence into .mp4 video file.

    Args:
        input_dir: Folder containing sequence of input images.
        output_path: Filepath to save output .mp4 file.
        fps: Number of frames per seconds in output file.
        skip_first_n: Do not add first n frames into output file (skip them).
    """
    input_dir = Path(input_dir)
    output_path = Path(output_path)

    files = sorted(
        [
            path
            for path in input_dir.iterdir()
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
        ],
        key=natural_sort_key,
    )

    if not files:
        raise RuntimeError(f"No images found in: {input_dir}")

    first_frame = cv2.imread(str(files[0]))
    if first_frame is None:
        raise RuntimeError(f"Could not read first image: {files[0]}")

    height, width = first_frame.shape[:2]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # mp4v is widely available and creates an MP4 file.
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(
        str(output_path),
        fourcc,
        fps,
        (width, height),
    )

    if not writer.isOpened():
        raise RuntimeError(f"Could not create video: {output_path}")

    print(f"Found {len(files)} frames")
    print(f"Resolution: {width}x{height}")
    print(f"FPS: {fps}")
    print(f"First frame: {files[0].name}")
    print(f"Last frame:  {files[-1].name}")

    try:
        for index, path in enumerate(files):
            if skip_first_n != -1 and index < skip_first_n:
                continue

            frame = cv2.imread(str(path))

            if frame is None:
                print(f"Warning: skipping unreadable image: {path.name}")
                continue

            frame_height, frame_width = frame.shape[:2]

            if (frame_width, frame_height) != (width, height):
                print(
                    f"Resizing {path.name}: "
                    f"{frame_width}x{frame_height} -> {width}x{height}"
                )
                frame = cv2.resize(
                    frame,
                    (width, height),
                    interpolation=cv2.INTER_AREA,
                )

            writer.write(frame)

            if index < 20:
                print(f"{index:04d}: {path.name}")

    finally:
        writer.release()

    print(f"Saved video to: {output_path}")


if __name__ == "__main__":
    Fire(images_to_video)
