"""Draws the pixel-art background: a medieval landscape, one image for day and one for night.

    python tools/landscape.py

Writes public/bg/landscape-day.png and landscape-night.png. The image tiles horizontally
(every layer is periodic in x), so it can repeat on very wide screens. Colours sit close to
the page background on purpose: the landscape should be noticed on a second look, not the first.
"""

import math
import random
from pathlib import Path

from PIL import Image

W, H = 640, 150
SEED = 26

# Palette index -> role. 0 is transparent sky.
SKY, STAR, STAR2, ORB, FAR, SNOW, DRAGON, MID, BUILD, WINDOW, NEAR = range(11)

PALETTES = {
    "day": {
        STAR: None,
        STAR2: None,
        ORB: "#e8e2cf",
        FAR: "#e3e6e4",
        SNOW: "#ecefed",
        DRAGON: "#d9ddda",
        MID: "#d8ddd9",
        BUILD: "#ccd3ce",
        WINDOW: "#ccd3ce",
        NEAR: "#c9d0ca",
    },
    "night": {
        STAR: "#262c3a",
        STAR2: "#3a4356",
        ORB: "#2f3749",
        FAR: "#1a202c",
        SNOW: "#212837",
        DRAGON: "#1d2330",
        MID: "#161b25",
        BUILD: "#131821",
        WINDOW: "#b8862e",
        NEAR: "#12151d",
    },
}


def periodic_noise(points: int, amp: float, rng: random.Random):
    """Smooth random curve that wraps around at x = W."""
    vals = [rng.uniform(-1, 1) for _ in range(points)]

    def f(x: float) -> float:
        t = x / W * points
        i = math.floor(t)
        u = t - i
        a, b = vals[i % points], vals[(i + 1) % points]
        u = (1 - math.cos(u * math.pi)) / 2
        return (a * (1 - u) + b * u) * amp

    return f


def draw(night: bool) -> list[list[int]]:
    rng = random.Random(SEED)
    g = [[SKY] * W for _ in range(H)]

    def put(x: int, y: int, c: int):
        if 0 <= y < H:
            g[y][x % W] = c

    def fill_below(x: int, top: int, c: int):
        for y in range(max(top, 0), H):
            put(x, y, c)

    def rect(x0: int, y0: int, w: int, h: int, c: int):
        for x in range(x0, x0 + w):
            for y in range(y0, y0 + h):
                put(x, y, c)

    # Stars, only drawn at night but always rolled so the rest of the scene matches between versions.
    stars = [(rng.randrange(W), rng.randrange(0, 80), rng.random()) for _ in range(140)]
    if night:
        for x, y, r in stars:
            put(x, y, STAR2 if r > 0.85 else STAR)

    # Sun by day, crescent moon by night.
    cx, cy, r = 548, 26, 8
    for x in range(cx - r, cx + r + 1):
        for y in range(cy - r, cy + r + 1):
            inside = (x - cx) ** 2 + (y - cy) ** 2 <= r * r
            bite = night and (x - cx - 4) ** 2 + (y - cy + 2) ** 2 <= (r - 1) ** 2
            if inside and not bite:
                put(x, y, ORB)

    # Far mountains: overlapping sharp peaks, snow near the tops.
    peaks = [(rng.randrange(W), rng.randint(14, 42), rng.uniform(0.55, 1.1)) for _ in range(13)]
    far_fine = periodic_noise(80, 1.5, rng)
    for x in range(W):
        rise = 0.0
        for px, ph, slope in peaks:
            d = min(abs(x - px), W - abs(x - px))
            rise = max(rise, ph - d * slope)
        top = int(76 - rise + far_fine(x))
        fill_below(x, top, FAR)
        if rise > 24:
            depth = int((rise - 24) * 0.6) + 1
            for y in range(top, top + depth):
                if y == top or (x * 7 + y * 3) % 5:
                    put(x, y, SNOW)

    # A dragon, far off, flying left.
    dragon = [
        "...........##.......",
        "..........###.......",
        ".........####.......",
        "........#####.......",
        "###....######.......",
        ".##########.....####",
        "..############.##...",
        "......########......",
        ".......#...#........",
    ]
    for dy, row in enumerate(dragon):
        for dx, ch in enumerate(row):
            if ch == "#":
                put(170 + dx, 22 + dy, DRAGON)

    # Middle hills, with a rise under the castle.
    mid = periodic_noise(7, 9, rng)
    castle_x = 410

    def mid_top(x: int) -> int:
        d = min(abs(x - castle_x), W - abs(x - castle_x))
        bump = 16 * math.exp(-((d / 38) ** 2))
        return int(100 + mid(x) - bump)

    for x in range(W):
        fill_below(x, mid_top(x), MID)

    # Castle: curtain wall, two towers, a keep and a flag.
    base = mid_top(castle_x) + 2
    rect(castle_x - 20, base - 9, 41, 9, BUILD)
    for x in range(castle_x - 20, castle_x + 21, 2):
        put(x, base - 10, BUILD)
    for tx in (castle_x - 24, castle_x + 19):
        rect(tx, base - 17, 6, 17, BUILD)
        for i in range(4):
            rect(tx + i // 2, base - 18 - i, 6 - 2 * (i // 2), 1, BUILD)
    rect(castle_x - 6, base - 24, 13, 24, BUILD)
    for i in range(6):
        rect(castle_x - 6 + i, base - 25 - i, 13 - 2 * i, 1, BUILD)
    rect(castle_x, base - 36, 1, 6, BUILD)
    rect(castle_x + 1, base - 36, 3, 2, BUILD)
    for wx, wy in [(castle_x - 3, base - 18), (castle_x + 3, base - 18), (castle_x, base - 12),
                   (castle_x - 22, base - 12), (castle_x + 21, base - 12)]:
        put(wx, wy, WINDOW)

    # A ruined watchtower on the far side.
    ruin_x = 96
    rb = mid_top(ruin_x) + 2
    rect(ruin_x, rb - 15, 7, 15, BUILD)
    for i, h in enumerate([2, 0, 3, 1, 0, 2, 4]):
        for y in range(rb - 15, rb - 15 + h):
            put(ruin_x + i, y, SKY if g[y][(ruin_x + i) % W] == BUILD else g[y][(ruin_x + i) % W])
    rect(ruin_x + 3, rb - 10, 1, 2, SKY)

    # Near ground and pine forest.
    ground = periodic_noise(5, 3, rng)
    for x in range(W):
        fill_below(x, int(134 + ground(x)), NEAR)
    x = 0
    while x < W:
        h = rng.randint(7, 17)
        gx = int(134 + ground(x))
        for dy in range(h):
            half = (dy + 1) // 2 if dy % 4 != 3 else (dy - 1) // 2
            for dx in range(-half, half + 1):
                put(x + dx, gx - h + dy, NEAR)
        x += rng.randint(3, 9) if rng.random() < 0.8 else rng.randint(18, 40)

    return g


def render(name: str):
    pal = PALETTES[name]
    grid = draw(name == "night")
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()
    for y in range(H):
        for x in range(W):
            c = pal.get(grid[y][x])
            if c:
                px[x, y] = tuple(int(c[i : i + 2], 16) for i in (1, 3, 5)) + (255,)
    out = Path(__file__).resolve().parent.parent / "public" / "bg" / f"landscape-{name}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, optimize=True)
    print(out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    render("day")
    render("night")
