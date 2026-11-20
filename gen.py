# gen.py — draws entry.png for news-image-20261119 (Thursday 19 November 2026).
# PIL only, no network, fully deterministic. Run: python3 gen.py
# Writes entry.png (1024x1024, RGB) next to this file and preview-300.png.
#
# Layout v5 — magazine / editorial, v4 content + PICTURES (user request
# 20 Nov 2026, "berita 1 sampai 13 ada gambarnya ... peta juga di setiap
# negara ada berapa berita", following the top-1 "Precise Lemma" page):
#   slim kicker + big sans masthead, region-counts line (also the dot
#   legend), a two-row BY THE NUMBERS band, ONE hero story (story 1, big
#   drawn diagram left — now with the three leaders seated at a table —
#   headline right), a 12-story "story river" in 2 columns where EVERY
#   cell carries a small original code-drawn illustration on the left
#   (32x32, theme per story), a MARKETS strip, the 42-item ALSO list in
#   3 columns, a "WHERE IT HAPPENED" world map (code-drawn, red pins
#   numbered with the story count per country), a small grey DATE CHECK
#   footer note, footer. 55 stories total, content identical to v4
#   except the river summaries were shortened to ONE line each (same
#   facts and numbers — see NOTES.md) so the illustrations and the map
#   fit without touching the ALSO list.
#
# All pictures are original drawings made with PIL for this entry: no
# external images, no photos, no copyrighted artwork, no Rockstar logo.
# The reference page was used only as a layout idea (illustrations per
# story + a map); no sentence or picture was copied from it.
#
# v4 fixes vs v3 (cross-check vs the two top entries + web verification
# to primary sources, 20 Nov 2026 — see NOTES.md): date audit 2, Dow
# −1,101 exact, Nvidia −3.3% on Thu, Anthropic close $97.17 +17%,
# Gaza raid ENDED, COP31 $120bn removed by the 19 Nov draft, hero deck
# names the four-point Declaration, river rebalanced (Americas 16,
# Asia 12, Europe 9, World 8, Middle East 4, Africa 4, Oceania 2).
# Hermes v3 verdict (Fix first, ~78, could be ~88) folded in; v4 was
# sent to the user for review 20 Nov and its content was approved.
#
# v5 changes vs v4 (visual only, 20 Nov 2026):
#   HERO — diagram gains the three leaders seated at a table in front
#   of the skyline (heads, suits, ties, mini flags on the table); hero
#   height 190 -> 146, headline leading 33 -> 32, summary leading
#   15 -> 14 (text still fits, asserted).
#   RIVER — each cell gets a 32x32 original illustration drawn at the
#   left and pasted at 28x28 (number as a small red badge on the
#   illustration corner); text starts 40px in. Summaries shortened to
#   one line each (measured, all <= 442px at 12px); #02 headline
#   shortened to "World court: Myanmar guilty of genocide" (was
#   "committed genocide", 446px > 442 budget — same fact). Row height
#   is now max(36, text height).
#   MAP — new "WHERE IT HAPPENED" section between ALSO and DATE
#   CHECK: a code-drawn world map (simplified continent outlines,
#   equirectangular projection, 112px tall) with a red pin per country
#   numbered with that country's story count (USA 15, China 4, UK 4,
#   South Korea 2, India 2, 25 more x 1; 3 global stories not pinned).
#   Counts computed from the 55 stories in NOTES.md (see the
#   COUNTRY_COUNTS table and the per-story assignment there). Pins are
#   hand-nudged so the crowded Europe / Middle East cluster does not
#   overlap.
#   SPACE — paid for by the hero (48px), the one-line river summaries
#   (6 rows x 36px instead of ~50px), the markets strip (42 -> 38)
#   and tighter gaps; ALSO untouched (14px/15px, 3 columns).

import hashlib
import math
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
TITLE = _font("DejaVuSans-Bold.ttf", 26)
REGION_LINE = _font("DejaVuSans-Bold.ttf", 12)
STAT_NUM = _font("DejaVuSans-Bold.ttf", 17)
STAT_LBL = _font("DejaVuSans.ttf", 10)
TICK_HEAD = _font("DejaVuSans-Bold.ttf", 11)
HERO_KICK = _font("DejaVuSans-Bold.ttf", 13)
HERO_HEAD = _font("DejaVuSans-Bold.ttf", 28)
HERO_SUMM = _font("DejaVuSans.ttf", 12)
SECT = _font("DejaVuSans-Bold.ttf", 16)
FLOW_NUM = _font("DejaVuSans-Bold.ttf", 8)
FLOW_KICK = _font("DejaVuSans-Bold.ttf", 11)
FLOW_HEAD = _font("DejaVuSans-Bold.ttf", 13)
FLOW_SUMM = _font("DejaVuSans.ttf", 12)
MKT_LABEL = _font("DejaVuSans-Bold.ttf", 12)
MKT_TXT = _font("DejaVuSans.ttf", 12)
DATE_HEAD = _font("DejaVuSans-Bold.ttf", 11)
DATE_TXT = _font("DejaVuSans.ttf", 11)
ALSO_NUM = _font("DejaVuSans-Bold.ttf", 13)
ALSO_TXT = _font("DejaVuSans.ttf", 14)
FOOT = _font("DejaVuSans.ttf", 11)
CAP = _font("DejaVuSans.ttf", 10)
MAP_LEGEND = _font("DejaVuSans.ttf", 10)

# (number, region, tag, headline, summary) — all stories happened or were
# first reported on Thursday 19 November 2026; wording is the author's own.
# River summaries are ONE line each (measured <= 442px at 12px) so the
# illustrations fit; facts and numbers are unchanged from v4.
# The hero headline carries a manual line break (\n) so it never wraps
# with a one-word orphan.
LEADS = [
    (1, "WORLD", "WORLD · SUMMIT",
     "Trump, Xi and Putin sign\na 'peace declaration'",
     "First-ever three-way summit in Shenzhen ends with a symbolic "
     "four-point Declaration on Peace — UN reform, oil supply, "
     "nuclear-risk talks. No mention of Ukraine."),
    (2, "WORLD", "WORLD · JUSTICE",
     "World court: Myanmar guilty of genocide",
     "First time a state is found guilty of genocide; reparations. 9–6."),
    (3, "AMERICAS", "AMERICAS · MARKETS",
     "Anthropic opens above $2 trillion",
     "Open $111.50, up 34%; close $97.17, up 17%. Biggest IPO ever."),
]

GRID = [
    (4, "MIDDLE EAST", "MIDDLE EAST · IRAN WAR",
     "Houthi missile hits Riyadh tower",
     "Missile hits PIF Tower; 7–8 floors of windows smashed, no injuries."),
    (5, "AMERICAS", "AMERICAS · MARKETS",
     "Dow plunges 1,101 points",
     "S&P 500 falls 2.0%, sixth straight loss; Nasdaq drops 2.25%."),
    (6, "AMERICAS", "AMERICAS · GAMES",
     "GTA VI goes on sale worldwide",
     "Launches on PS5 and Xbox; Take-Two −3.7%."),
    (7, "AMERICAS", "AMERICAS · VOTE",
     "Senate rejects Iran war-powers resolution",
     "48–51 vote leaves the war unchecked; three Republicans backed it."),
    (8, "ASIA", "ASIA · APEC",
     "APEC adopts Shenzhen Outlook",
     "Leaders back trade, data and AI cooperation; Xi pledges $20m."),
    (9, "ASIA", "ASIA · STORM",
     "Cyclone Akvan nears India's coast",
     "Odisha moves over 100,000 people to safety; landfall due Friday."),
    (10, "WORLD", "WORLD · CLIMATE",
     "COP31 cuts fossil fuels from draft deal",
     "Draft drops fossil fuels and $120bn aid target; talks to 20 Nov."),
    (11, "WORLD", "WORLD · CYBER",
     "Visa, Mastercard, JPMorgan data leaked",
     "Ransomware gang n0n dumps data on thousands; vendors blamed."),
    (12, "AFRICA", "AFRICA · RATES",
     "South Africa holds rate at 7.25%",
     "Holds after a 4–3 vote; inflation fears keep a hike on the table."),
    (13, "EUROPE", "EUROPE · UKRAINE",
     "Kyiv hits Crimean Bridge a third time",
     "Rail traffic halts; allies meet in Berlin to back Kyiv."),
]

# ALSO list: one short line each (number + text), kept short enough to
# fit a single 14px line in a 3-column cell (asserted below).
ALSO = [
    (14, "WORLD", "Infantino faces FIFA challengers"),
    (15, "ASIA", "Japan reveals Takaichi–Putin talks"),
    (16, "ASIA", "Ramayana passes ₹1,500 crore"),
    (17, "ASIA", "Indonesia passes asset bill"),
    (18, "ASIA", "Suneung: 551,864 sit Korea exam"),
    (19, "EUROPE", "UK, Norway fund £100m naval craft"),
    (20, "ASIA", "Korea top court orders Han retrial"),
    (21, "AMERICAS", "Bitcoin ETF holdings hit Q3 record"),
    (22, "AMERICAS", "$500bn Nvidia pledge, $0 delivered"),
    (23, "OCEANIA", "Australia jobless hits 4.9%"),
    (24, "AMERICAS", "Palo Alto +6.4% on AI deal"),
    (25, "AMERICAS", "Insmed +20.6% as Sanofi circles"),
    (26, "AMERICAS", "Walmart beats, lifts guidance"),
    (27, "ASIA", "Lenovo revenue +48% to $30.2bn"),
    (28, "AMERICAS", "Anthropic raises $107.3bn in all"),
    (29, "AMERICAS", "Trump pushes Iran decision to 2027"),
    (30, "ASIA", "North Korea's AI chatbot revealed"),
    (31, "ASIA", "879,000 AI chips cleared for China"),
    (32, "WORLD", "589m children in conflict zones"),
    (33, "AMERICAS", "Haiti police raid kills 34"),
    (34, "AMERICAS", "Nvidia −3.3% on record sales"),
    (35, "AMERICAS", "US jobless claims rise"),
    (36, "EUROPE", "Denmark backs Greenland deal 109–0"),
    (37, "EUROPE", "UK court: admit Apple data order"),
    (38, "EUROPE", "EU Commission hit by AI attack"),
    (39, "EUROPE", "UK opens new renewables auction"),
    (40, "EUROPE", "Sánchez admits mistakes in debate"),
    (41, "EUROPE", "Bayesian inquiry: wind risk unknown"),
    (42, "EUROPE", "Corrado Augias dies at 91"),
    (43, "AFRICA", "Migrant boat capsizes off Senegal"),
    (44, "AFRICA", "Somalia expels UAE ambassador"),
    (45, "AFRICA", "Jepchirchir gets 3-year doping ban"),
    (46, "MIDDLE EAST", "Iraq, Kataib Hezbollah reach deal"),
    (47, "MIDDLE EAST", "Aid groups score Gaza plan 4/26"),
    (48, "MIDDLE EAST", "Iran says mines hit two tankers"),
    (49, "ASIA", "Pakistan: 22 militants killed"),
    (50, "ASIA", "Philippines–Chile sign trade deal"),
    (51, "WORLD", "Gold falls to 14-month low"),
    (52, "AMERICAS", "Floods shut Florida schools again"),
    (53, "OCEANIA", "Tonga declares drought emergency"),
    (54, "AMERICAS", "Colombia holds national strike"),
    (55, "WORLD", "IEA: war may cut Hormuz reliance"),
]

STATS = [
    ("−1,101", "Dow points lost"),
    ("+34%", "Anthropic opening jump"),
    ("$81.3bn", "largest IPO ever"),
    ("589m", "children in conflict zones"),
    ("879,000", "AI chips cleared for China"),
    ("$107.3bn", "Anthropic total raise"),
]

# Stories first reported before Thursday 19 November, deliberately left
# out. Shown as a small grey footer note (v2's red box drew more eye
# than the hero).
DATE_CHECK = (
    "GPT-6.2 · England ODI · Raye · Rio Tinto · Holinei · Wattimena · "
    "Swift HMMA · solar · Doritos · Japan CPI · Alcaraz · Chelsea · "
    "Heat · Houston · Kenya 7s · Google TPUs · Trump–Vance · Anthropic "
    "pricing · IAEA · Iraq order · measles · EU–Mexico · Microsoft–Intel · "
    "RBA · Canaries · Xavier · Krasnodar."
)

REGION_COLORS = {
    "WORLD": (190, 24, 93),
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
    """Shenzhen skyline at dusk with the three flags above it and the
    three leaders seated at a table in front of it (v5)."""
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
    # Three leaders seated at a table in front of the skyline.
    table_y0 = base - 40
    d.rectangle([x + 30, table_y0, x + w - 30, base - 16], fill=(96, 62, 38))
    d.rectangle([x + 30, table_y0, x + w - 30, table_y0 + 3],
                fill=(140, 95, 60))
    leaders = [(x + 105, (25, 35, 70), draw_flag_us, (60, 45, 35)),
               (x + w // 2, (40, 40, 45), draw_flag_cn, (40, 35, 30)),
               (x + w - 105, (25, 45, 80), draw_flag_ru, (215, 215, 210))]
    for cx, suit, flag_fn, hair in leaders:
        d.rectangle([cx - 28, table_y0 - 12, cx + 28, table_y0], fill=suit)
        d.ellipse([cx - 12, table_y0 - 34, cx + 12, table_y0 - 11],
                  fill=(232, 198, 168))
        d.pieslice([cx - 12, table_y0 - 34, cx + 12, table_y0 - 11],
                   180, 360, fill=hair)
        d.polygon([(cx - 3, table_y0 - 12), (cx + 3, table_y0 - 12),
                   (cx, table_y0 - 2)], fill=(185, 28, 28))
        flag_fn(d, cx - 7, table_y0 + 6, 14, 9)
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(0, 0, 0))
    d.text((x + 8, y + h - 15), "SHENZHEN · THREE LEADERS, ONE TABLE",
           font=CAP, fill=(255, 255, 255))


# ---- v5: original code-drawn illustrations for stories 2–13 ----
# Each thumbnail is a 32x32 flat drawing on its own background colour.
# No external images, no photos, no copied artwork.

THUMB = 32
THUMB_BG = (200, 200, 200)


def _thumb_bg(d, x, y, color):
    d.rectangle([x, y, x + THUMB, y + THUMB], fill=color, outline=THUMB_BG)


def thumb_court(d, x, y):
    """#2 ICJ — courthouse: pediment, columns, base (navy)."""
    _thumb_bg(d, x, y, (219, 228, 238))
    c = (43, 63, 110)
    d.polygon([(x + 4, y + 13), (x + 16, y + 4), (x + 28, y + 13)], fill=c)
    for cx in (x + 7, x + 14, x + 21):
        d.rectangle([cx, y + 14, cx + 3, y + 25], fill=c)
    d.rectangle([x + 4, y + 25, x + 28, y + 28], fill=c)


def thumb_bars(d, x, y):
    """#3 Anthropic IPO — rising bars + green up-trend arrow."""
    _thumb_bg(d, x, y, (13, 22, 48))
    for i, (bh, col) in enumerate([(8, (120, 140, 180)),
                                   (14, (60, 120, 220)),
                                   (20, (34, 197, 94))]):
        bx = x + 10 + i * 7
        d.rectangle([bx, y + 27 - bh, bx + 5, y + 27], fill=col)
    d.line([x + 9, y + 25, x + 27, y + 7], fill=(74, 222, 128), width=2)
    d.polygon([(x + 28, y + 5), (x + 22, y + 5), (x + 28, y + 11)],
              fill=(74, 222, 128))


def thumb_tower(d, x, y):
    """#4 Riyadh — tower at night, lit windows, missile streak + burst."""
    _thumb_bg(d, x, y, (10, 20, 50))
    d.rectangle([x + 13, y + 8, x + 19, y + 29], fill=(70, 100, 160))
    d.polygon([(x + 13, y + 8), (x + 16, y + 2), (x + 19, y + 8)],
              fill=(70, 100, 160))
    for wy in range(y + 11, y + 28, 5):
        d.rectangle([x + 14, wy, x + 15, wy + 2], fill=(255, 220, 120))
        d.rectangle([x + 17, wy, x + 18, wy + 2], fill=(255, 220, 120))
    d.line([x + 22, y + 3, x + 27, y + 9], fill=(255, 255, 255), width=2)
    d.ellipse([x + 24, y + 8, x + 29, y + 13], fill=(255, 200, 60))


def thumb_down(d, x, y):
    """#5 Dow — red falling line chart with a down arrow."""
    _thumb_bg(d, x, y, (255, 255, 255))
    d.line([x + 3, y + 27, x + 3, y + 5], fill=(180, 180, 180), width=1)
    d.line([x + 3, y + 27, x + 28, y + 27], fill=(180, 180, 180), width=1)
    d.line([x + 5, y + 8, x + 12, y + 13, x + 19, y + 12, x + 27, y + 22],
           fill=(185, 28, 28), width=2)
    d.polygon([(x + 27, y + 22), (x + 21, y + 21), (x + 27, y + 16)],
              fill=(185, 28, 28))


def thumb_gta(d, x, y):
    """#6 GTA VI — night skyline, pink car, big VI."""
    _thumb_bg(d, x, y, (45, 20, 75))
    for bx, bh in [(3, 10), (9, 16), (16, 12), (22, 18), (27, 9)]:
        d.rectangle([x + bx, y + 32 - bh, x + bx + 5, y + 32],
                    fill=(20, 10, 40))
    f = _font("DejaVuSans-Bold.ttf", 15)
    d.text((x + 8, y + 3), "VI", font=f, fill=(255, 255, 255))
    d.rectangle([x + 19, y + 26, x + 27, y + 29], fill=(255, 80, 160))


def thumb_dome(d, x, y):
    """#7 Senate — Capitol dome. (The 48–51 vote is in the summary
    text; putting it on the thumbnail too would collide with the
    story-number badge.)"""
    _thumb_bg(d, x, y, (235, 240, 245))
    c = (90, 110, 140)
    d.pieslice([x + 10, y + 2, x + 22, y + 12], 180, 360, fill=c)
    d.rectangle([x + 8, y + 11, x + 24, y + 13], fill=c)
    for cx in (x + 10, x + 15, x + 20):
        d.rectangle([cx, y + 14, cx + 2, y + 20], fill=c)
    d.rectangle([x + 7, y + 20, x + 25, y + 22], fill=c)


def thumb_apec(d, x, y):
    """#8 APEC — three flags, three heads, table arc."""
    _thumb_bg(d, x, y, (18, 55, 90))
    draw_flag_us(d, x + 3, y + 6, 8, 5)
    draw_flag_cn(d, x + 13, y + 6, 8, 5)
    d.rectangle([x + 22, y + 6, x + 30, y + 11], fill=(13, 148, 136),
                outline=INK)
    for cx in (x + 8, x + 16, x + 24):
        d.ellipse([cx - 3, y + 13, cx + 3, y + 19], fill=(235, 200, 170))
    d.arc([x + 2, y + 18, x + 30, y + 34], 180, 360,
          fill=(240, 200, 120), width=3)


def thumb_cyclone(d, x, y):
    """#9 Cyclone Akvan — spiral over a coastline."""
    _thumb_bg(d, x, y, (198, 224, 244))
    d.arc([x + 5, y + 4, x + 25, y + 24], 0, 300, fill=(255, 255, 255),
          width=2)
    d.arc([x + 9, y + 8, x + 21, y + 20], 120, 420, fill=(40, 90, 160),
          width=2)
    d.ellipse([x + 13, y + 12, x + 18, y + 17], fill=(40, 90, 160))
    d.polygon([(x + 20, y + 32), (x + 30, y + 32), (x + 28, y + 24),
               (x + 23, y + 26)], fill=(150, 130, 90))


def thumb_globe(d, x, y):
    """#10 COP31 — globe with land + a leaf."""
    _thumb_bg(d, x, y, (218, 238, 228))
    d.ellipse([x + 5, y + 4, x + 27, y + 26], fill=(40, 120, 200))
    d.ellipse([x + 9, y + 8, x + 15, y + 13], fill=(60, 180, 90))
    d.ellipse([x + 17, y + 16, x + 24, y + 22], fill=(60, 180, 90))
    d.polygon([(x + 22, y + 1), (x + 29, y + 1), (x + 26, y + 8)],
              fill=(30, 140, 70))


def thumb_lock(d, x, y):
    """#11 data leak — cracked padlock."""
    _thumb_bg(d, x, y, (28, 28, 40))
    d.arc([x + 10, y + 4, x + 22, y + 16], 180, 300,
          fill=(200, 200, 200), width=2)
    d.arc([x + 10, y + 4, x + 22, y + 16], 320, 360,
          fill=(200, 200, 200), width=2)
    d.rectangle([x + 8, y + 14, x + 24, y + 28], fill=(200, 60, 60))
    d.line([x + 13, y + 14, x + 16, y + 19, x + 13, y + 23, x + 17, y + 28],
           fill=(255, 255, 255), width=1)
    d.ellipse([x + 14, y + 18, x + 18, y + 22], fill=(255, 255, 255))


def thumb_bank(d, x, y):
    """#12 SARB — bank with a % on it."""
    _thumb_bg(d, x, y, (228, 240, 224))
    c = (5, 122, 85)
    d.polygon([(x + 4, y + 11), (x + 16, y + 3), (x + 28, y + 11)], fill=c)
    d.rectangle([x + 6, y + 12, x + 26, y + 25], fill=c)
    d.rectangle([x + 4, y + 25, x + 28, y + 28], fill=c)
    f = _font("DejaVuSans-Bold.ttf", 12)
    d.text((x + 11, y + 13), "%", font=f, fill=(255, 255, 255))


def thumb_bridge(d, x, y):
    """#13 Crimean Bridge — deck, arch, pillars, explosion burst."""
    _thumb_bg(d, x, y, (178, 208, 234))
    d.rectangle([x + 2, y + 20, x + 30, y + 23], fill=(90, 90, 90))
    d.arc([x + 6, y + 12, x + 26, y + 28], 180, 360, fill=(90, 90, 90),
          width=2)
    d.rectangle([x + 5, y + 20, x + 7, y + 29], fill=(90, 90, 90))
    d.rectangle([x + 25, y + 20, x + 27, y + 29], fill=(90, 90, 90))
    cx, cy = x + 16, y + 12
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 160, 0))
    for ang in range(0, 360, 60):
        ex = cx + 7 * math.cos(math.radians(ang))
        ey = cy + 7 * math.sin(math.radians(ang))
        d.line([cx, cy, ex, ey], fill=(255, 120, 0), width=1)


THUMBS = {2: thumb_court, 3: thumb_bars, 4: thumb_tower, 5: thumb_down,
          6: thumb_gta, 7: thumb_dome, 8: thumb_apec, 9: thumb_cyclone,
          10: thumb_globe, 11: thumb_lock, 12: thumb_bank,
          13: thumb_bridge}


# ---- v5: "WHERE IT HAPPENED" world map ----
# Simplified continent outlines (lon, lat), equirectangular projection:
# x = (lon+180)/360 * w, y = (75-lat)/130 * h (lat 75 at top, -55 at
# bottom; Antarctica is off the map). Shapes are deliberately coarse —
# a locator map, not an atlas.
MAP_H = 112
MAP_SEA = (214, 227, 241)
MAP_LAND = (198, 182, 142)
MAP_LINE = (172, 154, 118)

CONTINENTS = [
    [(-168, 66), (-155, 71), (-135, 70), (-120, 72), (-100, 73), (-85, 70),
     (-75, 72), (-65, 62), (-55, 52), (-60, 47), (-70, 44), (-75, 38),
     (-81, 32), (-84, 30), (-90, 21), (-95, 16), (-97, 16), (-105, 20),
     (-110, 24), (-117, 33), (-124, 42), (-125, 49), (-135, 58),
     (-150, 60), (-162, 58), (-168, 66)],
    [(-58, 64), (-45, 60), (-32, 68), (-22, 70), (-25, 76), (-40, 80),
     (-55, 78), (-60, 74), (-58, 64)],
    [(-80, 9), (-77, 4), (-75, 0), (-70, -3), (-60, 0), (-52, 3),
     (-50, 0), (-44, -3), (-35, -8), (-38, -15), (-40, -22), (-48, -27),
     (-55, -34), (-60, -38), (-66, -45), (-68, -52), (-71, -54),
     (-73, -48), (-73, -37), (-71, -30), (-70, -20), (-75, -15),
     (-80, -6), (-81, 0), (-80, 9)],
    [(-17, 15), (-16, 21), (-10, 31), (-5, 35), (0, 36), (10, 37),
     (20, 32), (30, 31), (34, 28), (37, 22), (43, 12), (48, 11), (51, 10),
     (46, 0), (41, -5), (40, -12), (36, -18), (33, -26), (28, -33),
     (20, -35), (16, -29), (14, -22), (12, -15), (13, -8), (12, -2),
     (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 12), (-17, 15)],
    [(-10, 36), (-9, 43), (-2, 48), (2, 51), (7, 54), (10, 57), (12, 55),
     (18, 56), (23, 58), (28, 60), (30, 62), (25, 68), (18, 70), (12, 68),
     (5, 60), (0, 54), (-5, 49), (-9, 43), (-10, 36)],
    [(30, 62), (35, 66), (45, 68), (60, 70), (75, 73), (90, 75), (105, 76),
     (120, 73), (135, 72), (150, 70), (160, 66), (170, 66), (178, 64),
     (170, 60), (162, 58), (158, 52), (150, 48), (142, 45), (140, 40),
     (135, 35), (130, 33), (127, 35), (124, 30), (121, 25), (115, 22),
     (110, 20), (108, 15), (105, 9), (103, 7), (100, 8), (97, 10),
     (94, 16), (91, 22), (88, 22), (85, 20), (80, 15), (77, 8), (74, 12),
     (70, 20), (66, 25), (61, 25), (57, 26), (53, 27), (50, 29), (48, 30),
     (44, 29), (40, 31), (36, 36), (33, 36), (30, 36), (28, 40), (30, 46),
     (30, 55), (30, 62)],
    [(113, -22), (114, -28), (115, -32), (118, -35), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
     (144, -38), (147, -39), (150, -37), (153, -32), (153, -27),
     (150, -23), (146, -19), (142, -14), (142, -11), (137, -12),
     (135, -12), (132, -12), (130, -13), (126, -14), (123, -17),
     (119, -20), (114, -21), (113, -22)],
]

# Small islands as (lon, lat, rx_deg, ry_deg) ellipses.
ISLANDS = [
    (102, 0, 6, 3), (113, -2, 5, 3), (120, -8, 4, 2), (131, -3, 5, 3),
    (140, -4, 6, 3), (139, 38, 3, 6), (122, 13, 2.5, 4), (141, -4, 7, 3),
    (172, -41, 3, 5), (-2, 54, 2.5, 4), (47, -19, 2, 5), (81, 7, 1.5, 2),
]

# Story count per country, counted from the 55 stories (see NOTES.md for
# the per-story assignment). (lon, lat, count, dx, dy) — dx/dy are manual
# nudges in px so the crowded Europe / Middle East pins do not overlap.
# 52 stories pinned in 30 countries; 3 are global and not pinned
# (#32 children, #51 gold, #55 IEA). 15+4+4+2+2+25x1 = 52; 52+3 = 55.
PINS = [
    (-98, 39, 15, 0, 0),      # USA
    (104, 35, 4, 0, 0),       # China
    (-2, 54, 4, -2, -2),      # UK
    (128, 36, 2, 5, -3),      # South Korea
    (127, 40, 1, -4, -7),     # North Korea
    (79, 21, 2, 0, 0),        # India
    (5, 52, 1, -1, -6),       # Netherlands (ICJ ruling)
    (4.5, 50.5, 1, -6, 5),    # Belgium (EU Commission)
    (10, 56, 1, 2, -5),       # Denmark
    (-4, 40, 1, -4, 5),       # Spain
    (8, 47, 1, 1, 6),         # Switzerland (FIFA)
    (12.5, 42, 1, 3, 8),      # Italy
    (35, 39, 1, 0, 2),        # Turkey (COP31)
    (32, 49, 1, -1, -4),      # Ukraine
    (44, 33, 1, -2, -6),      # Iraq
    (53, 32, 1, 0, 0),        # Iran
    (34.5, 31.5, 1, 10, 7),   # Gaza
    (45, 25, 1, -3, 7),       # Saudi Arabia
    (-16, 14, 1, 0, 0),       # Senegal
    (46, 6, 1, 8, 3),         # Somalia
    (38, 0, 1, 0, 0),         # Kenya
    (25, -29, 1, 0, 0),       # South Africa
    (138, 37, 1, 0, 0),       # Japan
    (114, -2, 1, 0, 0),       # Indonesia
    (122, 13, 1, 0, 0),       # Philippines
    (134, -25, 1, 0, 0),      # Australia
    (-175, -21, 1, 0, 0),     # Tonga
    (-73, 19, 1, 2, -3),      # Haiti
    (-74, 4, 1, -2, 1),       # Colombia
    (67, 30, 1, 0, 0),        # Pakistan
]

MAP_LEGEND_TXT = ("Red dot = stories per country · USA 15 · China 4 · "
                  "UK 4 · South Korea 2 · India 2 · 25 more countries × 1 "
                  "each · 3 global stories not pinned")


def draw_map(d, x, y, w, h):
    """Draw the world map with per-country story-count pins."""
    d.rectangle([x, y, x + w, y + h], fill=MAP_SEA)

    def P(lon, lat):
        return (x + (lon + 180) / 360 * w, y + (75 - lat) / 130 * h)

    for poly in CONTINENTS:
        pts = [P(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=MAP_LAND, outline=MAP_LINE)
    for lon, lat, rx, ry in ISLANDS:
        cx, cy = P(lon, lat)
        sx = rx / 360 * w
        sy = ry / 130 * h
        d.ellipse([cx - sx, cy - sy, cx + sx, cy + sy], fill=MAP_LAND,
                  outline=MAP_LINE)
    pin_font = _font("DejaVuSans-Bold.ttf", 7)
    for lon, lat, count, dx, dy in PINS:
        px, py = P(lon, lat)
        px += dx
        py += dy
        r = 9 if count >= 10 else 6
        assert x + r <= px <= x + w - r, f"pin x out of map: {px}"
        assert y + r <= py <= y + h - r, f"pin y out of map: {py}"
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=1)
        s = str(count)
        tw = d.textlength(s, font=pin_font)
        d.text((px - tw / 2, py - 5), s, font=pin_font, fill=(255, 255, 255))


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
    y += 20

    # Masthead — 26px bold sans (v3: was 32px, louder than the hero)
    d.text((x0, y), "Thursday 19 November 2026", font=TITLE, fill=INK)
    y += 32

    # Region-counts line: coloured segments, e.g. "EUROPE 6 · ASIA 11 ..."
    # This line doubles as the legend for the ALSO region dots.
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
    y += 18

    # BY THE NUMBERS band — two rows of three stats; big red numbers,
    # small grey labels. (v3: was one 11px line; the figures did not pop.)
    head = "BY THE NUMBERS  "
    d.text((x0, y), head, font=TICK_HEAD, fill=RED)
    hx = x0 + d.textlength(head, font=TICK_HEAD)
    row_gap = 24
    for row in range(2):
        stats = STATS[row * 3:(row + 1) * 3]
        sx = hx if row == 0 else x0
        for num, lbl in stats:
            nw = d.textlength(num, font=STAT_NUM)
            lw = d.textlength(lbl, font=STAT_LBL)
            assert sx + nw + 6 + lw <= x1, f"stat row {row} too wide"
            d.text((sx, y), num, font=STAT_NUM, fill=RED)
            d.text((sx + nw + 6, y + 5), lbl, font=STAT_LBL, fill=GREY)
            sx += nw + 6 + lw + row_gap
        y += 21
    y += 2
    d.line([x0, y, x1, y], fill=RULE, width=3)
    y += 8

    # ---- HERO: story 1 — big diagram left, headline right ----
    # v5: diagram 142 tall (was 190); headline leading 32, summary 14.
    hero_h = 142
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
    # Manual line break (in the data): never wrap with a one-word orphan.
    head_lines = []
    for part in head.split("\n"):
        part_lines = wrap(d, part, HERO_HEAD, tw)
        assert len(part_lines) == 1, \
            f"hero headline part wraps: {part!r} -> {part_lines}"
        head_lines.append(part_lines[0])
    assert len(head_lines) <= 3, f"hero headline wraps to {len(head_lines)}"
    for ln in head_lines:
        d.text((tx, ty), ln, font=HERO_HEAD, fill=INK)
        ty += 32
    ty += 2
    summ_lines = wrap(d, summ, HERO_SUMM, tw)
    assert len(summ_lines) <= 3, f"hero summary wraps to {len(summ_lines)}"
    for ln in summ_lines:
        d.text((tx, ty), ln, font=HERO_SUMM, fill=GREY)
        ty += 14
    assert ty <= hero_y + hero_h, "hero text overflows hero block"
    y = hero_y + hero_h + 8

    # ---- Section header: the story river ----
    d.text((x0, y), "THE REST OF THE DAY", font=SECT, fill=RED)
    d.line([x0 + d.textlength("THE REST OF THE DAY", font=SECT) + 10, y + 8,
            x1, y + 8], fill=(200, 200, 200), width=1)
    y += 24

    # ---- Story river: stories 2–13 in 2 columns x 6 rows ----
    # v5: each cell carries an original illustration drawn at 32x32
    # and pasted at 28x28 at the left (story number as a small red
    # badge on the illustration corner); text starts 40px in.
    # Summaries are ONE line each (measured).
    river = LEADS[1:] + GRID
    assert len(river) == 12
    col_w = (x1 - x0 - 24) / 2
    gutter = 40
    text_w = col_w - gutter
    thumb_disp = 28
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
            assert len(sl) == 1, \
                f"story {num} summary wraps to {len(sl)} (v5: must be 1)"
            heights.append(16 + len(sl) * 15 + 4)
        rows.append(max(max(heights), thumb_disp + 8))
    for r in range(6):
        pair = river[r * 2:(r + 1) * 2]
        for c, (num, region, tag, head, summ) in enumerate(pair):
            cx = x0 + c * (col_w + 24)
            cy = y
            thumb_img = Image.new("RGB", (THUMB, THUMB), PAPER)
            td = ImageDraw.Draw(thumb_img)
            THUMBS[num](td, 0, 0)
            thumb_img = thumb_img.resize((thumb_disp, thumb_disp),
                                         Image.LANCZOS)
            img.paste(thumb_img, (int(cx), int(cy)))
            # Story number as a small red badge on the thumbnail corner.
            badge = f"{num:02d}"
            bw = d.textlength(badge, font=FLOW_NUM)
            d.rectangle([cx - 1, cy + thumb_disp - 9,
                         cx + bw + 5, cy + thumb_disp + 1], fill=RED)
            d.text((cx + 2, cy + thumb_disp - 9), badge, font=FLOW_NUM,
                   fill=(255, 255, 255))
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
    y += 6

    # ---- MARKETS strip: grey band, label + two lines ----
    mkt_h = 38
    d.rectangle([x0, y, x1, y + mkt_h], fill=LIGHT)
    mkt1 = ("Dow −1,101 pts · S&P 500 −2.0% · Nasdaq −2.25% — sixth "
            "straight loss for the S&P; the AI sell-off spreads.")
    mkt2 = ("Winners: Anthropic +17% at close (opened +34%) · Lenovo +48% "
            "· Insmed +20.6% · Palo Alto +6.4% — Loser: Take-Two −3.7% "
            "as GTA VI launched.")
    label = "MARKETS AT THE CLOSE — "
    assert (d.textlength(label, font=MKT_LABEL)
            + d.textlength(mkt1, font=MKT_TXT) <= x1 - x0 - 16), "mkt1 too wide"
    assert d.textlength(mkt2, font=MKT_TXT) <= x1 - x0 - 16, "mkt2 too wide"
    d.text((x0 + 8, y + 4), label, font=MKT_LABEL, fill=INK)
    d.text((x0 + 8 + d.textlength(label, font=MKT_LABEL), y + 4), mkt1,
           font=MKT_TXT, fill=INK)
    d.text((x0 + 8, y + 20), mkt2, font=MKT_TXT, fill=INK)
    y += mkt_h + 6

    # ---- ALSO header ----
    d.text((x0, y), "ALSO ON THURSDAY 19 NOVEMBER", font=SECT, fill=RED)
    d.line([x0 + d.textlength("ALSO ON THURSDAY 19 NOVEMBER", font=SECT) + 10,
            y + 8, x1, y + 8], fill=(200, 200, 200), width=1)
    y += 24

    # ---- ALSO list: 3 columns x 14 rows, region dot + number + text ----
    # v3: was 2 columns x 21 rows at 13px/13.5px leading, whose lines
    # overlapped (13px type has a 17px ink box). Now 14px type on 15px
    # leading in 3 columns, using the width the 2-column list wasted.
    # v5 leaves this untouched.
    also_col_w = (x1 - x0 - 48) / 3
    also_lead = 15
    for idx, (num, region, text) in enumerate(ALSO):
        col, row = divmod(idx, 14)
        lx = x0 + col * (also_col_w + 24)
        ly = y + row * also_lead
        assert d.textlength(text, font=ALSO_TXT) <= also_col_w - 40, \
            f"ALSO {num} too long: {text}"
        d.rectangle([lx, ly + 3, lx + 8, ly + 11],
                    fill=REGION_COLORS[region])
        d.text((lx + 14, ly), str(num), font=ALSO_NUM, fill=RED)
        d.text((lx + 40, ly), text, font=ALSO_TXT, fill=INK)
    for c in (0, 1):
        d.line([x0 + (c + 1) * also_col_w + c * 24 + 12, y,
                x0 + (c + 1) * also_col_w + c * 24 + 12,
                y + 14 * also_lead],
               fill=(220, 220, 220), width=1)
    y += 14 * also_lead + 6

    # ---- WHERE IT HAPPENED: world map with per-country story counts ----
    # v5 (user request): a code-drawn world map; each red pin is numbered
    # with how many of the 55 stories happened in that country.
    d.text((x0, y), "WHERE IT HAPPENED", font=SECT, fill=RED)
    d.line([x0 + d.textlength("WHERE IT HAPPENED", font=SECT) + 10, y + 8,
            x1, y + 8], fill=(200, 200, 200), width=1)
    y += 24
    draw_map(d, x0, y, x1 - x0, MAP_H)
    y += MAP_H + 5
    assert d.textlength(MAP_LEGEND_TXT, font=MAP_LEGEND) <= x1 - x0, \
        "map legend too wide"
    d.text((x0, y), MAP_LEGEND_TXT, font=MAP_LEGEND, fill=GREY)
    y += 13

    # ---- DATE CHECK footer note (v3: small grey text, no red box) ----
    # Items first reported before Thu 19 Nov, deliberately left out.
    dc_head = "DATE CHECK — left out: "
    dc_w = d.textlength(dc_head, font=DATE_HEAD)
    dc_lines = wrap(d, DATE_CHECK, DATE_TXT, x1 - x0 - dc_w)
    assert len(dc_lines) <= 2, f"DATE CHECK wraps to {len(dc_lines)}"
    d.text((x0, y), dc_head, font=DATE_HEAD, fill=GREY)
    ly = y
    for i, ln in enumerate(dc_lines):
        lx = x0 + dc_w if i == 0 else x0
        d.text((lx, ly), ln, font=DATE_TXT, fill=GREY)
        ly += 13
    y = ly + 4

    # Footer
    assert y <= H - 16, f"page overflow: footer at y={y}"
    d.line([x0, y, x1, y], fill=RULE, width=1)
    d.text((x0, y + 4), "Every story happened or was first reported on "
           "Thursday 19 November 2026.", font=FOOT, fill=GREY)
    src = "Sources: Reuters, BBC, AP, AFP, NYT, Bloomberg, UN."
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
