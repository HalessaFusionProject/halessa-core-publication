#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:
    raise SystemExit("Missing dependency: Pillow. Install with `pip install pillow`.") from exc


PHASES = [
    ("phase1_delta_q.png", "Phase I - Delta Q Sweep"),
    ("QESR_phase2_bloom_summary.png", "Phase II - Bloom Summary"),
    ("phase3_harmonic_feedback.png", "Phase III - Harmonic Feedback"),
    ("phase4_feedback_echo.png", "Phase IV - Feedback Echo"),
    ("phase5_echo_spiral.png", "Phase V - Echo Spiral"),
    ("phase6_curl_threading.png", "Phase VI - Curl Threading"),
]


def parse_canvas(value: str | None) -> tuple[int, int] | None:
    if not value or value.lower() == "auto":
        return None
    if "x" not in value:
        raise ValueError("Canvas must be like 1024x768 or 'auto'.")
    width, height = value.lower().split("x", 1)
    return int(width), int(height)


def fit_to_canvas(img: Image.Image, canvas: tuple[int, int] | None, bg_color: tuple[int, int, int]) -> Image.Image:
    if canvas is None:
        return img
    target_w, target_h = canvas
    img_ratio = img.width / img.height
    target_ratio = target_w / target_h
    if img_ratio > target_ratio:
        new_w = target_w
        new_h = int(target_w / img_ratio)
    else:
        new_h = target_h
        new_w = int(target_h * img_ratio)
    resized = img.resize((new_w, new_h), Image.LANCZOS)
    canvas_img = Image.new("RGB", (target_w, target_h), bg_color)
    x = (target_w - new_w) // 2
    y = (target_h - new_h) // 2
    canvas_img.paste(resized, (x, y))
    return canvas_img


def add_title_overlay(img: Image.Image, title: str, font: ImageFont.ImageFont) -> Image.Image:
    base = img.convert("RGBA")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    try:
        text_bbox = draw.textbbox((0, 0), title, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
    except AttributeError:
        text_w, text_h = draw.textsize(title, font=font)
    padding_x = 24
    padding_y = 14
    box_w = text_w + padding_x * 2
    box_h = text_h + padding_y * 2
    x = (base.width - box_w) // 2
    y = base.height - box_h - 32
    draw.rectangle([x, y, x + box_w, y + box_h], fill=(0, 0, 0, 160))
    draw.text((x + padding_x, y + padding_y), title, font=font, fill=(255, 255, 255, 255))
    return Image.alpha_composite(base, overlay).convert("RGB")


def load_font(font_path: Path | None, size: int) -> ImageFont.ImageFont:
    if font_path:
        return ImageFont.truetype(str(font_path), size=size)
    return ImageFont.load_default()


def build_frames(
    input_dir: Path,
    canvas: tuple[int, int] | None,
    overlay_titles: bool,
    font: ImageFont.ImageFont,
    bg_color: tuple[int, int, int],
) -> list[Image.Image]:
    frames: list[Image.Image] = []
    for filename, title in PHASES:
        image_path = input_dir / filename
        if not image_path.exists():
            raise FileNotFoundError(f"Missing input image: {image_path}")
        img = Image.open(image_path).convert("RGB")
        img = fit_to_canvas(img, canvas, bg_color)
        if overlay_titles:
            img = add_title_overlay(img, title, font)
        frames.append(img)
    return frames


def preview_frames(frames: list[Image.Image], titles: list[str]) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit("Missing dependency: matplotlib. Install with `pip install matplotlib`.") from exc
    instructions = "Click or press any key to advance (close window to exit)."
    for frame, title in zip(frames, titles):
        fig, ax = plt.subplots()
        ax.imshow(frame)
        ax.axis("off")
        ax.set_title(title)
        fig.text(0.5, 0.02, instructions, ha="center", va="bottom")
        fig.canvas.manager.set_window_title("QESR Phase Preview")
        plt.show(block=False)
        plt.waitforbuttonpress()
        plt.close(fig)


def write_gif(frames: list[Image.Image], output_path: Path, seconds_per_frame: float) -> None:
    if not frames:
        raise ValueError("No frames to write.")
    duration_ms = int(seconds_per_frame * 1000)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0,
        optimize=False,
    )


def write_mp4(
    frames: list[Image.Image],
    output_path: Path,
    seconds_per_frame: float,
    fps: int,
) -> None:
    try:
        import imageio.v2 as imageio
    except ImportError as exc:
        raise SystemExit("Missing dependency: imageio. Install with `pip install imageio`.") from exc
    hold_frames = max(1, round(seconds_per_frame * fps))
    with imageio.get_writer(
        output_path,
        fps=fps,
        codec="libx264",
        quality=8,
        macro_block_size=None,
    ) as writer:
        for frame in frames:
            arr = np.asarray(frame)
            for _ in range(hold_frames):
                writer.append_data(arr)


def main() -> int:
    parser = argparse.ArgumentParser(description="Concatenate QESR phase previews into a GIF and MP4.")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("results/orchestration_previews"),
        help="Directory containing phase PNGs.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results"),
        help="Directory to write outputs.",
    )
    parser.add_argument(
        "--canvas",
        default="1024x768",
        help="Canvas size like 1024x768, or 'auto' to preserve original.",
    )
    parser.add_argument(
        "--seconds-per-frame",
        type=float,
        default=2.5,
        help="Seconds to hold each frame.",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=2,
        help="FPS for MP4 (frames are repeated to match seconds-per-frame).",
    )
    parser.add_argument(
        "--no-titles",
        action="store_true",
        help="Disable title overlay.",
    )
    parser.add_argument(
        "--font",
        type=Path,
        default=None,
        help="Optional path to a .ttf/.otf font for overlays.",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Show each frame and wait for a click/key press before continuing.",
    )
    args = parser.parse_args()

    canvas = parse_canvas(args.canvas)
    font = load_font(args.font, size=36)
    frames = build_frames(
        args.input_dir,
        canvas,
        overlay_titles=not args.no_titles,
        font=font,
        bg_color=(12, 12, 12),
    )
    if args.interactive:
        preview_frames(frames, [title for _, title in PHASES])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    gif_path = args.output_dir / "QESR_simulation_phase_sequence.gif"
    mp4_path = args.output_dir / "QESR_simulation_phase_sequence.mp4"

    write_gif(frames, gif_path, args.seconds_per_frame)
    write_mp4(frames, mp4_path, args.seconds_per_frame, fps=args.fps)
    print(f"Wrote: {gif_path}")
    print(f"Wrote: {mp4_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
