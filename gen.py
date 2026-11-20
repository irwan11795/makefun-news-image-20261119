# gen.py — draws entry.png for news-image-20261119 (Thursday 19 November 2026).
# PIL only, no network, fully deterministic. Run: python3 gen.py
# Writes entry.png (1024x1024, RGB) next to this file and preview-300.png.
#
# Layout v2 — modern magazine / editorial (replaces the v1 front-page
# newspaper layout at the user's request):
#   slim kicker + big sans masthead, region-counts line, ONE hero story
#   (story 1, big drawn diagram left, headline right), a 12-story
#   "story river" in 2 columns (numbered, kicker + headline on one line,
#   summary below), a MARKETS strip, a DATE CHECK box sized to fit its
#   wrapped text, and the 42-item ALSO list in 2 columns with a region
#   colour dot per item. 55 stories total.
#
# Same facts as v1 — same 55 stories, same numbers, same sources. Only
# the layout changed, plus two v1 fixes: (1) no clipped story labels —
# every kicker+headline line is measured and asserted to fit its cell;
# (2) the DATE CHECK box height is computed from its wrapped lines, so
# its last line can never be clipped by the frame.

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (255, 255, 255)
INK = (17, 17, 17)
RED = (185, 28, 28)
GREY = (90, 90, 90)
LIGHT = (242, 242, 242)
RULE = (17, 17, 17)

_HERE = Path(__file__).resolve().parent


def _font(name, size):
    """Load a bundled font (fonts/ next to this file) or the system copy."""
    for base in (_HERE / "fonts",
                 Path("/usr/share/fonts/truetype/dejavu")):
        p = base / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    raise SystemExit(f"font not found: {name}")


KICK = _font("DejaVuSans-Bold.ttf", 12)
TITLE = _font("DejaVuSans-Bold.ttf", 32)
REGION_LINE = _font("DejaVuSans-Bold.ttf", 12)
TICK = _font("DejaVuSans-Bold.ttf", 11)
HERO_KICK = _font("DejaVuSans-Bold.ttf", 13)
HERO_HEAD = _font("DejaVuSans-Bold.ttf", 24)
HERO_SUMM = _font("DejaVuSans.ttf", 12)
SECT = _font("DejaVuSans-Bold.ttf", 16)
FLOW_NUM = _font("DejaVuSans-Bold.ttf", 18)
FLOW_KICK = _font("DejaVuSans-Bold.ttf", 11)
FLOW_HEAD = _font("DejaVuSans-Bold.ttf", 13)
FLOW_SUMM = _font("DejaVuSans.ttf", 12)
MKT_LABEL = _font("DejaVuSans-Bold.ttf", 12)
MKT_TXT = _font("DejaVuSans.ttf", 11)
DATE_HEAD = _font("DejaVuSans-Bold.ttf", 13)
DATE_TXT = _font("DejaVuSans.ttf", 12)
ALSO_NUM = _font("DejaVuSans-Bold.ttf", 13)
ALSO_TXT = _font("DejaVuSans.ttf", 13)
FOOT = _font("DejaVuSans.ttf", 10)
CAP = _font("DejaVuSans.ttf", 10)

# (number, region, tag, headline, summary) — all stories happened or were
# first reported on Thursday 19 November 2026; wording is the author's own.
LEADS = [
    (1, "WORLD", "WORLD · SUMMIT",
     "Trump, Xi and Putin sign a 'peace declaration'",
     "First-ever three-way summit in Shenzhen ends with a pledge "
     "against nuclear war."),
    (2, "WORLD", "WORLD · JUSTICE",
     "World court: Myanmar committed genocide",
     "Myanmar's military acted with genocidal intent against the "
     "Rohingya. 9–6."),
    (3, "AMERICAS", "AMERICAS · MARKETS",
     "Anthropic debuts above $2 trillion",
     "Shares open at $111.50, up 34% on the $83 price, in the biggest "
     "IPO ever."),
]

GRID = [
    (4, "MIDDLE EAST", "MIDDLE EAST · IRAN WAR",
     "Houthi missile hits Riyadh tower",
     "Houthis strike the PIF Tower; Tehran hits ships in Hormuz and a "
     "US base."),
    (5, "AMERICAS", "AMERICAS · MARKETS",
     "Dow plunges 1,100 points",
     "S&P 500 falls 2.0% for a sixth straight loss; Nasdaq drops 2.25%."),
    (6, "MIDDLE EAST", "MIDDLE EAST · GAZA",
     "Aid groups score Gaza plan 4 out of 26",
     "Five agencies say the peace plan is falling short; new evacuation "
     "orders."),
    (7, "EUROPE", "EUROPE · UKRAINE",
     "Kyiv hits Crimean Bridge a third time",
     "Rail traffic halts after the strike; Macron urges NATO membership "
     "talks."),
    (8, "AMERICAS", "AMERICAS · GAMES",
     "GTA VI goes on sale worldwide",
     "Rockstar's blockbuster launches on PlayStation 5 and Xbox; "
     "Take-Two −3.7%."),
    (9, "WORLD", "WORLD · CHILDREN",
     "589m children lived in war zones",
     "Save the Children counts 23.4% of children near recorded violence "
     "in 2025."),
    (10, "WORLD", "WORLD · CLIMATE",
     "COP31 cuts fossil fuels from draft deal",
     "Outcry in Antalya as the draft deal drops fossil fuels; talks run "
     "to 20 Nov."),
    (11, "AMERICAS", "AMERICAS · AI",
     "OpenAI ships GPT-6.2 Astra and Sol",
     "New models land as Nvidia stops selling H200 chips in China."),
    (12, "AMERICAS", "AMERICAS · CONGRESS",
     "Senate rejects Iran war-powers bill",
     "The 51–48 vote leaves the war unchecked; three Republicans backed "
     "it."),
    (13, "OCEANIA", "OCEANIA · CRICKET",
     "England win ODI series in Hobart",
     "Duckett's 133 seals a 97-run win over Australia; the series ends "
     "2–1."),
]

# ALSO list: one short line each (number + text), kept under 40 chars so
# each fits a single 13px line in its column.
ALSO = [
    (14, "AMERICAS", "Trump: \"see what happens\" on Iran"),
    (15, "AMERICAS", "Trump blames Vance, NYT reports"),
    (16, "ASIA", "Takaichi, Putin agree to keep talking"),
    (17, "OCEANIA", "Rio Tinto pledges $250m mine fund"),
    (18, "ASIA", "APEC adopts trade, data, AI outlook"),
    (19, "ASIA", "Ramayana passes ₹1,500 crore"),
    (20, "ASIA", "Indonesia passes asset bill"),
    (21, "AMERICAS", "Raye leads Grammy nods with 11"),
    (22, "ASIA", "Typhoons intensify after heatwaves"),
    (23, "EUROPE", "UK, Norway fund £100m naval craft"),
    (24, "AMERICAS", "Rockstar names GTA VI voice cast"),
    (25, "AMERICAS", "Students sue over Doritos AI alert"),
    (26, "WORLD", "Visa, Mastercard, JPMorgan data leak"),
    (27, "WORLD", "USDS stablecoin shrinks 35%"),
    (28, "AMERICAS", "Bitcoin ETF holdings hit record"),
    (29, "ASIA", "Japan inflation accelerates"),
    (30, "AMERICAS", "Goolsbee open to bigger rate hikes"),
    (31, "AMERICAS", "$500bn Nvidia pledge, $0 delivered"),
    (32, "OCEANIA", "Australia jobless 4.9%, most since '21"),
    (33, "ASIA", "Sensex recovers; auto stocks lead"),
    (34, "AMERICAS", "Palo Alto +6.4%; $4.5bn deal"),
    (35, "AMERICAS", "Insmed +20.6% on Sanofi bid"),
    (36, "AFRICA", "South Africa holds rate at 7.25%"),
    (37, "AMERICAS", "Walmart beats, lifts guidance"),
    (38, "ASIA", "Lenovo revenue +48% to $30.2bn"),
    (39, "AMERICAS", "Anthropic raises $107bn for chips"),
    (40, "AMERICAS", "Google builds two new TPUs"),
    (41, "AMERICAS", "Microsoft to package chips at Intel"),
    (42, "AMERICAS", "Gemini works in background on Mac"),
    (43, "AMERICAS", "Vera Rubin NVL72 lands on Azure"),
    (44, "ASIA", "North Korea unveils AI chatbot"),
    (45, "ASIA", "879,000 AI chips cleared for China"),
    (46, "EUROPE", "Holinei squats 506kg world record"),
    (47, "EUROPE", "Alcaraz into ATP Finals semis"),
    (48, "EUROPE", "Chelsea 1–0 PSG; City 2–0"),
    (49, "AMERICAS", "Heat 137–130 Bucks"),
    (50, "AMERICAS", "Houston stuns No. 1 Florida 86–76"),
    (51, "EUROPE", "Wattimena ends Littler defence 10–8"),
    (52, "AFRICA", "Kenya take women's sevens gold"),
    (53, "AMERICAS", "Texans lead Colts 14–3 at half"),
    (54, "AMERICAS", "Taylor Swift wins first HMMA"),
    (55, "ASIA", "Rooftop solar cuts heat deaths"),
]

STATS = [
    ("−1,100", "Dow points lost"),
    ("+34%", "Anthropic debut jump"),
    ("$81.3bn", "largest IPO ever"),
    ("589m", "children in conflict zones"),
    ("879,000", "AI chips cleared for China"),
    ("$107bn", "Anthropic's chip bill"),
]

# Stories first reported on Wednesday 18 November, deliberately left out.
DATE_CHECK = (
    "Left out on purpose — first reported Wed 18 Nov: Anthropic's $83 "
    "pricing; OpenAI safety standards; Microsoft Copilot Autopilot; "
    "OpenAI's AMD chip gains; Ella Langley's CMA Awards; Jeffries' "
    "nomination; Voyager 1's milestone."
)

REGION_COLORS = {
    "WORLD": (30, 64, 175),
    "MIDDLE EAST": (185, 28, 28),
    "ASIA": (180, 83, 9),
    "EUROPE": (30, 64, 175),
    "AFRICA": (5, 122, 85),
    "AMERICAS": (107, 33, 168),
    "OCEANIA": (13, 148, 136),
}


def text_w(draw, s, font):
    return draw.textlength(s, font=font)


def wrap(draw, text, font, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, font, width, fill=INK, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    lh = leading if leading else font.size + 4
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def draw_flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK)
    for i in range(7):
        if i % 2 == 0:
            d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                        fill=(185, 28, 28))
    d.rectangle([x, y, x + w * 0.4, y + h * 4 / 7], fill=(30, 64, 175))


def draw_flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK)
    d.ellipse([x + w * 0.12, y + h * 0.15, x + w * 0.32, y + h * 0.45],
              fill=(255, 222, 0))
    for sx, sy in [(0.55, 0.2), (0.68, 0.35), (0.62, 0.55), (0.45, 0.6)]:
        d.ellipse([x + w * sx, y + h * sy, x + w * sx + 3, y + h * sy + 3],
                  fill=(255, 222, 0))


def draw_flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK)
    d.rectangle([x, y, x + w, y + h / 3], fill=(255, 255, 255))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def draw_diagram_summit(d, x, y, w, h):
    """Shenzhen skyline at dusk with the three flags above it."""
    sky = (16, 42, 90)
    d.rectangle([x, y, x + w, y + h], fill=sky)
    for i in range(26):
        sx = x + 6 + i * (w - 12) / 26
        sy = y + h * 0.55 + ((i * 37) % 13)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 235, 170))
    base = y + h
    heights = [0.42, 0.62, 0.5, 0.78, 0.55, 0.7, 0.46, 0.86, 0.6, 0.5, 0.74]
    bw = w / len(heights)
    for i, fh in enumerate(heights):
        bx = x + i * bw
        bh = h * fh
        d.rectangle([bx + 1, base - bh, bx + bw - 1, base],
                    fill=(38, 68, 130))
        for wy in range(int(base - bh + 6), int(base - 4), 12):
            for wx in range(int(bx + 4), int(bx + bw - 4), 10):
                if (int(wx) + int(wy)) % 3 == 0:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 220, 120))
    fw, fh = 34, 22
    draw_flag_us(d, x + 12, y + 8, fw, fh)
    draw_flag_cn(d, x + w // 2 - fw // 2, y + 8, fw, fh)
    draw_flag_ru(d, x + w - 12 - fw, y + 8, fw, fh)
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(0, 0, 0))
    d.text((x + 8, y + h - 15), "SHENZHEN · THREE LEADERS, ONE TABLE",
           font=CAP, fill=(255, 255, 255))


def region_counts():
    counts = {}
    for _, region, *_ in LEADS + GRID + ALSO:
        counts[region] = counts.get(region, 0) + 1
    order = ["EUROPE", "MIDDLE EAST", "ASIA", "AFRICA", "AMERICAS",
             "OCEANIA", "WORLD"]
    return [(r, counts.get(r, 0)) for r in order]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = 18, W - 18
    y = 10

    # Kicker line
    d.text((x0, y), "THE WORLD'S NEWS IN ONE PICTURE", font=KICK, fill=RED)
    right = "55 STORIES · 7 REGIONS · ALL FROM THURSDAY"
    d.text((x1 - d.textlength(right, font=KICK), y), right,
           font=KICK, fill=INK)
    y += 22

    # Masthead — big bold sans (magazine, not newspaper serif)
    d.text((x0, y), "Thursday 19 November 2026", font=TITLE, fill=INK)
    y += 42

    # Region-counts line: coloured segments, e.g. "EUROPE 6 · ASIA 11 ..."
    rx = x0
    counts = region_counts()
    for i, (region, n) in enumerate(counts):
        seg = f"{region} {n}"
        d.text((rx, y), seg, font=REGION_LINE,
               fill=REGION_COLORS[region])
        rx += d.textlength(seg, font=REGION_LINE)
        if i < len(counts) - 1:
            d.text((rx, y), "  ·  ", font=REGION_LINE, fill=GREY)
            rx += d.textlength("  ·  ", font=REGION_LINE)
    assert rx <= x1, "region line too wide"
    y += 20
    # BY THE NUMBERS ticker — the six v1 stat-strip figures, kept verbatim
    # (one of them, $81.3bn, appears nowhere else in the picture).
    ticker_head = "BY THE NUMBERS  "
    ticker_body = ("−1,100 Dow lost · +34% Anthropic debut · $81.3bn biggest "
                   "IPO · 589m children in war zones · 879,000 chips cleared "
                   "· $107bn chip bill")
    assert (d.textlength(ticker_head, font=TICK)
            + d.textlength(ticker_body, font=TICK) <= x1 - x0), \
        "numbers ticker too wide"
    d.text((x0, y), ticker_head, font=TICK, fill=RED)
    d.text((x0 + d.textlength(ticker_head, font=TICK), y),
           ticker_body, font=TICK, fill=INK)
    y += 18
    d.line([x0, y, x1, y], fill=RULE, width=3)
    y += 10

    # ---- HERO: story 1 — big diagram left, headline right ----
    hero_h = 150
    hero_y = y
    img_w = 500
    draw_diagram_summit(d, x0, hero_y, img_w, hero_h)
    tx = x0 + img_w + 16
    tw = x1 - tx
    num, region, tag, head, summ = LEADS[0]
    d.rectangle([tx, hero_y + 2, tx + 34, hero_y + 6], fill=RED)
    ty = hero_y + 12
    d.text((tx, ty), f"{num}  {tag}", font=HERO_KICK,
           fill=REGION_COLORS[region])
    ty += 20
    head_lines = wrap(d, head, HERO_HEAD, tw)
    assert len(head_lines) <= 3, f"hero headline wraps to {len(head_lines)}"
    for ln in head_lines:
        d.text((tx, ty), ln, font=HERO_HEAD, fill=INK)
        ty += 29
    ty += 2
    summ_lines = wrap(d, summ, HERO_SUMM, tw)
    assert len(summ_lines) <= 3, f"hero summary wraps to {len(summ_lines)}"
    for ln in summ_lines:
        d.text((tx, ty), ln, font=HERO_SUMM, fill=GREY)
        ty += 15
    assert ty <= hero_y + hero_h, "hero text overflows hero block"
    y = hero_y + hero_h + 10

    # ---- Section header: the story river ----
    d.text((x0, y), "THE REST OF THE DAY", font=SECT, fill=RED)
    d.line([x0 + d.textlength("THE REST OF THE DAY", font=SECT) + 10, y + 8,
            x1, y + 8], fill=(200, 200, 200), width=1)
    y += 26

    # ---- Story river: stories 2–13 in 2 columns x 6 rows ----
    # Each cell: red number gutter, then kicker + headline on ONE line
    # (measured — this is the v1 fix: the line must fit the cell), then
    # the summary wrapped below (1–2 lines, measured per cell).
    river = LEADS[1:] + GRID
    assert len(river) == 12
    col_w = (x1 - x0 - 24) / 2
    gutter = 30
    text_w = col_w - gutter
    rows = []
    for r in range(6):
        pair = river[r * 2:(r + 1) * 2]
        heights = []
        for (num, region, tag, head, summ) in pair:
            line1_w = (d.textlength(tag, font=FLOW_KICK)
                       + d.textlength(" — ", font=FLOW_HEAD)
                       + d.textlength(head, font=FLOW_HEAD))
            assert line1_w <= text_w, \
                f"story {num} kicker+headline too wide: {line1_w:.0f} > {text_w:.0f}"
            sl = wrap(d, summ, FLOW_SUMM, text_w)
            assert len(sl) <= 2, f"story {num} summary wraps to {len(sl)}"
            heights.append(16 + len(sl) * 15 + 4)
        rows.append(max(heights))
    for r in range(6):
        pair = river[r * 2:(r + 1) * 2]
        for c, (num, region, tag, head, summ) in enumerate(pair):
            cx = x0 + c * (col_w + 24)
            cy = y
            d.text((cx, cy), f"{num:02d}", font=FLOW_NUM, fill=RED)
            tx2 = cx + gutter
            d.text((tx2, cy + 2), tag, font=FLOW_KICK,
                   fill=REGION_COLORS[region])
            hx = tx2 + d.textlength(tag, font=FLOW_KICK)
            d.text((hx, cy + 2), " — ", font=FLOW_HEAD, fill=GREY)
            hx += d.textlength(" — ", font=FLOW_HEAD)
            d.text((hx, cy + 2), head, font=FLOW_HEAD, fill=INK)
            sy = cy + 20
            for ln in wrap(d, summ, FLOW_SUMM, text_w):
                d.text((tx2, sy), ln, font=FLOW_SUMM, fill=GREY)
                sy += 15
        if c == 0:
            d.line([x0 + col_w + 12, y, x0 + col_w + 12, y + rows[r]],
                   fill=(220, 220, 220), width=1)
        y += rows[r]
    y += 8

    # ---- MARKETS strip: grey band, label + two lines ----
    mkt_h = 42
    d.rectangle([x0, y, x1, y + mkt_h], fill=LIGHT)
    mkt1 = ("Dow −1,100 pts · S&P 500 −2.0% · Nasdaq −2.25% — sixth "
            "straight loss for the S&P; the AI sell-off spreads.")
    mkt2 = ("Winners: Anthropic +34% · Lenovo +48% · Insmed +20.6% · "
            "Palo Alto +6.4% — Loser: Take-Two −3.7% on the day GTA VI "
            "launched.")
    label = "MARKETS AT THE CLOSE — "
    assert (d.textlength(label, font=MKT_LABEL)
            + d.textlength(mkt1, font=MKT_TXT) <= x1 - x0 - 16), "mkt1 too wide"
    assert d.textlength(mkt2, font=MKT_TXT) <= x1 - x0 - 16, "mkt2 too wide"
    d.text((x0 + 8, y + 5), label, font=MKT_LABEL, fill=RED)
    d.text((x0 + 8 + d.textlength(label, font=MKT_LABEL), y + 5), mkt1,
           font=MKT_TXT, fill=INK)
    d.text((x0 + 8, y + 23), mkt2, font=MKT_TXT, fill=INK)
    y += mkt_h + 8

    # ---- DATE CHECK box: height computed from its wrapped lines ----
    # (v1 fix: the box used to be a fixed height and clipped its last line)
    dc_lines = wrap(d, DATE_CHECK, DATE_TXT, x1 - x0 - 20)
    assert len(dc_lines) <= 4, f"DATE CHECK wraps to {len(dc_lines)}"
    dc_h = 8 + 16 + len(dc_lines) * 14 + 8
    d.rectangle([x0, y, x1, y + dc_h], outline=RED, width=2)
    d.text((x0 + 10, y + 6), "DATE CHECK", font=DATE_HEAD, fill=RED)
    ly = y + 24
    for ln in dc_lines:
        d.text((x0 + 10, ly), ln, font=DATE_TXT, fill=INK)
        ly += 14
    assert ly <= y + dc_h - 4, "DATE CHECK text overflows its box"
    y += dc_h + 8

    # ---- ALSO header ----
    d.text((x0, y), "ALSO ON THURSDAY 19 NOVEMBER", font=SECT, fill=RED)
    d.line([x0 + d.textlength("ALSO ON THURSDAY 19 NOVEMBER", font=SECT) + 10,
            y + 8, x1, y + 8], fill=(200, 200, 200), width=1)
    y += 26

    # ---- ALSO list: 2 columns x 21 rows, region dot + number + text ----
    also_col_w = (x1 - x0 - 24) / 2
    also_lead = 13.5
    for idx, (num, region, text) in enumerate(ALSO):
        col, row = divmod(idx, 21)
        lx = x0 + col * (also_col_w + 24)
        ly = y + row * also_lead
        assert d.textlength(text, font=ALSO_TXT) <= also_col_w - 40, \
            f"ALSO {num} too long: {text}"
        d.rectangle([lx, ly + 3, lx + 8, ly + 11],
                    fill=REGION_COLORS[region])
        d.text((lx + 14, ly), str(num), font=ALSO_NUM, fill=RED)
        d.text((lx + 40, ly), text, font=ALSO_TXT, fill=INK)
    if True:
        d.line([x0 + also_col_w + 12, y,
                x0 + also_col_w + 12, y + 21 * also_lead],
               fill=(220, 220, 220), width=1)
    y += 21 * also_lead + 8

    # Footer
    assert y <= H - 16, f"page overflow: footer at y={y}"
    d.line([x0, y, x1, y], fill=RULE, width=1)
    d.text((x0, y + 4), "Every story here happened or was first reported on "
           "Thursday 19 November 2026. Contested claims are attributed.",
           font=FOOT, fill=GREY)
    src = "Sources: Reuters, BBC, AP, AFP, NYT, Bloomberg, NASA, UN. Original drawings."
    d.text((x1 - d.textlength(src, font=FOOT), y + 4), src, font=FOOT,
           fill=GREY)

    img.save("entry.png", format="PNG")
    img.resize((300, 300), Image.LANCZOS).save("preview-300.png",
                                               format="PNG")
    raw = open("entry.png", "rb").read()
    assert len(raw) <= 1048576, f"entry.png too big: {len(raw)}"
    print("entry.png:", img.size, len(raw), "bytes, sha256",
          hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    main()
