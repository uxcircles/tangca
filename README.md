# Tang & Co Chartered Accountants：網站重新設計概念

UX CIRCLES 為鄧氏特許會計師事務所（Tang & Co，愛丁堡及格拉斯哥）製作的**非官方**改版概念網站。所有頁面都設了 `noindex`，`robots.txt` 禁止搜尋引擎收錄，頁頂和頁尾都標明這是概念設計，並附上官方網站連結（https://tangca.co.uk/）。

- 英文：`/`
- 繁體中文（香港用語）：`/zh/`
- 簡體中文：`/sc/`

## 頁面

| 檔案 | 內容 |
| --- | --- |
| `index.html` | 首頁：蘇格蘭入息稅六級計算器、六項服務、98% 推薦、創辦人、初到英國、兩間辦事處 |
| `services.html` | 六項服務的細項，以及 2026/27 年度蘇格蘭稅率表和計算器 |
| `about.html` | Mark 及 Charlotte Tang、十二人團隊、客戶評價 |
| `contact.html` | 聯絡方式、兩間辦事處地圖（含步行路線）、預約表格（經 WhatsApp 或電郵送出） |
| `privacy.html` | 私隱聲明草稿和相片來源 |
| `404.html` | 找不到頁面 |

## 如何修改

所有文字都寫在 `_build/pages.py`，格式是 `L(英文, 繁體[, 簡體])`。簡體版用 OpenCC（hk2s）由繁體自動轉換，需要時可以加第三個參數覆寫。

```bash
pip install opencc-python-reimplemented
python3 _build/pages.py      # 產生全部 HTML
python3 _build/fonts.py      # 改了中文字後要重新子集化字體
```

改了 CSS 或 JS，要把 `pages.py` 裡的 `V` 加 1，避免手機繼續用舊的快取。

## 設計概念

- **標誌元素：** logo 上的毛筆「鄧」字。我把它向量化（`_build/deng-path.txt`），用在頁首、favicon、地圖圖釘、創辦人照片、頁尾、行動呼籲區塊和 404 頁。
- **第二個元素：** 蘇格蘭入息稅的六個稅級，畫成由砂岩色漸變到墨藍的色帶。這條色帶就是首頁的計算器，也用作分隔線和清單符號。
- **首屏類型：** `tool-first`。客戶上門時通常帶著一個問題。很多由香港或英格蘭搬來的人都不知道，蘇格蘭的入息稅有六級，英格蘭只有三級。計算器即時顯示你的最高稅級、全年稅款，以及和英國其他地區的差額。背景是 Argyle Place 40–43 號的實景照片。
- **標題：** "Scotland has six income tax bands / Which one are you in?"、「蘇格蘭入息稅分六級／你屬於哪一級？」
- **字體：** 標題用 Barlow Condensed，呼應 logo 上的窄體英文字；內文用 Source Sans 3（17 px）；中文標題用 Noto Serif TC/SC，中文內文用 Noto Sans TC/SC。
- **配色：** logo 的墨藍（#1b2a3f），配愛丁堡砂岩色和石灰色底（#efede8）。
- **與同類網站的分別：** 最近四個會計師網站（KY、Tan & Co、IQTi、William Lai）都是左文右圖或資料卡，配色以米色加藍色為主。這個網站用全幅實景照片加工具，不用拱形圖片，也不用浮動標籤。`similarity_check.py` 結果：PASS。

## 需要鄧氏確認的資料

- **辦公時間：** 原網站沒有列出，所以聯絡頁寫「到訪前請先致電」。
- **服務語言：** 原網站只說 Charlotte 有「rare multilingual skills」。這版沒有寫明廣東話或普通話，只提供中文頁面，以及 WhatsApp 和微信聯絡方式。
- **「初次會面免費」：** 根據原中文首頁的「免费预约」寫成，需要確認。
- **98% 由推薦而來：** 原網站首頁的說法。
- **客戶評價：** 只節錄 tangca.co.uk 上已公開的評價，名稱照原文。
- **公司秘書服務：** 原英文頁的內容誤抄了會計服務的項目。這版改用原中文首頁列出的內容（成立公司、董事及股東記錄、周年申報）。
- **BNO 頁面：** 原頁面仍提到 remittance basis / domicile。這個制度已在 2025 年 4 月 6 日改為「四年海外收入及增值（FIG）」制度，這版已按新制度改寫。
- **入息稅數字：** 2026/27 年度蘇格蘭稅率，起始稅率 £12,571–16,537，基本稅率至 £29,526，中級稅率至 £43,662，較高稅率至 £75,000，進階稅率至 £125,140。來源是 GOV.UK 和 gov.scot 的 Scottish Rate Resolution。計算器只計算工資、退休金和租金收入，不包括國民保險，並標明「僅供估算，並非稅務建議」。
- **私隱聲明：** 這是草稿，需要鄧氏審閱。原版日期為 2022 年 6 月 10 日，仍留有範本方括號。

## 圖片來源

| 檔案 | 來源 | 授權 | 是否鄧氏自己的照片 |
| --- | --- | --- | --- |
| `argyle-corner.webp`、`argyle-corner-tall.webp` | [Edinburgh, 40-43 Argyle Place](https://commons.wikimedia.org/wiki/File:Edinburgh,_40-43_Argyle_Place_-_20170917162217.jpg)，Dogwoodfire | CC BY-SA 4.0 | 否（大樓實景） |
| `argyle-4043.webp` | [Edinburgh, 40-43 Argyle Place](https://commons.wikimedia.org/wiki/File:Edinburgh,_40-43_Argyle_Place_-_20170917162222.jpg)，Dogwoodfire | CC BY-SA 4.0 | 否 |
| `argyle-street.webp` | [Argyle Place, geograph 8289639](https://commons.wikimedia.org/wiki/File:Argyle_Place_-_geograph.org.uk_-_8289639.jpg)，Richard Webb | CC BY-SA 2.0 | 否 |
| `marchmont-crescent.webp` | [Marchmont Crescent](https://commons.wikimedia.org/wiki/File:Edinburgh,_92,_94,_96,_98,_100,_102,_104_Marchmont_Crescent_-_20170917163325.jpg)，Dogwoodfire | CC BY-SA 4.0 | 否 |
| `meadows-jawbone-sq.webp` | [Jawbone Walk, The Meadows](https://commons.wikimedia.org/wiki/File:Jawbone_Walk,_The_Meadows_-_geograph.org.uk_-_3270514.jpg)，Stephen Elwyn Roddick | CC BY-SA 2.0 | 否 |
| `meadows-blossom-wide.webp` | [The Meadows Cherry Blossoms 02](https://commons.wikimedia.org/wiki/File:The_Meadows_Cherry_Blossoms_02.jpg)，BenTanXiaoMing | CC BY-SA 4.0 | 否 |
| `argyle-bw.webp` | tangca.co.uk（building2.jpg） | 鄧氏網站 | 是 |
| `calculator.webp` | tangca.co.uk（原為 Unsplash，Annie Spratt） | 鄧氏網站 / Unsplash | 是（網站原有圖片） |
| `paperwork.webp` | tangca.co.uk（原為 Unsplash，Marissa Grootes） | 鄧氏網站 / Unsplash | 是（網站原有圖片） |
| 毛筆「鄧」字 | 由 tangca.co.uk 的 logo.png 向量化 | 鄧氏 logo | 是 |

所有相片的作者和授權都列在私隱聲明頁的「相片來源」部分。

## 地圖

使用 MapLibre GL JS（`assets/vendor/maplibre/`，BSD 授權）和 OpenFreeMap 地圖。步行路線取自 routing.openstreetmap.de，並預先寫進 `_build/routes.json`：Waverley 火車站到愛丁堡辦事處 1.7 公里，約 21 分鐘；Charing Cross 火車站到格拉斯哥辦事處 560 米，約 7 分鐘。

設計：UX CIRCLES（https://ux-circles.com/professionals）
