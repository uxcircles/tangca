"""Self-hosted web fonts. Run after editing Chinese text:

    python3 _build/pages.py && python3 _build/fonts.py

- Barlow Condensed 600, Source Sans 3 (variable 200-900): Google's Latin subset
- Noto Serif TC/SC 700, Noto Sans TC/SC 400/700: only the characters used on the site
"""
import glob, html, os, re, urllib.parse, urllib.request

BUILD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD)
OUT = os.path.join(ROOT, "assets", "fonts")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
API = "https://fonts.googleapis.com/css2?"


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA})).read()


def latin_src(css):
    for comment, block in re.findall(r"/\* ([\w-]+) \*/\s*@font-face \{(.*?)\}", css, re.S):
        if comment == "latin":
            return re.search(r"url\((.*?)\)", block).group(1)
    raise SystemExit("latin block not found")


def save(name, data):
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, name + ".woff2"), "wb").write(data)
    print(f"{name}.woff2  {len(data) // 1024} KB")


def cjk(folder):
    chars = set()
    files = glob.glob(os.path.join(ROOT, folder, "*.html")) + [os.path.join(ROOT, "assets", "site.js")]
    for f in files:
        chars.update(ch for ch in html.unescape(open(f, encoding="utf-8").read()) if ord(ch) > 0x2E7F)
    chars.update("，。：；！？（）「」、·…“”")
    return "".join(sorted(chars))


def subset(family, w, text, name):
    css = get(API + f"family={family}:wght@{w}&display=swap&text=" + urllib.parse.quote(text)).decode()
    save(name, get(re.search(r"url\((.*?)\)", css).group(1)))


if __name__ == "__main__":
    save("barlow-condensed-600", get(latin_src(get(API + "family=Barlow+Condensed:wght@600&display=swap").decode())))
    save("source-sans-3", get(latin_src(get(API + "family=Source+Sans+3:wght@200..900&display=swap").decode())))
    for code, folder in (("tc", "zh"), ("sc", "sc")):
        text = cjk(folder)
        subset(f"Noto+Serif+{code.upper()}", 700, text, f"noto-serif-{code}-700")
        for w in (400, 700):
            subset(f"Noto+Sans+{code.upper()}", w, text, f"noto-sans-{code}-{w}")
        print(code, len(text), "characters")
