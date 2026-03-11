from __future__ import annotations

from pathlib import Path

from PIL import Image


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    frames_dir = root / "docs" / "demo-frames"
    output = root / "docs" / "screenshots" / "copilot-sre-demo.gif"

    frame_paths = sorted(frames_dir.glob("frame-*.png"))
    if not frame_paths:
        raise SystemExit("No demo frames found")

    frames = []
    for frame_path in frame_paths:
        image = Image.open(frame_path).convert("P", palette=Image.ADAPTIVE)
        frames.append(image)

    durations = [1100, 1400, 1200, 1200, 1200, 1200, 1200, 1600][: len(frames)]
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
    )
    print(output)


if __name__ == "__main__":
    main()
