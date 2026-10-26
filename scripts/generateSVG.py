import base64

def b64(name):
    with open(f"icons/animated/{name}.gif", "rb") as f:
        return base64.b64encode(f.read()).decode()

def img(name, x, y, s=99):
    return f'<image x="{x}" y="{y}" width="{s}" height="{s}" href="data:image/gif;base64,{b64(name)}"/>'

W, H = 830, 330
S = 99                           # icon size (fixed)
ROW1, ROW2, ROW3 = 0, 115, 230   # top y of each row
M = 1                            # 1px space from the borders

EMO = 30                         # width reserved for each emoji
FAV_TXT = 250                    # exact width of "Favourite Stack" at 32px
FOC_TXT = 215                    # exact width of "Current Focus" at 32px

# left group: 💎 + "Favourite Stack"
FAV_START = M
FAV_END = M + EMO + FAV_TXT

# right group: "Current Focus" + 🚀
FOC_START = W - M - EMO - FOC_TXT
FOC_END = W - M

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <style>
    .t {{ font: italic 700 32px 'Segoe UI', Arial, sans-serif; fill: #1f2328; }}
    .e {{ font: normal 400 24px 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', sans-serif; }}
    @media (prefers-color-scheme: dark) {{ .t {{ fill: #ffffff; }} }}
  </style>

  <!-- row 1: java starts at the 💎, js ends at the end of "Stack"; title on the right -->
  {img("javaIcon", FAV_START, ROW1)}
  {img("javascriptIcon", FAV_END - S, ROW1)}
  <text class="t" x="{FOC_START}" y="{ROW1 + 60}" textLength="{FOC_TXT}" lengthAdjust="spacing">Current Focus</text>
  <text class="e" x="{FOC_END - EMO + 2}" y="{ROW1 + 48}">🚀</text>

  <!-- row 2: github icon centered -->
  {img("githubIcon", (W - S) // 2, ROW2)}

  <!-- row 3: title on the left; python starts at "Current Focus", react ends at the 🚀 -->
  <text class="e" x="{FAV_START}" y="{ROW3 + 68}">💎</text>
  <text class="t" x="{FAV_START + EMO}" y="{ROW3 + 60}" textLength="{FAV_TXT}" lengthAdjust="spacing">Favourite Stack</text>
  {img("pythonIcon", FOC_START, ROW3)}
  {img("react-nativeIcon", FOC_END - S, ROW3)}
</svg>'''

with open("icons/animated/animatedScreen.svg", "w", encoding="utf-8") as f:
    f.write(svg)