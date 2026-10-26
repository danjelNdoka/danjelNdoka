import base64

def b64(name):
    with open(f"icons/animated/{name}.gif", "rb") as f:
        return base64.b64encode(f.read()).decode()

def img(name, x, y, s=99):
    return f'<image x="{x}" y="{y}" width="{s}" height="{s}" href="data:image/gif;base64,{b64(name)}"/>'

W, H = 830, 330
S = 99          # icon size
ROW1, ROW2, ROW3 = 0, 115, 230   # top y of each row

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <style>
    text {{ font: italic 700 38px 'Segoe UI', Arial, sans-serif; fill: #1f2328; }}
    @media (prefers-color-scheme: dark) {{ text {{ fill: #ffffff; }} }}
  </style>

  <!-- row 1: java + js on the left, title on the right -->
  {img("javaIcon", 0, ROW1)}
  {img("javascriptIcon", 110, ROW1)}
  <text x="{W}" y="{ROW1 + 65}" text-anchor="end">Current Focus 🚀</text>

  <!-- row 2: github icon centered -->
  {img("githubIcon", (W - S) // 2, ROW2)}

  <!-- row 3: title on the left, python + react on the right -->
  <text x="0" y="{ROW3 + 65}">💎 Favourite Stack</text>
  {img("pythonIcon", W - 209, ROW3)}
  {img("react-nativeIcon", W - S, ROW3)}
</svg>'''

with open("icons/animatedScreen.svg", "w", encoding="utf-8") as f:
    f.write(svg)
