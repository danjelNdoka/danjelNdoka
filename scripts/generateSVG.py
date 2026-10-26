import base64

def b64(name):
    with open(f"icons/animated/{name}.gif", "rb") as f:
        return base64.b64encode(f.read()).decode()

def img(name, x, y, s=99):
    return f'<image x="{x}" y="{y}" width="{s}" height="{s}" href="data:image/gif;base64,{b64(name)}"/>'

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

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <style>
    .t {{ font: italic 700 32px 'Segoe UI', Arial, sans-serif; fill: #1f2328; }}
    .e {{ font: normal 400 24px 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', sans-serif; }}
    @media (prefers-color-scheme: dark) {{ .t {{ fill: #ffffff; }} }}
  </style>

  <!-- row 1 -->
  {img("javaIcon", FAV_START, ROW1)}
  {img("javascriptIcon", FAV_END - S, ROW1)}
  <text class="t" x="{FOC_START}" y="{ROW1 + 60}" textLength="{FOC_TXT}" lengthAdjust="spacing">Current Focus</text>
  <text class="e" x="{FOC_END + NUDGE}" y="{ROW1 + 48}" text-anchor="end">🚀</text>

  <!-- row 2 -->
  {img("githubIcon", (W - S) // 2, ROW2)}

  <!-- row 3 -->
  <text class="e" x="{FAV_START - NUDGE}" y="{ROW3 + 68}">💎</text>
  <text class="t" x="{FAV_START + EMO}" y="{ROW3 + 60}" textLength="{FAV_TXT}" lengthAdjust="spacing">Favourite Stack</text>
  {img("pythonIcon", FOC_START, ROW3)}
  {img("react-nativeIcon", FOC_END - S, ROW3)}
</svg>'''

with open("icons/animated/animatedScreen.svg", "w", encoding="utf-8") as f:
    f.write(svg)