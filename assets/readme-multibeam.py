"""Render the README illustration from the preserved contour image.

Run from any directory with Python 3.10+, Pillow and NumPy:
    python assets\\readme-multibeam.py

The contour geometry comes from code\\问题四\\等深线图.png. Only its
palette and projection change. Vessel, beams, swaths and survey lines are
conceptual illustrations; this image does not represent a verified solution.
The source SHA-256 is embedded in the resulting PNG.

Use --font-regular and --font-bold to supply Chinese fonts on other systems.
No project solver modules or generated verification reports are required.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin


WIDTH, HEIGHT, SCALE = 1800, 1000, 2
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "code" / "问题四" / "等深线图.png"
OUTPUT = Path(__file__).with_suffix(".png")
INK = (232, 249, 250)
MUTED = (135, 177, 190)
AQUA = (93, 231, 223)
MAP_ORIGIN = np.array([760.0, 660.0])
MAP_AXES = np.array([[740.0, 235.0], [142.0, -333.0]])


def point(u: float, v: float) -> tuple[float, float]:
    return tuple(MAP_ORIGIN + MAP_AXES @ np.array([u, v]))


def pixels(points):
    return [(round(x * SCALE), round(y * SCALE)) for x, y in points]


def line(draw, points, fill, width=1):
    draw.line(pixels(points), fill=fill, width=max(1, round(width * SCALE)), joint="curve")


def dashed(draw, start, end, fill, width=1.5, dash=12, gap=12):
    start, end = np.array(start), np.array(end)
    length = np.linalg.norm(end - start)
    direction = (end - start) / length
    for position in np.arange(0, length, dash + gap):
        line(draw, [start + direction * position, start + direction * min(position + dash, length)], fill, width)


def fonts(arguments):
    regular, bold = Path(arguments.font_regular), Path(arguments.font_bold)
    for font_path in (regular, bold):
        if not font_path.is_file():
            raise FileNotFoundError(f"Chinese font unavailable: {font_path}; pass --font-regular / --font-bold")
    return {
        "title": ImageFont.truetype(str(bold), 98 * SCALE),
        "label": ImageFont.truetype(str(regular), 29 * SCALE),
        "small": ImageFont.truetype(str(regular), 26 * SCALE),
        "tiny": ImageFont.truetype(str(regular), 24 * SCALE),
        "identifier": ImageFont.truetype(str(bold), 26 * SCALE),
    }


def text(draw, position, value, font, fill=INK):
    draw.text((round(position[0] * SCALE), round(position[1] * SCALE)), value, font=font, fill=fill, anchor="lt")


def background():
    y, x = np.mgrid[0 : HEIGHT * SCALE, 0 : WIDTH * SCALE]
    x, y = x / SCALE, y / SCALE
    glow = np.exp(-(((x - 1390) / 660) ** 2 + ((y - 430) / 540) ** 2))
    low_glow = np.exp(-(((x - 180) / 700) ** 2 + ((y - 1150) / 700) ** 2))
    channels = [6 + glow * 4 + low_glow * 2, 19 + glow * 24 + low_glow * 9, 31 + glow * 30 + low_glow * 11]
    rgb = np.stack(channels, axis=-1).astype(np.uint8)
    return Image.fromarray(rgb).convert("RGBA")


def contour_texture():
    with Image.open(SOURCE) as original:
        if original.size != (772, 609):
            raise ValueError(f"Contour image dimensions changed: {original.size}; review crop before rendering")
        crop = original.convert("RGB").crop((71, 9, 666, 543))
    hsv = np.asarray(crop.convert("HSV"), dtype=np.float32)
    rgb = np.asarray(crop, dtype=np.float32)
    amount = np.clip((181 - hsv[:, :, 0]) / 140, 0, 1)
    first = np.array([12, 49, 69], dtype=np.float32)
    second = np.array([33, 116, 126], dtype=np.float32)
    recolored = first + amount[:, :, None] * (second - first)
    contour = rgb.max(axis=-1) < 100
    recolored[contour] = [83, 160, 166]
    return Image.fromarray(recolored.astype(np.uint8)).convert("RGBA")


def project_texture(texture):
    inverse = np.linalg.inv(MAP_AXES)
    width, height = texture.size
    a, b = width * inverse[0] / SCALE
    c = -width * (inverse[0] @ MAP_ORIGIN)
    d, e = -height * inverse[1] / SCALE
    f = height * (1 + inverse[1] @ MAP_ORIGIN)
    return texture.transform((WIDTH * SCALE, HEIGHT * SCALE), Image.Transform.AFFINE, (a, b, c, d, e, f), Image.Resampling.BICUBIC)


def draw_map(canvas):
    draw = ImageDraw.Draw(canvas)
    a, b, c, d = [point(*pair) for pair in [(0, 0), (1, 0), (1, 1), (0, 1)]]
    lower = lambda p: (p[0], p[1] + 42)
    draw.polygon(pixels([a, b, lower(b), lower(a)]), fill=(8, 40, 55))
    draw.polygon(pixels([b, c, lower(c), lower(b)]), fill=(9, 54, 65))
    line(draw, [lower(a), lower(b), lower(c)], (24, 83, 95), 1.3)
    canvas.alpha_composite(project_texture(contour_texture()))
    draw = ImageDraw.Draw(canvas)
    line(draw, [a, b, c, d, a], (81, 173, 181), 1.6)
    for u in np.linspace(0.1, 0.9, 9):
        line(draw, [point(u, 0), point(u, -0.025)], (79, 119, 137), 1)
    for v in np.linspace(0.1, 0.9, 9):
        line(draw, [point(1, v), point(1.014, v)], (79, 119, 137), 1)


def draw_routes(canvas):
    overlay = Image.new("RGBA", canvas.size)
    draw = ImageDraw.Draw(overlay)
    for index, u in enumerate([0.16, 0.35, 0.54, 0.73, 0.92]):
        fill = (168, 233, 238, 175 if index == 2 else 115)
        dashed(draw, point(u, 0.09), point(u, 0.91), fill, 2.0 if index == 2 else 1.7, 11, 12)
    swath = [point(0.065, 0.51), point(0.94, 0.51), point(0.94, 0.64), point(0.065, 0.64)]
    draw.polygon(pixels(swath), fill=(88, 241, 207, 57))
    for v in [0.51, 0.64]:
        line(draw, [point(0.065, v), point(0.94, v)], (139, 253, 229, 200), 1.7)
    canvas.alpha_composite(overlay)


def draw_fan(canvas):
    source = (point(0.52, 0.575)[0], 272)
    left, right = point(0.065, 0.575), point(0.94, 0.575)
    mask = Image.new("L", canvas.size)
    ImageDraw.Draw(mask).polygon(pixels([source, left, right]), fill=255)
    overlay = Image.new("RGBA", canvas.size)
    draw = ImageDraw.Draw(overlay)
    for row in range(round(source[1] * SCALE), round(right[1] * SCALE) + 1):
        amount = (row / SCALE - source[1]) / (right[1] - source[1])
        draw.line([(0, row), (WIDTH * SCALE, row)], fill=(97, 235, 227, round(9 + 26 * amount)))
    empty = Image.new("RGBA", canvas.size)
    canvas.alpha_composite(Image.composite(overlay, empty, mask))
    draw = ImageDraw.Draw(canvas)
    for u in np.linspace(0.065, 0.94, 13):
        line(draw, [source, point(u, 0.575)], (65, 132, 150), 1)
    for endpoint in [left, right]:
        line(draw, [source, endpoint], (94, 211, 216), 1.8)
    line(draw, [left, right], (172, 255, 235), 2.4)
    draw.ellipse((round((source[0] - 5) * SCALE), round((source[1] - 5) * SCALE), round((source[0] + 5) * SCALE), round((source[1] + 5) * SCALE)), fill=AQUA)
    return source


def draw_vessel(canvas, source):
    draw = ImageDraw.Draw(canvas)
    cx, cy = source[0], source[1] - 8
    hull = [(cx - 98, cy - 29), (cx + 108, cy - 29), (cx + 85, cy + 1), (cx - 71, cy + 1)]
    draw.polygon(pixels(hull), fill=(217, 247, 247))
    draw.polygon(pixels([(cx - 90, cy - 18), (cx + 99, cy - 18), (cx + 85, cy + 1), (cx - 71, cy + 1)]), fill=(95, 214, 212))
    draw.polygon(pixels([(cx - 68, cy - 65), (cx + 33, cy - 65), (cx + 47, cy - 29), (cx - 68, cy - 29)]), fill=(231, 248, 247))
    draw.polygon(pixels([(cx - 51, cy - 91), (cx + 14, cy - 91), (cx + 24, cy - 65), (cx - 51, cy - 65)]), fill=(210, 239, 240))
    for x in [-43, -16, 11]:
        draw.rectangle((round((cx + x) * SCALE), round((cy - 58) * SCALE), round((cx + x + 16) * SCALE), round((cy - 45) * SCALE)), fill=(15, 59, 77))
    line(draw, [(cx - 21, cy - 91), (cx - 21, cy - 128)], (166, 221, 226), 3)
    line(draw, [(cx - 40, cy - 110), (cx + 5, cy - 110)], (166, 221, 226), 2)
    line(draw, [(cx + 57, cy - 29), (cx + 57, cy - 46), (cx + 93, cy - 46)], (178, 235, 236), 2)
    for offset, opacity in [(13, (64, 125, 143)), (22, (33, 81, 103))]:
        line(draw, [(cx - 111, cy + offset), (cx - 55, cy + offset), (cx - 42, cy + offset - 4)], opacity, 1.5)


def draw_concepts(canvas, font):
    draw = ImageDraw.Draw(canvas)
    centers = [174, 379, 584]
    y = 639
    for cx in [278, 483]:
        line(draw, [(cx, y - 8), (cx, y + 118)], (25, 58, 77), 1)
    cx = centers[0]
    line(draw, [(cx - 51, y + 65), (cx + 51, y + 65)], AQUA, 2.4)
    line(draw, [(cx - 42, y + 58), (cx - 51, y + 65), (cx - 42, y + 72)], AQUA, 2)
    line(draw, [(cx + 42, y + 58), (cx + 51, y + 65), (cx + 42, y + 72)], AQUA, 2)
    line(draw, [(cx - 48, y + 47), (cx, y + 3), (cx + 48, y + 47)], (102, 160, 181), 2)
    cx = centers[1]
    for shift in [-23, 23]:
        draw.rounded_rectangle((round((cx + shift - 31) * SCALE), round((y + 12) * SCALE), round((cx + shift + 31) * SCALE), round((y + 65) * SCALE)), radius=7 * SCALE, outline=(83, 164, 181), width=2 * SCALE)
    draw.rectangle((round((cx - 8) * SCALE), round((y + 13) * SCALE), round((cx + 8) * SCALE), round((y + 64) * SCALE)), fill=(62, 147, 146))
    line(draw, [(cx, y + 17), (cx, y + 60)], AQUA, 2.2)
    cx = centers[2]
    for shift in [-41, 0, 41]:
        line(draw, [(cx + shift, y + 8), (cx + shift, y + 68)], (96, 177, 189), 2)
    line(draw, [(cx - 36, y + 36), (cx - 5, y + 36)], AQUA, 2)
    line(draw, [(cx - 31, y + 30), (cx - 37, y + 36), (cx - 31, y + 42)], AQUA, 2)
    line(draw, [(cx - 11, y + 30), (cx - 5, y + 36), (cx - 11, y + 42)], AQUA, 2)
    for cx, label in zip(centers, ["覆盖宽度", "相邻重叠", "测线间距"]):
        width = draw.textlength(label, font=font["small"]) / SCALE
        text(draw, (cx - width / 2, y + 92), label, font["small"], (168, 204, 215))


def draw_typography(canvas, font):
    draw = ImageDraw.Draw(canvas)
    line(draw, [(92, 82), (130, 82)], AQUA, 4)
    text(draw, (150, 67), "2023 全国大学生数学建模竞赛 · B 题", font["identifier"], (173, 212, 220))
    draw.rounded_rectangle((1510 * SCALE, 62 * SCALE, 1710 * SCALE, 113 * SCALE), radius=25 * SCALE, outline=(53, 111, 129), width=SCALE)
    text(draw, (1558, 74), "概念示意", font["small"], (157, 215, 221))
    text(draw, (88, 209), "多波束", font["title"])
    text(draw, (88, 335), "测线规划", font["title"])
    text(draw, (95, 496), "海底地形 · 覆盖几何 · 测线布局", font["label"], MUTED)
    line(draw, [(97, 584), (666, 584)], (28, 60, 80), 1)
    text(draw, (904, 252), "声束扇面", font["small"], (166, 214, 221))
    line(draw, [(948, 290), (1003, 328), (1073, 386)], (72, 129, 148), 1.2)
    text(draw, (1430, 244), "测量船", font["small"], (166, 214, 221))
    line(draw, [(1411, 260), (1387, 260)], (72, 129, 148), 1.2)
    text(draw, (1530, 702), "覆盖带", font["small"], (173, 234, 227))
    line(draw, [(1534, 687), (1495, 642), point(0.79, 0.51)], (105, 186, 183), 1.2)
    text(draw, (1199, 833), "等深线底图 / 测线投影", font["small"], (132, 182, 193))
    line(draw, [(92, 905), (1710, 905)], (37, 74, 91), 1)
    text(draw, (96, 936), "等深线底图取自仓库历史成果；声束、覆盖带及测线为概念示意。", font["tiny"], (135, 174, 188))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font-regular", default=r"C:\Windows\Fonts\msyh.ttc")
    parser.add_argument("--font-bold", default=r"C:\Windows\Fonts\msyhbd.ttc")
    arguments = parser.parse_args()
    font = fonts(arguments)
    canvas = background()
    draw_map(canvas)
    draw_routes(canvas)
    source = draw_fan(canvas)
    draw_vessel(canvas, source)
    draw_concepts(canvas, font)
    draw_typography(canvas, font)
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("Title", "2023 国赛 B 题：多波束测线规划")
    metadata.add_text("Description", "历史等深线图改色并做平面投影；船舶、声束、覆盖带和测线均为概念示意，不对应验证方案。")
    metadata.add_text("ContourSource", "code/问题四/等深线图.png")
    metadata.add_text("ContourSourceSHA256", hashlib.sha256(SOURCE.read_bytes()).hexdigest())
    canvas.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS).save(OUTPUT, optimize=True, pnginfo=metadata)
    print(f"Rendered: {OUTPUT} ({WIDTH} x {HEIGHT})")
    print(f"Preserved contour source SHA-256: {hashlib.sha256(SOURCE.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
