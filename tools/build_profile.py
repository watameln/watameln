import base64
import io
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SOURCE = "https://snow-leopard.dev/campfire-banner.png"


def load_background() -> Image.Image:
    request = urllib.request.Request(SOURCE, headers={"User-Agent": "githubtest-slop-profile-builder/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read()
    return Image.open(io.BytesIO(data)).convert("RGB")


def image_data_uri(image: Image.Image, size: tuple[int, int], quality: int = 80) -> str:
    fitted = ImageOps.fit(image, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    output = io.BytesIO()
    fitted.save(output, format="JPEG", quality=quality, optimize=True, progressive=True)
    encoded = base64.b64encode(output.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


def build_hero(background: Image.Image) -> str:
    image = image_data_uri(background, (1100, 610), 82)
    return f'''<svg width="1100" height="610" viewBox="0 0 1100 610" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="horizontal" x1="0" y1="0" x2="1100" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#140d0b" stop-opacity="0.70"/>
      <stop offset="0.52" stop-color="#140d0b" stop-opacity="0.46"/>
      <stop offset="1" stop-color="#140d0b" stop-opacity="0.24"/>
    </linearGradient>
    <linearGradient id="vertical" x1="0" y1="610" x2="0" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#100b0a" stop-opacity="0.62"/>
      <stop offset="0.48" stop-color="#100b0a" stop-opacity="0"/>
      <stop offset="1" stop-color="#100b0a" stop-opacity="0.36"/>
    </linearGradient>
    <style>
      .mono {{ font-family: 'Cascadia Code','SFMono-Regular',Consolas,monospace; }}
      .sans {{ font-family: Inter,ui-sans-serif,system-ui,-apple-system,sans-serif; }}
      .in1 {{ animation: enter .65s ease-out both; }}
      .in2 {{ animation: enter .65s .10s ease-out both; }}
      .in3 {{ animation: enter .65s .20s ease-out both; }}
      @keyframes enter {{ from {{ opacity:0; transform:translateY(9px); }} to {{ opacity:1; transform:translateY(0); }} }}
    </style>
  </defs>

  <image href="{image}" x="0" y="0" width="1100" height="610"/>
  <rect width="1100" height="610" fill="url(#horizontal)"/>
  <rect width="1100" height="610" fill="url(#vertical)"/>

  <g class="mono in1">
    <text x="48" y="40" fill="#f5e8d8" font-size="12" font-weight="650">snow-leopard.dev</text>
    <line x1="48" y1="68" x2="1052" y2="68" stroke="#e5b260" stroke-opacity="0.28"/>
    <text x="1052" y="40" text-anchor="end" fill="#a69684" font-size="10">GITHUB / WATAMELN</text>
  </g>

  <g class="in2">
    <text x="48" y="193" class="mono" fill="#efb75f" font-size="12" font-weight="650" letter-spacing="1.1">ROBLOX DEVELOPMENT — CYBERSECURITY — SOFTWARE DEVELOPMENT</text>
    <text x="44" y="292" class="sans" fill="#f8f0e6" font-size="78" font-weight="760" letter-spacing="-3.4">Hey, I'm</text>
    <text x="44" y="382" class="sans" fill="#f0b45a" font-size="82" font-weight="800" letter-spacing="-4.2">watameln</text>
  </g>

  <g class="in3 sans">
    <text x="48" y="445" fill="#d3c9bd" font-size="17">I'm a Roblox scripter and cybersecurity professional. I've been scripting on Roblox</text>
    <text x="48" y="474" fill="#d3c9bd" font-size="17">since 2018, and I also work on software, security, and other projects outside the platform.</text>
  </g>
</svg>'''


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    background = load_background()
    (ASSETS / "hero.svg").write_text(build_hero(background), encoding="utf-8")


if __name__ == "__main__":
    main()
