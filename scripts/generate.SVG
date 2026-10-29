"""
Builds icons/animated/animatedScreen.svg from the GIFs in icons/animated/.
Needs Pillow:  pip install pillow
Run from the repo root:  python scripts/generateSVG.py
"""
import base64, io, math
from PIL import Image, ImageSequence, ImageOps

# ================================================================ settings you can tweak
FRONT_SPEED = 75        # units/second: how fast the digit stream spreads along its path
SOFT = 36               # softness of the front edge of the stream (units)
RAMP_SECONDS = 2.0      # how long an icon takes to "turn on" (slow start up to full speed)
RAMP_FRAMES = 12        # how many of the icon's first frames are played in slow motion
PROCESS_DELAY = 0.8     # pause after the language icons are fully on, before digits head to github
EXTRA_DELAY = 0.0       # push the whole sequence later (seconds)
# The still image an icon shows while it is "off". None = automatic (the frame with the most visible pixels,
# normally the complete icon). Or give a frame number, e.g. {"javaIcon": 0}.
STATIC_FRAME = {"javaIcon": None, "javascriptIcon": None, "pythonIcon": None,
                "react-nativeIcon": None, "githubIcon": None}

# ================================================================ helpers
def b64(raw):
    return base64.b64encode(raw).decode()

def gif_b64(name):
    with open(f"icons/animated/{name}.gif", "rb") as f:
        return b64(f.read())

_NONE = getattr(Image, "Dither", Image).NONE

def encode(frame):
    """RGBA frame -> palette image with transparent index 0 (what GIF needs)."""
    alpha = frame.getchannel("A").point(lambda a: 255 if a >= 128 else 0)
    q = frame.convert("RGB").quantize(colors=255, dither=_NONE)
    pal = q.getpalette()[:765]
    q = q.point(lambda i: min(i + 1, 255))
    q.putpalette([0, 0, 0] + pal)
    q.paste(0, mask=ImageOps.invert(alpha))
    q.info = {"transparency": 0}      # drop what was inherited from the source GIF (loop count, delays...)
    return q

def to_gif(frames, delays, loop):
    buf = io.BytesIO()
    kw = dict(format="GIF", save_all=True, append_images=frames[1:], duration=delays,
              transparency=0, disposal=2, optimize=False)
    if loop:
        kw["loop"] = 0          # no loop block = plays once and holds its last frame
    frames[0].save(buf, **kw)
    return buf.getvalue()

_icon_cache = {}

def prepare_icon(name):
    """Returns (still_png, ramp_gif, loop_gif, ramp_seconds) for one icon.
    still : the icon as a picture (shown while the icon is off)
    ramp  : the first RAMP_FRAMES frames in slow motion, speeding up (plays once)
    loop  : the full animation, continuing exactly where the ramp stopped (loops forever)"""
    if name in _icon_cache:
        return _icon_cache[name]
    im = Image.open(f"icons/animated/{name}.gif")
    frames, durs, full = [], [], []
    for fr in ImageSequence.Iterator(im):
        rgba = fr.convert("RGBA")
        durs.append(fr.info.get("duration", 40) or 40)
        full.append(sum(rgba.getchannel("A").histogram()[1:]))      # visible pixels
        frames.append(encode(rgba))
    n = len(frames)
    s = STATIC_FRAME.get(name)
    if s is None:
        s = full.index(max(full))
    order = [(s + i) % n for i in range(n)]
    seq = [frames[i] for i in order]
    dseq = [durs[i] for i in order]

    png = io.BytesIO()
    seq[0].copy().convert("RGBA").save(png, "PNG", optimize=True)   # from a copy: converting the original would corrupt its palette

    if n < 4:                                    # a still image: nothing to animate
        res = (png.getvalue(), None, None, 0.0)
    else:
        k = min(RAMP_FRAMES, n - 1)
        while k > 2 and sum(dseq[:k]) > 0.5 * RAMP_SECONDS * 1000:
            k -= 1
        w = [(1 - i / (k - 1)) ** 2 for i in range(k)]                # 1 -> 0 : slowest first, normal speed last
        base = sum(dseq[:k]); wsum = sum(d * wi for d, wi in zip(dseq[:k], w))
        m0 = max(1.0, 1 + (RAMP_SECONDS * 1000 - base) / wsum)
        rd = [max(20, int(round(d * (1 + (m0 - 1) * wi) / 10.0)) * 10) for d, wi in zip(dseq[:k], w)]
        ramp = to_gif(seq[:k], rd, loop=False)
        loop = to_gif(seq[k:] + seq[:k], dseq[k:] + dseq[:k], loop=True)
        res = (png.getvalue(), ramp, loop, sum(rd) / 1000.0)
    _icon_cache[name] = res
    return res

def pic(x, y, w, h, mime, raw_b64, begin=0.0, end=None, stretch=False):
    """An embedded picture that shows from `begin` seconds until `end` seconds.
    A GIF starts playing from its first frame when it is first displayed."""
    attrs = f'x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}"'
    if stretch:
        attrs += ' preserveAspectRatio="none"'
    kids = ""
    if begin > 0:
        attrs += ' display="none"'
        kids += f'<set attributeName="display" to="inline" begin="{begin:.2f}s" fill="freeze"/>'
    if end is not None:
        kids += f'<set attributeName="display" to="none" begin="{end:.2f}s" fill="freeze"/>'
    return f'<image {attrs} href="data:{mime};base64,{raw_b64}">{kids}</image>'

OVERLAP = 0.04   # seconds the old picture stays under the new one, so there is never a blink at a hand-over

def icon(name, x, y, size, start):
    """Visible and still from the start. At `start` it turns on slowly, then runs freely forever."""
    png, ramp, loop, rs = prepare_icon(name)
    out = [pic(x, y, size, size, "image/png", b64(png), end=(start + OVERLAP) if ramp else None)]
    if ramp:
        out.append(pic(x, y, size, size, "image/gif", b64(ramp), begin=start, end=start + rs + OVERLAP))
        out.append(pic(x, y, size, size, "image/gif", b64(loop), begin=start + rs))
    return "\n  ".join(out)

defs = []

def reveal(uid, name, box, S, E, start):
    """Show the looping flow GIF `name` progressively from point S towards E, starting at `start` seconds,
    with a soft-edged mask. Returns (markup, seconds the first digits need to reach E)."""
    bx, by, bw, bh = box
    L = math.dist(S, E)
    ux, uy = (E[0] - S[0]) / L, (E[1] - S[1]) / L
    dur = (L + SOFT) / FRONT_SPEED
    arrive = L / FRONT_SPEED
    p1a, p2a = (S[0] - ux * SOFT, S[1] - uy * SOFT), S
    p1b, p2b = E, (S[0] + ux * (L + SOFT), S[1] + uy * (L + SOFT))
    anim = "".join(
        f'<animate attributeName="{a}" from="{f:.2f}" to="{t:.2f}" begin="{start:.2f}s" dur="{dur:.2f}s" fill="freeze"/>'
        for a, f, t in (("x1", p1a[0], p1b[0]), ("y1", p1a[1], p1b[1]), ("x2", p2a[0], p2b[0]), ("y2", p2a[1], p2b[1])))
    defs.append(
        f'<linearGradient id="g_{uid}" gradientUnits="userSpaceOnUse" x1="{p1a[0]:.2f}" y1="{p1a[1]:.2f}" x2="{p2a[0]:.2f}" y2="{p2a[1]:.2f}">'
        f'<stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/>{anim}</linearGradient>'
        f'<mask id="m_{uid}" maskUnits="userSpaceOnUse" x="{bx-4:.2f}" y="{by-4:.2f}" width="{bw+8:.2f}" height="{bh+8:.2f}">'
        f'<rect x="{bx-4:.2f}" y="{by-4:.2f}" width="{bw+8:.2f}" height="{bh+8:.2f}" fill="url(#g_{uid})"/></mask>')
    markup = (f'<g mask="url(#m_{uid})"><image x="{bx:.2f}" y="{by:.2f}" width="{bw:.2f}" height="{bh:.2f}" '
              f'preserveAspectRatio="none" href="data:image/gif;base64,{gif_b64(name)}"/>'
              f'<set attributeName="mask" to="none" begin="{start + dur:.2f}s" fill="freeze"/></g>')
    return markup, arrive

# ================================================================ layout
W, H = 830, 330
S = 99                           # icon size (fixed)
M = 8                            # one box from the borders
NUDGE = 4                        # cancels the emoji glyph's built-in side padding

ROW1 = M
ROW3 = H - M - S
ROW2 = (H - S) // 2

EMO = 32
FAV_TXT = 250
FOC_TXT = 215

FAV_START = M
FAV_END = M + EMO + FAV_TXT
FOC_END = W - M
FOC_START = FOC_END - EMO - FOC_TXT

gap_left = ((FAV_END - FAV_START) - 2 * S) / 3
java_x = FAV_START + gap_left
js_x = java_x + S + gap_left

gap_right = ((FOC_END - FOC_START) - 2 * S) / 3
python_x = FOC_START + gap_right
react_x = python_x + S + gap_right

UP_X = (FAV_START + java_x) / 2
UP_W = (js_x + S + FAV_END) / 2 - UP_X
DOWN_X = (FOC_START + python_x) / 2
DOWN_W = (react_x + S + FOC_END) / 2 - DOWN_X
UP_TOP, UP_BOTTOM = ROW1 + S + 2, ROW3 + 60 - 23 - 3
DOWN_TOP, DOWN_BOTTOM = ROW1 + 60 + 4, ROW3 - 3
UP_H = UP_BOTTOM - UP_TOP
DOWN_H = DOWN_BOTTOM - DOWN_TOP

GH_CX = W / 2
LANE, PAD = 26, 11
JG_X = js_x + S
JG_Y = ROW1
JG_W = (GH_CX + LANE + PAD) - JG_X
JG_H = ROW2 - 1 - ROW1
PG_X = GH_CX - LANE - PAD
PG_Y = ROW2 + S + 2
PG_W = python_x - PG_X
PG_H = ROW3 + S - PG_Y

# ================================================================ the sequence
t0 = EXTRA_DELAY

# 1) digits spread out from the texts: up from "Favourite Stack", down from "Current Focus". All icons are still.
up_markup, up_arrive = reveal("up", "binary_flow_up", (UP_X, UP_TOP, UP_W, UP_H),
                              (UP_X + UP_W / 2, UP_BOTTOM), (UP_X + UP_W / 2, UP_TOP), t0)
down_markup, down_arrive = reveal("down", "binary_flow_down", (DOWN_X, DOWN_TOP, DOWN_W, DOWN_H),
                                  (DOWN_X + DOWN_W / 2, DOWN_TOP), (DOWN_X + DOWN_W / 2, DOWN_BOTTOM), t0)

# 2) the first digits hit the language icons: they turn on slowly
T_JAVA_JS = t0 + up_arrive
T_PYTHON_REACT = t0 + down_arrive
ramp_up = max(prepare_icon("javaIcon")[3], prepare_icon("javascriptIcon")[3])
ramp_down = max(prepare_icon("pythonIcon")[3], prepare_icon("react-nativeIcon")[3])

# 3) once they are fully on, a short pause ("processing"), then digits head for the github icon
RIGHT_START = T_JAVA_JS + ramp_up + PROCESS_DELAY
LEFT_START = T_PYTHON_REACT + ramp_down + PROCESS_DELAY
right_markup, right_arrive = reveal("right", "binary_flow_right", (JG_X, JG_Y, JG_W, JG_H),
                                    (JG_X + 2, ROW1 + S / 2), (GH_CX + LANE, ROW2 - 2), RIGHT_START)
left_markup, left_arrive = reveal("left", "binary_flow_left", (PG_X, PG_Y, PG_W, PG_H),
                                  (python_x - 4, ROW3 + S / 2), (GH_CX - LANE, ROW2 + S + 3), LEFT_START)

# 4) digits have arrived from BOTH sides: the github icon turns on slowly
T_GITHUB = max(RIGHT_START + right_arrive, LEFT_START + left_arrive)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <style>
    .t {{ font: italic 700 32px 'Segoe UI', Arial, sans-serif; fill: #1f2328; }}
    .e {{ font: normal 400 24px 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', sans-serif; }}
    @media (prefers-color-scheme: dark) {{ .t {{ fill: #ffffff; }} }}
  </style>
  <defs>{"".join(defs)}</defs>

  <!-- binary flows (drawn first so they sit behind everything else) -->
  {up_markup}
  {down_markup}
  {right_markup}
  {left_markup}

  <!-- row 1 -->
  {icon("javaIcon", java_x, ROW1, S, T_JAVA_JS)}
  {icon("javascriptIcon", js_x, ROW1, S, T_JAVA_JS)}
  <text class="t" x="{FOC_START}" y="{ROW1 + 60}" textLength="{FOC_TXT}" lengthAdjust="spacing">Current Focus</text>
  <text class="e" x="{FOC_END + NUDGE}" y="{ROW1 + 48}" text-anchor="end">🚀</text>

  <!-- row 2 -->
  {icon("githubIcon", (W - S) / 2, ROW2, S, T_GITHUB)}

  <!-- row 3 -->
  <text class="e" x="{FAV_START - NUDGE}" y="{ROW3 + 68}">💎</text>
  <text class="t" x="{FAV_START + EMO}" y="{ROW3 + 60}" textLength="{FAV_TXT}" lengthAdjust="spacing">Favourite Stack</text>
  {icon("pythonIcon", python_x, ROW3, S, T_PYTHON_REACT)}
  {icon("react-nativeIcon", react_x, ROW3, S, T_PYTHON_REACT)}
</svg>'''

with open("icons/animated/animatedScreen.svg", "w", encoding="utf-8") as f:
    f.write(svg)
