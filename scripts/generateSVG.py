import base64

def b64(name):
    with open(f"icons/animated/{name}.gif", "rb") as f:
        return base64.b64encode(f.read()).decode()

def img(name, x, y, s=99):
    return f'<image x="{x:.2f}" y="{y}" width="{s}" height="{s}" href="data:image/gif;base64,{b64(name)}"/>'

def flow(name, x, y, w, h):
    # binary flow gifs are stretched to an exact box
    return (f'<image x="{x:.2f}" y="{y}" width="{w:.2f}" height="{h}" '
            f'preserveAspectRatio="none" href="data:image/gif;base64,{b64(name)}"/>')

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

# left group: 💎 + "Favourite Stack"
FAV_START = M
FAV_END = M + EMO + FAV_TXT

# right group: "Current Focus" + 🚀
FOC_END = W - M
FOC_START = FOC_END - EMO - FOC_TXT

# equal gaps: group start -> icon 1 -> icon 2 -> group end (3 gaps)
gap_left = ((FAV_END - FAV_START) - 2 * S) / 3
java_x = FAV_START + gap_left
js_x = java_x + S + gap_left

gap_right = ((FOC_END - FOC_START) - 2 * S) / 3
python_x = FOC_START + gap_right
react_x = python_x + S + gap_right

# binary flows: horizontally from the middle of the first gap to the middle of the last gap
UP_X = (FAV_START + java_x) / 2
UP_W = (js_x + S + FAV_END) / 2 - UP_X
DOWN_X = (FOC_START + python_x) / 2
DOWN_W = (react_x + S + FOC_END) / 2 - DOWN_X

# vertically: up flow runs from just above "Favourite Stack" to just under the row-1 icons,
# down flow runs from just under "Current Focus" to just above the row-3 icons
UP_TOP, UP_BOTTOM = ROW1 + S + 2, ROW3 + 60 - 23 - 3
DOWN_TOP, DOWN_BOTTOM = ROW1 + 60 + 4, ROW3 - 3
UP_H = UP_BOTTOM - UP_TOP
DOWN_H = DOWN_BOTTOM - DOWN_TOP

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <style>
    .t {{ font: italic 700 32px 'Segoe UI', Arial, sans-serif; fill: #1f2328; }}
    .e {{ font: normal 400 24px 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', sans-serif; }}
    @media (prefers-color-scheme: dark) {{ .t {{ fill: #ffffff; }} }}
  </style>

  <!-- binary flows (drawn first so they sit behind everything) -->
  {flow("binary_flow_up", UP_X, UP_TOP, UP_W, UP_H)}
  {flow("binary_flow_down", DOWN_X, DOWN_TOP, DOWN_W, DOWN_H)}

  <!-- row 1 -->
  {img("javaIcon", java_x, ROW1)}
  {img("javascriptIcon", js_x, ROW1)}
  <text class="t" x="{FOC_START}" y="{ROW1 + 60}" textLength="{FOC_TXT}" lengthAdjust="spacing">Current Focus</text>
  <text class="e" x="{FOC_END + NUDGE}" y="{ROW1 + 48}" text-anchor="end">🚀</text>

  <!-- row 2 -->
  {img("githubIcon", (W - S) / 2, ROW2)}

  <!-- row 3 -->
  <text class="e" x="{FAV_START - NUDGE}" y="{ROW3 + 68}">💎</text>
  <text class="t" x="{FAV_START + EMO}" y="{ROW3 + 60}" textLength="{FAV_TXT}" lengthAdjust="spacing">Favourite Stack</text>
  {img("pythonIcon", python_x, ROW3)}
  {img("react-nativeIcon", react_x, ROW3)}
</svg>'''

with open("icons/animated/animatedScreen.svg", "w", encoding="utf-8") as f:
    f.write(svg)