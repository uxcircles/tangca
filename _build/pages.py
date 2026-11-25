"""Build the Tang & Co concept site (dependency: opencc for 简体).

    python3 _build/pages.py && python3 _build/fonts.py

English at /, Traditional Chinese (Hong Kong wording) at /zh/, Simplified at /sc/.
Every string is L(english, traditional[, simplified]). Simplified is converted from the
traditional text with OpenCC (hk2s) unless a third argument overrides it.
"""
import json
import os

try:
    import opencc
    _HK2S = opencc.OpenCC("hk2s")
except ImportError:
    raise SystemExit("pip install opencc-python-reimplemented")

BUILD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD)
V = "2"  # cache-bust: bump on every CSS/JS change
LANG = "en"


def L(en, zh, sc=None):
    if LANG == "en":
        return en
    if LANG == "zh":
        return zh
    if sc is not None:
        return sc
    out = _HK2S.convert(zh)
    for a, b in SC_WORDS:
        out = out.replace(a, b)
    return out


SC_WORDS = [("入息税", "个人所得税"), ("选单", "菜单"), ("私隐", "隐私"), ("电邮", "邮箱"), ("程式", "程序"), ("会计师楼", "会计师事务所"), ("物业", "房产"), ("按揭", "房贷"), ("资讯", "信息"), ("短讯", "短信")]

# ------------------------------------------------------------------ facts (sources in README)
NAME = "Tang &amp; Co"
PHONE = "0131 229 2888"
TEL = "+441312292888"
WA_SHOW = "07544 341837"
WA = "447544341837"
WECHAT = "TangCa2888"
EMAIL = "info@tangca.co.uk"
OFFICIAL = "https://tangca.co.uk/"
UXC = "https://ux-circles.com/professionals"
BASE = "https://uxcircles.github.io/tangca/"
ROUTES = json.load(open(os.path.join(BUILD, "routes.json")))

LANGS = [("en", "", "English", "en-GB"), ("zh", "zh/", "繁體", "zh-Hant-HK"), ("sc", "sc/", "简体", "zh-Hans")]
HTML_LANG = {"en": "en-GB", "zh": "zh-Hant-HK", "sc": "zh-Hans"}

DENG_PATH = open(os.path.join(BUILD, "deng-path.txt")).read().strip()


def deng(cls="deng", label=None):
    """The signature: the brush-written 鄧 (Tang) from the firm's own logo."""
    aria = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true"'
    return f'<svg class="{cls}" viewBox="0 0 1080 1090" {aria}><path fill-rule="evenodd" d="{DENG_PATH}"/></svg>'


def bands_rule(cls="bands-rule"):
    """Second device: the six Scottish income tax bands as a stripe, used as a divider."""
    return f'<div class="{cls}" aria-hidden="true">' + "".join(f"<i class=b{i}></i>" for i in range(1, 7)) + "</div>"


def biz():
    return L("Tang &amp; Co", "鄧氏特許會計師事務所", "邓氏特许会计师事务所")


def edi_addr():
    return L("41 Argyle Place, Edinburgh EH9 1JT", "愛丁堡 Argyle Place 41 號（EH9 1JT）")


def gla_addr():
    return L("14 Newton Terrace, Glasgow G3 7PJ", "格拉斯哥 Newton Terrace 14 號（G3 7PJ）")


def img(prefix, name, w, h, alt, cls="", lazy=True, sizes=None):
    extra = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{prefix}assets/img/{name}.webp" width="{w}" height="{h}" alt="{alt}"{extra}>'


# ------------------------------------------------------------------ shared pieces
def head(prefix, slug, title, desc):
    alts = "".join(
        f'<link rel="alternate" hreflang="{h}" href="{BASE}{d}{slug if slug != "index.html" else ""}">\n'
        for _, d, _, h in LANGS
    )
    zh_pre = ""
    if LANG in ("zh", "sc"):
        s = "tc" if LANG == "zh" else "sc"
        zh_pre = f'<link rel="preload" href="{prefix}assets/fonts/noto-serif-{s}-700.woff2" as="font" type="font/woff2" crossorigin>\n'
    return f'''<!doctype html>
<html lang="{HTML_LANG[LANG]}" class="l-{LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<meta name="description" content="{desc}">
{alts}<link rel="alternate" hreflang="x-default" href="{BASE}{slug if slug != "index.html" else ""}">
<link rel="icon" href="{prefix}assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{prefix}assets/img/apple-touch-icon.png">
<meta name="theme-color" content="#1b2a3f">
<link rel="preload" href="{prefix}assets/fonts/barlow-condensed-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{prefix}assets/fonts/source-sans-3.woff2" as="font" type="font/woff2" crossorigin>
{zh_pre}<link rel="stylesheet" href="{prefix}assets/site.css?v={V}">
<script defer src="{prefix}assets/site.js?v={V}"></script>
</head>
'''


def nav_items():
    return [
        ("services.html", L("Services", "服務")),
        ("about.html", L("People", "團隊")),
        ("index.html#hong-kong", L("New from Hong Kong", "初到英國")),
        ("contact.html", L("Offices", "辦事處")),
    ]


def lang_links(prefix, slug, cls):
    target = "" if slug == "index.html" else slug
    out = []
    for code, d, label, h in LANGS:
        cur = ' aria-current="true"' if code == LANG else ""
        out.append(f'<a href="{prefix}{d}{target}" lang="{h}" hreflang="{h}"{cur}>{label}</a>')
    return f'<div class="{cls}">' + "".join(out) + "</div>"


def concept_bar():
    if LANG == "en":
        return f'''<div class="concept-bar" role="note">
  <div class="concept-inner">
    <p class="concept-text"><span class="concept-tag">Concept</span><span class="concept-long">Redesign concept. Not the <a href="{OFFICIAL}" target="_blank" rel="noopener">official Tang &amp; Co website</a>.</span></p>
    <a class="concept-credit" href="{UXC}" target="_blank" rel="noopener"><span class="concept-by">Designed by </span><strong>UX CIRCLES</strong><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg></a>
  </div>
</div>'''
    if LANG == "zh":
        return f'''<div class="concept-bar" role="note">
  <div class="concept-inner">
    <p class="concept-text"><span class="concept-tag">概念</span><span class="concept-long">概念設計展示，並非<a href="{OFFICIAL}" target="_blank" rel="noopener">鄧氏特許會計師事務所官方網站</a>。</span></p>
    <a class="concept-credit" href="{UXC}" target="_blank" rel="noopener"><span class="concept-by">設計：</span><strong>UX CIRCLES</strong><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg></a>
  </div>
</div>'''
    return f'''<div class="concept-bar" role="note">
  <div class="concept-inner">
    <p class="concept-text"><span class="concept-tag">概念</span><span class="concept-long">概念设计展示，并非<a href="{OFFICIAL}" target="_blank" rel="noopener">邓氏特许会计师事务所官方网站</a>。</span></p>
    <a class="concept-credit" href="{UXC}" target="_blank" rel="noopener"><span class="concept-by">设计：</span><strong>UX CIRCLES</strong><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg></a>
  </div>
</div>'''


def concept_note():
    if LANG == "en":
        return f'<p class="concept-note">Unofficial redesign concept by <a href="{UXC}" target="_blank" rel="noopener">UX CIRCLES</a></p>'
    if LANG == "zh":
        return f'<p class="concept-note">非官方概念設計：<a href="{UXC}" target="_blank" rel="noopener">UX CIRCLES</a></p>'
    return f'<p class="concept-note">非官方概念设计：<a href="{UXC}" target="_blank" rel="noopener">UX CIRCLES</a></p>'


def header(prefix, pg, slug):
    links = "".join(
        f'<a href="{pg}{h}"{" aria-current=page" if h == slug else ""}>{t}</a>' for h, t in nav_items()
    )
    return f'''<body>
<a class="skip" href="#main">{L("Skip to content", "跳至內容")}</a>
{concept_bar()}
<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="{pg}index.html" aria-label="{L("Tang &amp; Co Chartered Accountants, home", "鄧氏特許會計師事務所 主頁")}">
      {deng("brand-mark")}
      <span class="brand-txt"><span class="brand-name">Tang <span class="amp">&amp;</span> Co</span><span class="brand-sub">{L("Chartered Accountants", "特許會計師")}</span></span>
    </a>
    <nav class="nav" aria-label="{L('Main', '主選單')}">{links}</nav>
    {lang_links(prefix, slug, "langs")}
    <a class="head-call" href="tel:{TEL}">{PHONE}</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">{L("Menu", "選單")}</button>
  </div>
  <div class="menu" id="menu" hidden>
    <nav class="wrap" aria-label="{L('Menu', '選單')}">
      {links}
      <a href="tel:{TEL}">{L("Call", "致電")} {PHONE}</a>
      <a href="https://wa.me/{WA}">WhatsApp {WA_SHOW}</a>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      {lang_links(prefix, slug, "menu-langs")}
    </nav>
  </div>
</header>
<main id="main">
'''


def footer(prefix, pg, slug):
    return f'''</main>
<footer class="site-foot">
  {bands_rule()}
  <div class="wrap foot-grid">
    <div class="foot-brand">
      {deng("foot-mark")}
      <p><strong>{L("Tang &amp; Co Chartered Accountants", "鄧氏特許會計師事務所")}</strong><br>{L("Members of ICAS, the Institute of Chartered Accountants of Scotland", "蘇格蘭特許會計師公會（ICAS）會員")}</p>
    </div>
    <div>
      <p><strong>{L("Edinburgh", "愛丁堡")}</strong><br>{edi_addr()}</p>
      <p><strong>{L("Glasgow", "格拉斯哥")}</strong><br>{gla_addr()}</p>
    </div>
    <div>
      <p><a href="tel:{TEL}">{PHONE}</a><br><a href="https://wa.me/{WA}">WhatsApp {WA_SHOW}</a><br>{L("WeChat", "微信")} {WECHAT}<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div class="foot-links">
      <a href="{pg}services.html">{L("Services", "服務")}</a>
      <a href="{pg}about.html">{L("People", "團隊")}</a>
      <a href="{pg}contact.html">{L("Offices &amp; booking", "辦事處及預約")}</a>
      <a href="{pg}privacy.html">{L("Privacy notice", "私隱聲明")}</a>
      {lang_links(prefix, slug, "foot-langs")}
    </div>
  </div>
  <div class="wrap foot-end">
    <p>{L("Tax figures on this site are estimates for 2026/27 and are not advice.", "本網站的稅務數字為 2026/27 年度估算，並非稅務建議。")}</p>
    {concept_note()}
  </div>
</footer>
<nav class="mbar" aria-label="{L('Quick actions', '快捷操作')}">
  <a href="tel:{TEL}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2"/></svg>{L("Call", "致電")}</a>
  <a href="https://wa.me/{WA}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 21l1.6-4.7A8.5 8.5 0 1 1 7.8 19.5Z"/></svg>WhatsApp</a>
  <a href="{pg}contact.html#book"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>{L("Book", "預約")}</a>
</nav>
</body>
</html>
'''


# ------------------------------------------------------------------ tax tool
BAND_NAMES = lambda: [
    L("Starter", "起始稅率", "起始税率"),
    L("Basic", "基本稅率", "基本税率"),
    L("Intermediate", "中級稅率", "中间税率"),
    L("Higher", "較高稅率", "高税率"),
    L("Advanced", "進階稅率", "进阶税率"),
    L("Top", "最高稅率", "最高税率"),
]


def tax_tool(prefix, compact=True):
    names = BAND_NAMES()
    rates = [19, 20, 21, 42, 45, 48]
    segs = "".join(
        f'<li class="seg b{i+1}" data-band="{i}"><span class="seg-rate">{r}%</span><span class="seg-name">{names[i]}</span></li>'
        for i, r in enumerate(rates)
    )
    strings = {
        "band": L("Top band", "最高稅級", "最高税档"),
        "tax": L("Tax a year", "每年稅款", "每年税款"),
        "vs": L("vs rest of UK", "相比英格蘭", "相比英格兰"),
        "more": L("more", "多繳", "多缴"),
        "less": L("less", "少繳", "少缴"),
        "same": L("about the same", "差不多", "差不多"),
        "none": L("Below the personal allowance: no income tax", "低於個人免稅額，無須繳入息稅", "低于个人免税额，无需缴纳个人所得税"),
        "names": names,
    }
    return f'''<form class="taxtool" id="taxtool" onsubmit="return false" aria-describedby="tt-note">
  <div class="tt-row">
    <label for="tt-pay">{L("Salary before tax", "稅前年薪", "税前年薪")}</label>
    <div class="tt-input"><span aria-hidden="true">£</span><input id="tt-pay" inputmode="numeric" autocomplete="off" value="38,000" aria-describedby="tt-note"></div>
  </div>
  <ol class="tt-bands" aria-label="{L("Scottish income tax bands 2026/27", "2026/27 年度蘇格蘭入息稅稅級", "2026/27 年度苏格兰个人所得税税档")}">{segs}</ol>
  <output class="tt-out" for="tt-pay" aria-live="polite">
    <span class="tt-k"><span class="tt-l">{strings["band"]}</span> <b id="tt-band">—</b></span>
    <span class="tt-k"><span class="tt-l">{strings["tax"]}</span> <b id="tt-tax">—</b></span>
    <span class="tt-k"><span class="tt-l">{strings["vs"]}</span> <b id="tt-vs">—</b></span>
  </output>
  <script type="application/json" id="tt-strings">{json.dumps(strings, ensure_ascii=False)}</script>
</form>'''


# ------------------------------------------------------------------ map
def office_map(prefix):
    data = {
        "mark": prefix + "assets/img/pin.svg",
        "offices": {
            "edinburgh": {
                "home": ROUTES["edinburgh"]["home"],
                "label": L("Tang &amp; Co · Argyle Place", "鄧氏 · Argyle Place"),
                "routes": [{"name": L("Edinburgh Waverley", "Waverley 火車站", "Waverley 火车站"), "short": "Waverley", "min": r["min"], "start": r["start"], "coords": r["coords"]} for r in ROUTES["edinburgh"]["routes"].values()],
            },
            "glasgow": {
                "home": ROUTES["glasgow"]["home"],
                "label": L("Tang &amp; Co · Newton Terrace", "鄧氏 · Newton Terrace"),
                "routes": [{"name": L("Charing Cross station", "Charing Cross 火車站", "Charing Cross 火车站"), "short": "Charing Cross", "min": r["min"], "start": r["start"], "coords": r["coords"]} for r in ROUTES["glasgow"]["routes"].values()],
            },
        },
    }
    e = ROUTES["edinburgh"]["routes"]["Edinburgh Waverley"]["min"]
    g = ROUTES["glasgow"]["routes"]["Charing Cross"]["min"]
    return f'''<div class="office-tabs" role="tablist" aria-label="{L("Choose an office", "選擇辦事處")}">
  <button type="button" role="tab" aria-selected="true" data-office="edinburgh">{L("Edinburgh", "愛丁堡")}</button>
  <button type="button" role="tab" aria-selected="false" data-office="glasgow">{L("Glasgow", "格拉斯哥")}</button>
</div>
<div class="map" data-map>
  <img class="map-fallback" src="{prefix}assets/img/map-sketch.svg" alt="{L("Sketch map of the Edinburgh office on Argyle Place, beside the Meadows", "簡圖：愛丁堡辦事處位於 Argyle Place，毗鄰 The Meadows 公園")}" width="800" height="560" loading="lazy">
</div>
<script type="application/json" id="map-data">{json.dumps(data, ensure_ascii=False)}</script>
<div class="offices">
  <div class="office">
    <h3>{L("Edinburgh", "愛丁堡")}</h3>
    <p>{edi_addr()}</p>
    <p class="walk"><strong>{e} {L("min", "分鐘")}</strong> {L("walk from Edinburgh Waverley, or two minutes from the Meadows", "由 Waverley 火車站步行前往；距 The Meadows 公園只需兩分鐘", "由 Waverley 火车站步行前往；距 The Meadows 公园只需两分钟")}</p>
  </div>
  <div class="office">
    <h3>{L("Glasgow", "格拉斯哥")}</h3>
    <p>{gla_addr()}</p>
    <p class="walk"><strong>{g} {L("min", "分鐘")}</strong> {L("walk from Charing Cross station", "由 Charing Cross 火車站步行前往", "由 Charing Cross 火车站步行前往")}</p>
  </div>
</div>'''


def booking_form():
    svc = [s[1] for s in SERVICES()]
    return f'''<form class="book" id="book-form" novalidate>
  <div class="f-row">
    <label for="f-name">{L("Your name", "姓名")}</label>
    <input id="f-name" name="name" autocomplete="name" required>
  </div>
  <div class="f-row">
    <label for="f-phone">{L("Phone", "電話")}</label>
    <input id="f-phone" name="phone" type="tel" autocomplete="tel" required>
  </div>
  <div class="f-row">
    <label for="f-topic">{L("What do you need?", "需要甚麼服務？", "需要什么服务？")}</label>
    <select id="f-topic" name="topic">{"".join(f"<option>{n}</option>" for n in svc)}<option>{L("Not sure yet", "未確定", "还不确定")}</option></select>
  </div>
  <div class="f-row">
    <label for="f-office">{L("Office", "辦事處")}</label>
    <select id="f-office" name="office"><option>{L("Edinburgh", "愛丁堡")}</option><option>{L("Glasgow", "格拉斯哥")}</option><option>{L("Phone or video call", "電話或視像會議", "电话或视频会议")}</option></select>
  </div>
  <div class="f-row f-wide">
    <label for="f-msg">{L("Anything we should know (optional)", "補充資料（可選）", "补充信息（可选）")}</label>
    <textarea id="f-msg" name="msg" rows="3"></textarea>
  </div>
  <p class="f-err" id="f-err" role="alert" hidden>{L("Please add your name and a phone number.", "請填寫姓名及電話號碼。")}</p>
  <div class="f-actions">
    <button class="btn btn-ink" type="submit" data-via="wa">{L("Send by WhatsApp", "以 WhatsApp 發送")}</button>
    <button class="btn btn-line" type="submit" data-via="mail">{L("Send by email", "以電郵發送")}</button>
  </div>
  <p class="f-note"><small>{L("Your message opens in WhatsApp or your email app. Nothing is stored on this website.", "訊息會在 WhatsApp 或電郵程式開啟，本網站不會儲存任何資料。", "信息会在 WhatsApp 或邮件应用中打开，本网站不会保存任何资料。")}</small></p>
  <script type="application/json" id="f-strings">{json.dumps({"to": EMAIL, "wa": WA, "subject": L("Appointment request", "預約查詢", "预约查询"), "name": L("Name", "姓名"), "phone": L("Phone", "電話"), "topic": L("Service", "服務"), "office": L("Office", "辦事處"), "msg": L("Notes", "補充")}, ensure_ascii=False)}</script>
</form>'''


# ------------------------------------------------------------------ content
def SERVICES():
    """(id, title, one line). From tangca.co.uk service pages and the Chinese home page."""
    return [
        ("accounting", L("Accounts &amp; payroll", "會計及薪俸", "会计及工资"),
         L("Bookkeeping, VAT records under Making Tax Digital, payroll, management and annual accounts.",
           "簿記、按「數碼稅務」(MTD) 保存增值稅記錄、薪俸、管理賬目及年度賬目。",
           "簿记、按“数字税务”(MTD) 保存增值税记录、工资、管理账目及年度账目。")),
        ("self-assessment", L("Self-assessment", "個人報稅", "个人报税"),
         L("Self-employed, a director, or rental and investment income: we file it and tell you what is due, and when.",
           "自僱、公司董事，或有租金及投資收入：我們代你報稅，並說明應繳多少、何時繳交。",
           "自雇、公司董事，或有租金及投资收入：我们代您报税，并说明应缴多少、何时缴纳。")),
        ("tax", L("Tax compliance", "稅務合規", "税务合规"),
         L("PAYE, VAT, CIS, corporation tax, capital gains and inheritance tax, and HMRC enquiries.",
           "PAYE、增值稅、建築業計劃 (CIS)、公司稅、資本增值稅、遺產稅，以及 HMRC 查詢。",
           "PAYE、增值税、建筑业计划 (CIS)、公司税、资本利得税、遗产税，以及 HMRC 查询。")),
        ("secretarial", L("Company secretarial", "公司秘書", "公司秘书"),
         L("Forming the company, keeping director and shareholder records, and Companies House filings.",
           "成立公司、保存董事及股東記錄，以及向公司註冊處 (Companies House) 提交文件。",
           "成立公司、保存董事及股东记录，以及向公司注册处 (Companies House) 提交文件。")),
        ("advisory", L("Business advice", "商業顧問", "商业顾问"),
         L("Starting up, cash-flow forecasts, checking your accounting system, and planning for growth.",
           "開業、現金流預測、檢查會計系統，以及擴展計劃。",
           "开业、现金流预测、检查会计系统，以及扩张计划。")),
        ("hong-kong", L("New from Hong Kong", "初到英國", "初到英国"),
         L("BN(O) and Asian clients: income from home, a UK home or buy-to-let, and starting a business here.",
           "BN(O) 及亞洲客戶：海外收入、在英國置業或買樓收租，以及在英國創業。",
           "BN(O) 及亚洲客户：海外收入、在英国置业或买房出租，以及在英国创业。")),
    ]


QUOTES = lambda: [
    ("Mark and Charlotte are so professional and personable that I never worry about a trip to the accountants.", L("Client review, tangca.co.uk", "客戶評價，tangca.co.uk")),
    ("…a brilliant service, with a really knowledgeable and friendly team of accountants…", "ANP Edinburgh"),
    ("…not treated as a number but as a person…", "Locanda de Gusti, Pizzeria 1926 &amp; Wine &amp; Peach"),
]


# ------------------------------------------------------------------ pages
def page_index(prefix, pg):
    S = SERVICES()
    cards = "".join(
        f'<li><a href="{pg}services.html#{i}"><h3>{t}</h3><p>{d}</p></a></li>' for i, t, d in S
    )
    quotes = "".join(
        f'<figure class="quote"><blockquote lang="en"><p>{q}</p></blockquote><figcaption>{w}</figcaption></figure>' for q, w in QUOTES()
    )
    e = ROUTES["edinburgh"]["routes"]["Edinburgh Waverley"]["min"]
    g = ROUTES["glasgow"]["routes"]["Charing Cross"]["min"]
    return f'''
<section class="hero">
  {img(prefix, "argyle-corner", 1600, 1000, L("The sandstone tenement at 40 to 43 Argyle Place, Marchmont, home of the Edinburgh office", "Marchmont 區 Argyle Place 40 至 43 號的砂岩公寓大樓，愛丁堡辦事處所在", "Marchmont 区 Argyle Place 40 至 43 号的砂岩公寓大楼，爱丁堡办事处所在"), "hero-photo", lazy=False)}
  <div class="wrap hero-in">
    <h1>{L("<span class=nb>Scotland has six income tax bands</span> <span class=nb>Which one are you in?</span>", "蘇格蘭入息稅分六級<br>你屬於哪一級？", "苏格兰个人所得税分六档<br>您在哪一档？")}</h1>
    <p class="hero-sub">{L("Try a salary. ICAS chartered accountants.", "輸入年薪，即時試算。", "输入年薪，即时试算。")}</p>
    {tax_tool(prefix)}
    <div class="hero-act">
      <a class="btn btn-paper" href="tel:{TEL}">{L("Call", "致電")} {PHONE}</a>
      <a class="btn btn-ghost" href="{pg}contact.html#book">{L("Book a free chat", "預約免費初次會面", "预约免费初次会面")}</a>
    </div>
  </div>
</section>

<section class="svc wrap" aria-labelledby="svc-h">
  <div class="svc-head">
    <h2 id="svc-h">{L("Six things we do, from one office by the Meadows", "六項服務，同一間會計師樓", "六项服务，同一家会计师事务所")}</h2>
    <a class="more" href="{pg}services.html">{L("All services", "全部服務")} →</a>
  </div>
  <div class="svc-grid">
    {img(prefix, "calculator", 1000, 1250, L("A calculator on a grey desk", "灰色桌面上的計算機"), "svc-photo")}
    <ul class="cards">{cards}</ul>
  </div>
</section>

<figure class="band-photo">
  {img(prefix, "meadows-blossom-wide", 1600, 685, L("Cherry blossom over a path on the Meadows, two minutes from the Edinburgh office", "The Meadows 公園的櫻花小徑，距愛丁堡辦事處兩分鐘", "The Meadows 公园的樱花小径，距爱丁堡办事处两分钟"))}
  <figcaption class="wrap"><small>{L("The Meadows in spring. Our door is two minutes south.", "春天的 The Meadows 公園，往南走兩分鐘就到。", "春天的 The Meadows 公园，往南走两分钟就到。")}</small></figcaption>
</figure>

<section class="recs wrap" aria-labelledby="recs-h">
  <div class="recs-num">
    <p class="big" aria-hidden="true">98%</p>
    <h2 id="recs-h">{L("of our new clients come through a personal recommendation", "新客戶有超過 98% 由親友介紹而來", "新客户有超过 98% 由亲友介绍而来")}</h2>
    <a class="more" href="{pg}about.html#clients">{L("What clients say", "客戶怎樣說", "客户怎么说")} →</a>
  </div>
  <div class="recs-q">{quotes}</div>
</section>

<section class="founders" aria-labelledby="fo-h">
  <div class="wrap fo-grid">
    <div class="fo-photo">
      {img(prefix, "argyle-bw", 768, 301, L("The Argyle Place office from the street, in black and white", "Argyle Place 辦事處街景（黑白照片）"))}
      {deng("fo-mark")}
    </div>
    <div class="fo-txt">
      <h2 id="fo-h">{L("Mark and Charlotte Tang", "鄧氏夫婦：Mark 與 Charlotte", "邓氏夫妇：Mark 与 Charlotte")}</h2>
      <p>{L("Mark qualified as a chartered accountant in 1996, trained in Edinburgh and worked with the Big Four in Malaysia and London. Charlotte lectured at a business school and knows the restaurant trade from the inside.",
            "Mark 於 1996 年取得特許會計師資格，在愛丁堡受訓，其後在馬來西亞及倫敦的四大會計師行工作。Charlotte 曾任商學院講師，對餐飲業瞭如指掌。",
            "Mark 于 1996 年取得特许会计师资格，在爱丁堡受训，其后在马来西亚及伦敦的四大会计师事务所工作。Charlotte 曾任商学院讲师，对餐饮业了如指掌。")}</p>
      <p>{L("Both give their time to the Edinburgh Chinese Community School, where Mark has been treasurer for about twenty years.",
            "兩人亦為愛丁堡中文學校義務服務，Mark 擔任司庫約二十年。",
            "两人亦为爱丁堡中文学校义务服务，Mark 担任司库约二十年。")}</p>
      <a class="more" href="{pg}about.html">{L("Meet the team of twelve", "認識十二人團隊", "认识十二人团队")} →</a>
    </div>
  </div>
</section>

<section class="hk wrap" id="hong-kong" aria-labelledby="hk-h">
  {img(prefix, "paperwork", 1000, 1249, L("A client filling in forms at a kitchen table", "客戶在餐桌上填寫表格"), "hk-photo")}
  <div class="hk-txt">
    <h2 id="hk-h">{L("New to Scotland from Hong Kong", "從香港移居蘇格蘭", "从香港移居苏格兰")}</h2>
    <p>{L("Rent from a flat in Kowloon, a pension at home, a first home in Edinburgh: we sort out what the UK taxes, and what it doesn't.",
          "九龍的物業租金、香港的強積金、在愛丁堡置業：哪些要在英國報稅、哪些不用，我們替你理清。",
          "九龙的房产租金、香港的强积金、在爱丁堡置业：哪些要在英国报税、哪些不用，我们替您理清。")}</p>
    <ul class="ticks">
      <li>{L("Income and gains from outside the UK, under the 4-year rule that replaced the remittance basis in April 2025", "英國境外收入及增值：2025 年 4 月起以「四年規則」取代匯入制", "英国境外收入及增值：2025 年 4 月起以“四年规则”取代汇入制")}</li>
      <li>{L("Buying a home or a buy-to-let flat", "自住置業或買樓收租", "自住置业或买房出租")}</li>
      <li>{L("Self-employed or starting a company", "自僱或開設公司", "自雇或开设公司")}</li>
      <li>{L("Capital gains and inheritance tax", "資本增值稅及遺產稅", "资本利得税及遗产税")}</li>
    </ul>
    <p class="contact-line">WhatsApp <a href="https://wa.me/{WA}">{WA_SHOW}</a> · {L("WeChat", "微信")} <span class="mono">{WECHAT}</span></p>
  </div>
</section>

<section class="where" aria-labelledby="where-h">
  <div class="wrap">
    <h2 id="where-h">{L("Marchmont and Newton Terrace", "愛丁堡 Marchmont 與格拉斯哥 Newton Terrace")}</h2>
  </div>
  <ul class="strip" aria-label="{L("Around the Edinburgh office", "愛丁堡辦事處周邊")}">
    <li>{img(prefix, "argyle-4043", 800, 800, L("40 to 43 Argyle Place, the office building", "Argyle Place 40 至 43 號，辦事處所在大樓"))}</li>
    <li>{img(prefix, "argyle-street", 1200, 799, L("Argyle Place looking towards the Meadows", "Argyle Place 街景，遠望 The Meadows 公園", "Argyle Place 街景，远望 The Meadows 公园"))}</li>
    <li>{img(prefix, "marchmont-crescent", 800, 800, L("Tenements on Marchmont Crescent", "Marchmont Crescent 的砂岩公寓"))}</li>
    <li>{img(prefix, "meadows-jawbone-sq", 800, 800, L("The whale-jawbone arch on Jawbone Walk, the Meadows", "The Meadows 公園 Jawbone Walk 的鯨骨拱門", "The Meadows 公园 Jawbone Walk 的鲸骨拱门"))}</li>
  </ul>
  <div class="wrap where-grid">
    <a class="addr" href="{pg}contact.html#map">
      <h3>{L("Edinburgh", "愛丁堡")}</h3><p>{edi_addr()}</p><p class="walk">{e} {L("min walk from Waverley", "分鐘由 Waverley 步行", "分钟由 Waverley 步行")}</p>
    </a>
    <a class="addr" href="{pg}contact.html#map">
      <h3>{L("Glasgow", "格拉斯哥")}</h3><p>{gla_addr()}</p><p class="walk">{g} {L("min walk from Charing Cross", "分鐘由 Charing Cross 步行", "分钟由 Charing Cross 步行")}</p>
    </a>
  </div>
</section>

<section class="cta">
  {deng("cta-mark")}
  <div class="wrap cta-in">
    <h2>{L("Tell us what's on your desk", "有甚麼文件，拿來給我們看", "有什么文件，拿来给我们看")}</h2>
    <div class="cta-acts">
      <a class="btn btn-paper" href="tel:{TEL}">{L("Call", "致電")} {PHONE}</a>
      <a class="btn btn-ghost" href="https://wa.me/{WA}">WhatsApp</a>
      <a class="btn btn-ghost" href="{pg}contact.html#book">{L("Book online", "網上預約", "在线预约")}</a>
    </div>
  </div>
</section>
'''


def page_services(prefix, pg):
    detail = {
        "accounting": [L("Book-keeping", "簿記"), L("VAT records and Making Tax Digital", "增值稅記錄及數碼稅務 (MTD)", "增值税记录及数字税务 (MTD)"), L("Payroll", "薪俸", "工资"), L("Periodic management accounts", "定期管理賬目", "定期管理账目"), L("Annual accounts", "年度賬目", "年度账目")],
        "self-assessment": [L("Self-employed professionals and sole traders", "自僱專業人士及獨資經營者", "自雇专业人士及个体经营者"), L("Company directors", "公司董事"), L("Rental property income", "物業租金收入", "房产租金收入"), L("Investment income and capital gains", "投資收入及資本增值", "投资收入及资本利得"), L("Your tax bill and its due dates, in advance", "預先告訴你稅額及繳稅日期", "预先告诉您税额及缴税日期")],
        "tax": [L("PAYE, National Insurance and auto-enrolment", "PAYE、國民保險及自動加入退休金計劃", "PAYE、国民保险及自动加入养老金计划"), L("VAT returns and VAT schemes", "增值稅申報及增值稅計劃", "增值税申报及增值税计划"), L("Construction Industry Scheme", "建築業計劃 (CIS)", "建筑业计划 (CIS)"), L("Personal, corporation and property tax returns", "個人、公司及物業稅表", "个人、公司及房产税表"), L("HMRC enquiries and investigations", "HMRC 查詢及調查", "HMRC 查询及调查"), L("Capital gains and inheritance tax", "資本增值稅及遺產稅", "资本利得税及遗产税")],
        "secretarial": [L("Forming a limited company", "成立有限公司"), L("Director and shareholder records", "董事及股東記錄", "董事及股东记录"), L("Confirmation statements to Companies House", "向公司註冊處提交確認聲明", "向公司注册处提交确认声明"), L("Filing accounts on time", "按時提交賬目", "按时提交账目")],
        "advisory": [L("Business start-up", "開業支援", "开业支持"), L("Cash-flow projections", "現金流預測", "现金流预测"), L("Monitoring financial performance", "監察財務表現", "监察财务表现"), L("Accounting system health check", "會計系統檢查", "会计系统检查"), L("Future capital requirements", "未來資金需要", "未来资金需求")],
        "hong-kong": [L("Foreign income and gains, including the 4-year regime from April 2025", "海外收入及增值，包括 2025 年 4 月起的四年規則", "海外收入及增值，包括 2025 年 4 月起的四年规则"), L("Tax residence", "稅務居民身份", "税务居民身份"), L("Buying a home or a buy-to-let", "自住置業或買樓收租", "自住置业或买房出租"), L("Self-employment or an investment portfolio", "自僱收入或投資組合", "自雇收入或投资组合"), L("Starting a business in the UK", "在英國創業", "在英国创业"), L("Capital gains and inheritance tax", "資本增值稅及遺產稅", "资本利得税及遗产税")],
    }
    photos = {"accounting": ("calculator", 1000, 1250, L("A calculator", "計算機", "计算器")), "hong-kong": ("paperwork", 1000, 1249, L("Filling in forms", "填寫表格"))}
    blocks = []
    for i, t, d in SERVICES():
        lis = "".join(f"<li>{x}</li>" for x in detail[i])
        ph = ""
        if i in photos:
            n, w, h, a = photos[i]
            ph = img(prefix, n, w, h, a, "sv-photo")
        blocks.append(f'<section class="sv{" sv-has" if ph else ""}" id="{i}"><div class="sv-txt"><h2>{t}</h2><p>{d}</p><ul class="ticks">{lis}</ul></div>{ph}</section>')
    rows = [
        (L("Personal allowance", "個人免稅額", "个人免税额"), "£0 – £12,570", "0%"),
        (BAND_NAMES()[0], "£12,571 – £16,537", "19%"),
        (BAND_NAMES()[1], "£16,538 – £29,526", "20%"),
        (BAND_NAMES()[2], "£29,527 – £43,662", "21%"),
        (BAND_NAMES()[3], "£43,663 – £75,000", "42%"),
        (BAND_NAMES()[4], "£75,001 – £125,140", "45%"),
        (BAND_NAMES()[5], L("over £125,140", "£125,140 以上"), "48%"),
    ]
    trs = "".join(f'<tr><th scope="row"><i class="sw b{k}"></i>{a}</th><td>{b}</td><td>{c}</td></tr>' for k, (a, b, c) in enumerate(rows))
    return f'''
<section class="page-head wrap">
  <h1>{L("Services", "服務範圍", "服务范围")}</h1>
  <p class="lead">{L("We agree what you need, then give you a quote before any work starts.", "先了解你的需要，開始工作前提供報價。", "先了解您的需要，开始工作前提供报价。")}</p>
  <nav class="jump" aria-label="{L("On this page", "本頁內容")}">{"".join(f'<a href="#{i}">{t}</a>' for i, t, _ in SERVICES())}<a href="#scottish-rates">{L("Scottish rates", "蘇格蘭稅率", "苏格兰税率")}</a></nav>
</section>
<div class="wrap sv-list">{"".join(blocks)}</div>
<section class="rates wrap" id="scottish-rates" aria-labelledby="rates-h">
  <h2 id="rates-h">{L("Scottish income tax 2026/27", "2026/27 年度蘇格蘭入息稅", "2026/27 年度苏格兰个人所得税")}</h2>
  <p>{L("For earnings, pensions and rental income if you live in Scotland. Savings and dividends use UK rates. The personal allowance shrinks by £1 for every £2 earned over £100,000.",
        "適用於居於蘇格蘭人士的工作收入、退休金及租金收入；儲蓄利息及股息按全英稅率計算。收入超過 £100,000 後，每多賺 £2，個人免稅額減少 £1。",
        "适用于居住在苏格兰人士的工作收入、养老金及租金收入；储蓄利息及股息按全英税率计算。收入超过 £100,000 后，每多赚 £2，个人免税额减少 £1。")}</p>
  <table class="rate-table"><thead><tr><th scope="col">{L("Band", "稅級", "税档")}</th><th scope="col">{L("Income", "收入")}</th><th scope="col">{L("Rate", "稅率", "税率")}</th></tr></thead><tbody>{trs}</tbody></table>
  <p class="src">{L('Source: <a href="https://www.gov.uk/scottish-income-tax" target="_blank" rel="noopener">GOV.UK, Income Tax in Scotland</a>. An estimate, not advice.', '資料來源：<a href="https://www.gov.uk/scottish-income-tax" target="_blank" rel="noopener">GOV.UK「Income Tax in Scotland」</a>。僅供估算，並非稅務建議。', '资料来源：<a href="https://www.gov.uk/scottish-income-tax" target="_blank" rel="noopener">GOV.UK“Income Tax in Scotland”</a>。仅供估算，并非税务建议。')}</p>
  <div class="tool-card">{tax_tool(prefix)}</div>
</section>
<section class="cta cta-slim"><div class="wrap cta-in"><h2>{L("Not sure which service you need?", "不確定需要哪項服務？", "不确定需要哪项服务？")}</h2><div class="cta-acts"><a class="btn btn-paper" href="tel:{TEL}">{L("Call", "致電")} {PHONE}</a><a class="btn btn-ghost" href="{pg}contact.html#book">{L("Book a free first chat", "預約免費初次會面", "预约免费初次会面")}</a></div></div></section>
'''


TEAM = lambda: [
    ("Mark Tang", L("Founder · Chartered Accountant (ICAS)", "創辦人．特許會計師（ICAS）", "创办人．特许会计师（ICAS）")),
    ("Charlotte Tang", L("Founder", "創辦人", "创办人")),
    ("Ken Chew", "CPA"), ("Natalie Mook", "CPA"), ("Jinky Ho", "CPA"),
    ("Alvin Ho", L("ACCA, part qualified", "ACCA（部分合格）")), ("Dominic Tang", L("ACCA, part qualified", "ACCA（部分合格）")),
    ("Nigel Goh", L("Accountant", "會計師", "会计师")), ("Jomi Wong", L("Accountant", "會計師", "会计师")),
    ("Winnie Kwok", L("Support", "行政支援", "行政支持")), ("Howard Kwan", L("Support", "行政支援", "行政支持")), ("Kelly Ho", L("Team", "團隊成員", "团队成员")),
]

CLIENTS = ["AGG Builders Ltd", "Grainee Morton", "ANP Edinburgh", "KAM Artistry Company Limited", "Allo Energy", "Burgess Adams Architects", "Diva Thy Ltd", "Links Aerospace Ltd", "Locanda de Gusti", "Pizzeria 1926", "Wine &amp; Peach", "Linda Chan-Malcolm", "Baixing Limited", "Clary Sage Ltd"]


def page_about(prefix, pg):
    team = "".join(
        f'<li><span class="ini" aria-hidden="true">{n.split()[0][0]}{n.split()[-1][0]}</span><span><strong>{n}</strong><br>{r}</span></li>' for n, r in TEAM()
    )
    quotes = "".join(
        f'<figure class="quote"><blockquote lang="en"><p>{q}</p></blockquote><figcaption>{w}</figcaption></figure>' for q, w in QUOTES()
    )
    more = [
        ("…efficient, reliable, and extremely helpful.", "Grainee Morton"),
        ("…we continued to appreciate their professionalism…", "Allo Energy"),
        ("Would highly recommend!", "Baixing Limited"),
    ]
    quotes += "".join(f'<figure class="quote"><blockquote lang="en"><p>{q}</p></blockquote><figcaption>{w}</figcaption></figure>' for q, w in more)
    return f'''
<section class="page-head wrap">
  <h1>{L("Twelve people, two founders, one name on the door", "十二人團隊，由鄧氏夫婦創立", "十二人团队，由邓氏夫妇创立")}</h1>
</section>
<section class="wrap about-grid">
  <div class="about-photo">{img(prefix, "argyle-corner-tall", 900, 1125, L("The Argyle Place tenement corner", "Argyle Place 街角大樓"), "")}</div>
  <div class="about-txt">
    <h2>Mark Tang</h2>
    <p>{L("Qualified as a chartered accountant in 1996 after training in Edinburgh, then worked with the Big Four in Malaysia and in London, including on a PLC. A member of ICAS. Treasurer of the Edinburgh Chinese Community School for about twenty years.",
          "1996 年在愛丁堡受訓後取得特許會計師資格，其後在馬來西亞及倫敦的四大會計師行工作，包括上市公司項目。ICAS 會員，擔任愛丁堡中文學校司庫約二十年。",
          "1996 年在爱丁堡受训后取得特许会计师资格，其后在马来西亚及伦敦的四大会计师事务所工作，包括上市公司项目。ICAS 会员，担任爱丁堡中文学校司库约二十年。")}</p>
    <h2>Charlotte Tang</h2>
    <p>{L("A former business-school lecturer with years in the catering trade. Many of her clients run food businesses, and many come from ethnic-minority communities. She also volunteers at the Edinburgh Chinese Community School.",
          "曾任商學院講師，亦有多年餐飲業經驗。她的客戶不少經營餐飲生意，亦有很多來自少數族裔社群。她同樣在愛丁堡中文學校擔任義工。",
          "曾任商学院讲师，亦有多年餐饮业经验。她的客户不少经营餐饮生意，也有很多来自少数族裔社群。她同样在爱丁堡中文学校担任志愿者。")}</p>
  </div>
</section>
{bands_rule("bands-rule wrap")}
<section class="wrap team" aria-labelledby="team-h">
  <h2 id="team-h">{L("The team", "團隊成員", "团队成员")}</h2>
  <ul class="team-list">{team}</ul>
</section>
<section class="wrap clients" id="clients" aria-labelledby="cl-h">
  <h2 id="cl-h">{L("In clients' words", "客戶的話", "客户的话")}</h2>
  <div class="recs-q recs-q3">{quotes}</div>
  <p class="cl-list"><strong>{L("Reviews on tangca.co.uk from:", "tangca.co.uk 上的評價來自：", "tangca.co.uk 上的评价来自：")}</strong> {", ".join(CLIENTS)}</p>
</section>
<figure class="band-photo">
  {img(prefix, "meadows-blossom-wide", 1600, 685, L("Cherry blossom on the Meadows", "The Meadows 公園的櫻花", "The Meadows 公园的樱花"))}
</figure>
'''


def page_contact(prefix, pg):
    return f'''
<section class="page-head wrap">
  <h1>{L("Come to Argyle Place, or Newton Terrace", "到 Argyle Place 或 Newton Terrace 找我們", "到 Argyle Place 或 Newton Terrace 找我们")}</h1>
  <p class="lead">{L("Call before you visit so the right person is in.", "到訪前請先致電，確保負責同事在辦公室。", "到访前请先致电，确保负责同事在办公室。")}</p>
</section>
<section class="wrap contact-grid">
  <div class="c-ways">
    <a class="way" href="tel:{TEL}"><span>{L("Phone", "電話")}</span><strong>{PHONE}</strong></a>
    <a class="way" href="https://wa.me/{WA}"><span>WhatsApp</span><strong>{WA_SHOW}</strong></a>
    <div class="way"><span>{L("WeChat", "微信")}</span><strong class="mono">{WECHAT}</strong></div>
    <a class="way" href="mailto:{EMAIL}"><span>{L("Email", "電郵")}</span><strong>{EMAIL}</strong></a>
  </div>
  {img(prefix, "argyle-street", 1200, 799, L("Argyle Place, Marchmont", "Marchmont 區 Argyle Place"), "c-photo")}
</section>
<section class="wrap map-sec" id="map" aria-labelledby="map-h">
  <h2 id="map-h">{L("Find us", "如何前往")}</h2>
  {office_map(prefix)}
</section>
<section class="wrap book-sec" id="book" aria-labelledby="book-h">
  <h2 id="book-h">{L("Book a first chat", "預約初次會面", "预约初次会面")}</h2>
  <p>{L("The first conversation is free. Tell us a little and we'll call you back.", "初次會面免費。留下簡單資料，我們會回電。", "初次会面免费。留下简单资料，我们会回电。")}</p>
  {booking_form()}
</section>
<link rel="stylesheet" href="{prefix}assets/vendor/maplibre/maplibre-gl.css" media="print" onload="this.media='all'">
<script defer src="{prefix}assets/map.js?v={V}"></script>
'''


def page_privacy(prefix, pg):
    P = lambda en, zh, sc=None: f"<p>{L(en, zh, sc)}</p>"
    return f'''
<section class="page-head wrap"><h1>{L("Privacy notice", "私隱聲明", "隐私声明")}</h1>
<p class="lead">{L("Draft for Tang &amp; Co to review. It replaces a 2022 notice that still contains template brackets.", "供鄧氏審閱的草稿，用以取代仍留有範本括號的 2022 年版本。", "供邓氏审阅的草稿，用以取代仍留有模板括号的 2022 年版本。")}</p></section>
<div class="wrap prose">
<h2>{L("Who we are", "我們是誰", "我们是谁")}</h2>
{P("Tang &amp; Co Chartered Accountants, 41 Argyle Place, Edinburgh EH9 1JT, is the controller of the personal information we hold about you. Contact Mrs Charlotte Tang at info@tangca.co.uk or 0131 229 2888.", "鄧氏特許會計師事務所（地址：愛丁堡 Argyle Place 41 號，EH9 1JT）是你個人資料的控制者。如有查詢，請聯絡 Charlotte Tang 女士：info@tangca.co.uk 或 0131 229 2888。", "邓氏特许会计师事务所（地址：爱丁堡 Argyle Place 41 号，EH9 1JT）是您个人资料的控制者。如有查询，请联系 Charlotte Tang 女士：info@tangca.co.uk 或 0131 229 2888。")}
<h2>{L("What we use and why", "我們使用哪些資料及原因", "我们使用哪些资料及原因")}</h2>
{P("Your contact details, identity documents, financial records and tax information, to provide accounting and tax services under our engagement letter, to meet anti-money-laundering rules, and to deal with HMRC and Companies House for you.", "你的聯絡資料、身份證明文件、財務記錄及稅務資料，用於按委聘書提供會計及稅務服務、遵守反洗錢規定，以及代你與 HMRC 和公司註冊處聯絡。", "您的联系资料、身份证明文件、财务记录及税务资料，用于按委托书提供会计及税务服务、遵守反洗钱规定，以及代您与 HMRC 和公司注册处联络。")}
<h2>{L("How long we keep it", "保存期限", "保存期限")}</h2>
{P("Normally six years after our work for you ends, longer where the law requires.", "一般在服務結束後保存六年；法律另有規定者除外。", "一般在服务结束后保存六年；法律另有规定者除外。")}
<h2>{L("Your rights", "你的權利", "您的权利")}</h2>
{P("You can ask for a copy of your information, ask us to correct or delete it, object to its use, or ask us to stop direct marketing at any time. If you are unhappy, you can complain to the Information Commissioner's Office (ico.org.uk, 0303 123 1113).", "你可隨時要求索取個人資料副本、更正或刪除資料、反對資料被使用，或要求停止直接推廣。如有不滿，可向資訊專員辦公室 (ICO) 投訴（ico.org.uk，0303 123 1113）。", "您可随时要求获取个人资料副本、更正或删除资料、反对资料被使用，或要求停止直接营销。如有不满，可向信息专员办公室 (ICO) 投诉（ico.org.uk，0303 123 1113）。")}
<h2>{L("This website", "本網站", "本网站")}</h2>
{P("This concept site sets no cookies and stores nothing you type. The booking form opens WhatsApp or your email app.", "本概念網站不設 Cookie，亦不儲存你輸入的任何內容。預約表格會開啟 WhatsApp 或電郵程式。", "本概念网站不设 Cookie，也不保存您输入的任何内容。预约表格会打开 WhatsApp 或邮件应用。")}
<h2 id="photos">{L("Photo credits", "相片來源", "图片来源")}</h2>
<ul class="credits">
<li>Argyle Place (40–43), Marchmont Crescent: Dogwoodfire, <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener">CC BY-SA 4.0</a>, Wikimedia Commons</li>
<li>Argyle Place street: Richard Webb, <a href="https://creativecommons.org/licenses/by-sa/2.0/" target="_blank" rel="noopener">CC BY-SA 2.0</a>, geograph.org.uk</li>
<li>Jawbone Walk: Stephen Elwyn Roddick, <a href="https://creativecommons.org/licenses/by-sa/2.0/" target="_blank" rel="noopener">CC BY-SA 2.0</a>, geograph.org.uk</li>
<li>The Meadows cherry blossom: BenTanXiaoMing, <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener">CC BY-SA 4.0</a>, Wikimedia Commons</li>
<li>{L("Office in black and white, calculator, paperwork: tangca.co.uk", "黑白辦事處照片、計算機、文件：tangca.co.uk", "黑白办事处照片、计算器、文件：tangca.co.uk")}</li>
</ul>
</div>
'''


def page_404(prefix, pg):
    return f'''
<section class="nf wrap">
  {deng("nf-mark")}
  <h1>Page not found<span lang="zh-Hant"> · 找不到頁面</span></h1>
  <p><a class="btn btn-ink" href="{pg}index.html">Home</a> <a class="btn btn-line" href="{pg}zh/index.html" lang="zh-Hant">中文主頁</a></p>
</section>
'''


PAGES = [
    ("index.html", page_index, lambda: L("Tang &amp; Co Chartered Accountants, Edinburgh and Glasgow", "鄧氏特許會計師事務所｜愛丁堡及格拉斯哥", "邓氏特许会计师事务所｜爱丁堡及格拉斯哥"),
     lambda: L("ICAS chartered accountants on Argyle Place, Edinburgh, and Newton Terrace, Glasgow. Accounts, payroll, self-assessment, tax and advice for newcomers from Hong Kong.", "愛丁堡及格拉斯哥的 ICAS 特許會計師：會計、薪俸、個人報稅、稅務及初到英國人士的稅務諮詢。")),
    ("services.html", page_services, lambda: L("Services · Tang &amp; Co", "服務範圍｜鄧氏特許會計師事務所", "服务范围｜邓氏特许会计师事务所"),
     lambda: L("Accounts, payroll, self-assessment, tax compliance, company secretarial and business advice, plus Scottish income tax rates for 2026/27.", "會計、薪俸、個人報稅、稅務合規、公司秘書及商業顧問，以及 2026/27 年度蘇格蘭入息稅稅率。")),
    ("about.html", page_about, lambda: L("People · Tang &amp; Co", "團隊｜鄧氏特許會計師事務所", "团队｜邓氏特许会计师事务所"),
     lambda: L("Mark and Charlotte Tang and the team at Tang &amp; Co, and what clients say.", "鄧氏夫婦及團隊介紹，以及客戶評價。")),
    ("contact.html", page_contact, lambda: L("Offices &amp; booking · Tang &amp; Co", "辦事處及預約｜鄧氏特許會計師事務所", "办事处及预约｜邓氏特许会计师事务所"),
     lambda: L("Visit Tang &amp; Co at 41 Argyle Place, Edinburgh, or 14 Newton Terrace, Glasgow. Phone 0131 229 2888.", "愛丁堡 Argyle Place 41 號或格拉斯哥 Newton Terrace 14 號。電話 0131 229 2888。")),
    ("privacy.html", page_privacy, lambda: L("Privacy notice · Tang &amp; Co", "私隱聲明｜鄧氏特許會計師事務所", "隐私声明｜邓氏特许会计师事务所"),
     lambda: L("How Tang &amp; Co uses personal information.", "鄧氏如何使用個人資料。")),
]


def build():
    global LANG
    for code, d, _, _ in LANGS:
        LANG = code
        prefix = "../" if d else ""
        pg = ""
        for slug, fn, title, desc in PAGES:
            html = head(prefix, slug, title(), desc()) + header(prefix, pg, slug) + fn(prefix, pg) + footer(prefix, pg, slug)
            path = os.path.join(ROOT, d, slug)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w", encoding="utf-8").write(html)
            print("wrote", d + slug)
    LANG = "en"
    html = head("/tangca/", "404.html", "Page not found · Tang &amp; Co", "Page not found").replace('href="/tangca/assets', 'href="/tangca/assets') + header("/tangca/", "/tangca/", "404.html") + page_404("/tangca/", "/tangca/") + footer("/tangca/", "/tangca/", "404.html")
    open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(html)
    open(os.path.join(ROOT, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")
    print("wrote 404.html, robots.txt")


if __name__ == "__main__":
    build()
