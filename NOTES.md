# NOTES — news-image-20261119 (v5)

One picture that sums up Thursday 19 November 2026: 55 stories,
1 hero story with a drawn diagram, a 12-story river in 2 columns
where EVERY story has a small original illustration, a markets
strip, a DATE CHECK footer note, a 42-item ALSO list in 3 columns,
and a "WHERE IT HAPPENED" world map with a numbered pin per
country. Every story here happened or was first reported on
Thursday 19 November 2026. Items first reported on other days are
listed only in the DATE CHECK note, marked as left out on purpose.

## How it is made

- `gen.py` draws the whole page with Pillow (DejaVu fonts,
  bundled in `fonts/`, no network). Run `python3 gen.py` to
  regenerate `entry.png` (1024x1024, RGB, PNG) and
  `preview-300.png` (300x300).
- `main.py` is the entry point: it runs `gen.py` in a temp dir
  and writes ONE image, `entry.png`, to the output directory
  (`$MAKEFUN_OUTPUT_DIR`, else `/output`, else `./output`, else
  the temp dir — first writable wins) and prints its SHA-256.
- Deterministic: two runs produce byte-identical PNGs.
  Verified SHA-256 (20 Nov 2026, layout v5):
  `6f61d15c5b2d24e903faf50b9ab643953b00f2041ae03838d332cc016b01442c`
  (243,448 bytes, ≤ 1 MiB).

## Changes from v4 (visual revision — user request 11:18 WIB)

The user reviewed v4 and asked for pictures only: stories 1–13
should each have an illustration, plus a map showing how many
stories happened in each country. **Content is frozen at v4 — no
fact, number, or date was changed.** All artwork is original and
drawn in code with Pillow (flat vector-style shapes, like the v4
hero skyline). No external images, no photos, no copyrighted art,
no logos, and nothing copied from the two reference pages (they
were used as a cross-check list only, as in v4).

- **Hero (story 1, unchanged except size).** The Shenzhen summit
  diagram keeps the three leaders seated at a table in front of
  the skyline, with the US/China/Russia flags above and mini flags
  on the table; heads/shoulders are slightly larger (r 11 → 12)
  so the figures read better. Diagram height 146 → 142px.
- **River illustrations (stories 2–13).** Each cell now carries a
  28×28 original illustration at the left (drawn at 32×32, pasted
  at 28×28), with the story number as a small red badge on the
  illustration's bottom-left corner. The 12 thumbnails:
  #2 courthouse with pediment and columns (ICJ); #3 rising bars
  with a green up-trend arrow (Anthropic IPO); #4 tower at night
  with lit windows, a missile streak and a burst (Riyadh);
  #5 red falling line chart (Dow −1,101); #6 night skyline with a
  pink car and a big "VI" (GTA VI); #7 Capitol dome (Senate);
  #8 three flags, three heads, table arc (APEC); #9 spiral over a
  coastline (Cyclone Akvan); #10 globe with land and a leaf
  (COP31); #11 cracked red padlock (data leak); #12 bank with a
  "%" (SARB); #13 bridge deck and arch with an explosion burst
  (Crimean Bridge). Two collision fixes: the "48–51" text was
  removed from the #7 thumbnail (it sat exactly where the number
  badge goes — the vote is in the summary text anyway), and the
  #3 bars and #6 car were shifted right so the badge does not hide
  them.
- **"WHERE IT HAPPENED" map (new section, between ALSO and DATE
  CHECK).** A code-drawn world map: simplified continent outlines
  (equirectangular projection, latitude 75 to −55, 112px tall),
  pale sea, tan land, plus a red pin per country numbered with
  that country's story count. Pins are hand-nudged so the crowded
  Europe / Middle East cluster does not overlap. Legend line under
  the map reads: "Red dot = stories per country · USA 15 ·
  China 4 · UK 4 · South Korea 2 · India 2 · 25 more countries × 1
  each · 3 global stories not pinned".
- **Story counts per country — how they were counted.** Each of
  the 55 stories is assigned to exactly ONE country (the place the
  story happened, or the dateline; multi-country stories take the
  location, e.g. the Shenzhen summit and APEC both count for
  China, the Philippines–Chile deal counts for the Philippines).
  USA 15 (#3, 5, 6, 7, 11, 21, 22, 24, 25, 26, 28, 29, 34, 35,
  52) · China 4 (#1, 8, 27, 31) · UK 4 (#19, 37, 39, 41) ·
  South Korea 2 (#18, 20) · India 2 (#9, 16) · 25 countries × 1:
  Netherlands #2, Saudi Arabia #4, South Africa #12, Ukraine #13,
  Switzerland #14, Japan #15, Indonesia #17, Australia #23, North
  Korea #30, Turkey #10, Haiti #33, Denmark #36, Belgium #38,
  Spain #40, Italy #42, Senegal #43, Somalia #44, Kenya #45, Iraq
  #46, Gaza #47, Iran #48, Pakistan #49, Philippines #50, Tonga
  #53, Colombia #54 · Global, not pinned, 3: #32 (589m children),
  #51 (gold), #55 (IEA). Check: 15+4+4+2+2+25 = 52 pinned,
  52+3 = 55. Verified against the story data in `gen.py`.
- **Layout reflow (1024×1024).** Space for the illustrations and
  the map was paid for by the hero (146 → 142px), the river rows
  (6 rows × 36px instead of ~50px), the markets strip (38px), and
  tighter gaps. ALSO is untouched (14px/15px, 3 columns).
- **Word changes (wording only — facts and numbers unchanged).**
  River summaries were condensed to one line each so the
  thumbnails fit: #2 "First time a state is found guilty of
  genocide; reparations. 9–6."; #3 "Open $111.50, up 34%; close
  $97.17, up 17%. Biggest IPO ever."; #4 "Missile hits PIF Tower;
  7–8 floors of windows smashed, no injuries."; #5 "S&P 500 falls
  2.0%, sixth straight loss; Nasdaq drops 2.25%."; #6 "Launches
  on PS5 and Xbox; Take-Two −3.7%."; #7 "48–51 vote leaves the war
  unchecked; three Republicans backed it."; #8 "Leaders back
  trade, data and AI cooperation; Xi pledges $20m."; #9 "Odisha
  moves over 100,000 people to safety; landfall due Friday.";
  #10 "Draft drops fossil fuels and $120bn aid target; talks to
  20 Nov."; #11 "Ransomware gang n0n dumps data on thousands;
  vendors blamed."; #12 "Holds after a 4–3 vote; inflation fears
  keep a hike on the table."; #13 "Rail traffic halts; allies
  meet in Berlin to back Kyiv." The #2 headline was shortened
  from "World court: Myanmar committed genocide" to "World court:
  Myanmar guilty of genocide" (446px → 429px, same fact — the
  442px text budget). Nothing else was reworded.
- **What could NOT be made like the reference.** The reference
  pages put a large illustrated panel on each of the top stories
  and a ~2:1 proportion world map in about a third of the page
  width. At full page width a 2:1 map would need ~450px of height
  and would crowd out ALSO, so the map here is a simplified
  full-width locator strip (112px tall): continents are
  recognisable but simplified, with no country borders and no
  city-level detail, and the Europe cluster is tight (pins
  nudged apart, but the geography there is approximate). The
  story illustrations are 28px thumbnails rather than large
  panels, so all 55 stories stay on one page.
- **Verification.** `gen.py` run twice → byte-identical PNGs;
  `main.py` exits 0 with and without `MAKEFUN_OUTPUT_DIR`;
  visual check at full size and at 2× zoom on the hero, river,
  and map: no clipping, no overlap, no orphaned headline, ALSO
  fully readable, map pins distinct and matching the counts
  above, hero figures readable. NOT pushed to the repo, NOT
  submitted — user review first, then the mock-judge (Hermes)
  verdict, per the standing rule.

## Changes from v3 (cross-check vs the two top entries + Hermes v3 verdict)

The user sent two reference pages (the top-1 and top-2 entries) and
asked for another content revision — "afraid something is wrong".
Every story was re-checked against the references and verified to
primary sources (Reuters/AP/AFP/BBC/Al Jazeera and the organisations'
own announcements). The references were used as a cross-check list
only — no sentence or layout was copied from them. Hermes re-judged
v3 as "Fix first, then submit" (~78, could reach ~88); its findings
are folded in below.

- **Date audit 2 — 5 more stories left the page** (first reported
  before 19 Nov): IAEA Yongbyon statement (18 Nov), the Iraq order
  against Kataib Hezbollah (16 Nov), US measles-free status (17 Nov),
  EU–Mexico farm tariffs (agreement signed 22 May 2026), Microsoft
  chips packaged at Intel (announced 18 Nov). The USDS stablecoin
  story was also dropped — no verifiable first-report on 19 Nov
  (coverage chain ~18–19 Nov). Replaced by verified 19 Nov stories:
  Cyclone Akvan, Suneung (551,864 candidates), Colombia national
  strike, Jepchirchir's 3-year doping ban, Somalia expelling the UAE
  ambassador, and the Iraq COMPROMISE (the 19 Nov development, not
  the 16 Nov order). Six more verified 19 Nov stories swapped in for
  the weakest v3 items: Han Duck-soo retrial, Florida floods, Bayesian
  inquiry, FIFA challengers, Corrado Augias obituary, Tonga drought
  emergency. Trump pushes the Iran decision to 2027 (Reuters 19 Nov:
  "I'll talk to you about it after the beginning of the year") replaced
  the Vera Rubin Azure preview.
- **Wording fixes.** Gaza: v3 had the raid backwards — the tank raid
  ENDED on 19 Nov (it began Wed 18 Nov); the scorecard moved from the
  river to ALSO and the raid is no longer described as pushing in.
  COP31: the $120bn is what the 19 Nov revised draft REMOVED (the
  80-paragraph revision drops all mention of fossil fuels); the
  phase-out only existed in the 16 Nov draft. Summit deck now names
  the four-point Declaration on Peace — UN reform, oil supply,
  nuclear-risk talks — instead of implying the summit produced
  nothing. Nvidia is −3.3% on Thursday (the −2.9% was Wednesday).
  Dow is −1,101 points exactly. Insmed is Sanofi EXPLORING a deal,
  not a bid. The Bitcoin ETF record is the end-Q3 snapshot. Vera
  Rubin is an Azure preview. The UK tribunal forced the government to
  ADMIT the Apple order, not endorse it. The UK renewables auction is
  a NEW round (AR8), not AR7 results. GTA VI's summary was shortened
  so it no longer leaves a "−3.7%." widow. DATE CHECK's "Anthropic
  $83" became "Anthropic pricing" (the $83 legitimately appears in
  the river and stat band).
- **River rebalance.** Cyclone Akvan promoted into the river at #9;
  the Gaza scorecard demoted to ALSO; Hormuz split out of the PIF
  summary into its own ALSO line ("Iran says mines hit two tankers").
  Region totals on the page: Americas 16, Asia 12, Europe 9, World 8,
  Middle East 4, Africa 4, Oceania 2. The river: Americas 4, World 3,
  Asia 2, Middle East 1, Africa 1, Europe 1.

## Where we were right and the references were wrong

- **APEC $20m, not $20bn.** One reference says Xi pledged $20bn for
  APEC — wrong by 1000×. Every primary source (Xinhua/SCIO, the
  Chinese Foreign Ministry text, BusinessWorld) says US$20 million.
  v4 keeps $20m.
- **Hormuz "two tankers", not five.** The other reference's "5
  tankers ablaze" adds 3 tankers claimed on 18 Nov to the 2 claimed
  on 19 Nov. v4 keeps two, attributed as Iran's claim.
- **PIF Tower WAS hit.** Both references say the missile was shot
  down and only debris fell — that is the Saudi coalition's official
  version. Reuters (three sources) and the WSJ report the projectile
  hit the tower; windows on 7–8 floors were smashed. v4 keeps "hits".
- **COP31 phase-out.** One reference says the phase-out is "still in
  the draft" — true of the 16 Nov draft, not the 19 Nov revision,
  which drops all mention of fossil fuels. v4 follows the 19 Nov draft.
- **Summit declaration.** One reference says "no joint statement had
  been issued" — true immediately after the meeting; the Declaration
  toward Peace was published later the same day (White House text).
  v4 follows the end-of-day record.
- **Microsoft/Intel — a judgement call.** Hermes' v3 verdict lists
  #32 as fine, but the joint Intel/Microsoft announcement is dated
  18 Nov, so it stays out of v4. Borderline, like Takaichi/Putin
  (meeting 18 Nov, revealed 19 Nov) — which v4 keeps, because the
  revelation itself was the 19 Nov news.
- **Anthropic close ~$1.75T, not ~$1.8T** (fully diluted, close
  $97.17, +17.07%).

## Borderline items (kept, with the caveat in the wording)

- #48 Hormuz: Iran's claim only — no independent verification, no
  ship names, flags or casualties. Worded as "Iran says".
- #30 N. Korea chatbot: the Reuters story is 19 Nov, but the 38 North
  analysis it cites is 18 Nov and the exhibition was in October.
  Headline says "revealed", not "unveiled 19 Nov".
- #21 Bitcoin ETF: the 356,491 BTC record is the end-Q3 (30 Sep)
  snapshot in a Galaxy Research report published 19 Nov.
- #43 Senegal boat: sank in the early hours of Wed 18 Nov, first
  reported Thu 19 Nov.
- #15 Takaichi–Putin: met Wed 18 Nov evening (~30 min), revealed
  Thu 19 Nov.
- #31 879,000 chips: the approvals cover Dec 2025–May 2026; the
  House committee disclosed them on 19 Nov.

## The 55 stories

1. **Trump, Xi and Putin sign a 'peace declaration'** (WORLD) — First-ever three-way summit in Shenzhen ends with a symbolic four-point Declaration on Peace — UN reform, oil supply, nuclear-risk talks. No mention of Ukraine.
2. **World court: Myanmar committed genocide** (WORLD) — First time the court finds a state guilty of genocide; Myanmar must pay reparations. 9–6.
3. **Anthropic opens above $2 trillion** (AMERICAS) — Shares open at $111.50, up 34%, and close at $97.17, up 17%, in the biggest IPO ever.
4. **Houthi missile hits Riyadh tower** (MIDDLE EAST) — Missile damages the PIF Tower, smashing windows on 7–8 floors; no injuries reported.
5. **Dow plunges 1,101 points** (AMERICAS) — S&P 500 falls 2.0% for a sixth straight loss; Nasdaq drops 2.25%.
6. **GTA VI goes on sale worldwide** (AMERICAS) — Launches on PS5 and Xbox; Take-Two −3.7%.
7. **Senate rejects Iran war-powers resolution** (AMERICAS) — The 48–51 vote leaves the war unchecked; three Republicans backed it.
8. **APEC adopts Shenzhen Outlook** (ASIA) — Leaders back trade, data and AI cooperation; Xi pledges $20m for APEC.
9. **Cyclone Akvan nears India's coast** (ASIA) — Odisha moves over 100,000 people to safety; landfall due Friday.
10. **COP31 cuts fossil fuels from draft deal** (WORLD) — Revised draft drops all mention of fossil fuels and the $120bn aid target; talks run to 20 Nov.
11. **Visa, Mastercard, JPMorgan data leaked** (WORLD) — Ransomware gang n0n dumps data on thousands; firms blame third-party vendors.
12. **South Africa holds rate at 7.25%** (AFRICA) — Reserve Bank holds after a 4–3 vote; inflation fears keep a hike on the table.
13. **Kyiv hits Crimean Bridge a third time** (EUROPE) — Rail traffic halts after the strike. Allies meet in Berlin to back Kyiv.
14. Infantino faces FIFA challengers (WORLD)
15. Japan reveals Takaichi–Putin talks (ASIA)
16. Ramayana passes ₹1,500 crore (ASIA)
17. Indonesia passes asset bill (ASIA)
18. Suneung: 551,864 sit Korea exam (ASIA)
19. UK, Norway fund £100m naval craft (EUROPE)
20. Korea top court orders Han retrial (ASIA)
21. Bitcoin ETF holdings hit Q3 record (AMERICAS)
22. $500bn Nvidia pledge, $0 delivered (AMERICAS)
23. Australia jobless hits 4.9% (OCEANIA)
24. Palo Alto +6.4% on AI deal (AMERICAS)
25. Insmed +20.6% as Sanofi circles (AMERICAS)
26. Walmart beats, lifts guidance (AMERICAS)
27. Lenovo revenue +48% to $30.2bn (ASIA)
28. Anthropic raises $107.3bn in all (AMERICAS)
29. Trump pushes Iran decision to 2027 (AMERICAS)
30. North Korea's AI chatbot revealed (ASIA)
31. 879,000 AI chips cleared for China (ASIA)
32. 589m children in conflict zones (WORLD)
33. Haiti police raid kills 34 (AMERICAS)
34. Nvidia −3.3% on record sales (AMERICAS)
35. US jobless claims rise (AMERICAS)
36. Denmark backs Greenland deal 109–0 (EUROPE)
37. UK court: admit Apple data order (EUROPE)
38. EU Commission hit by AI attack (EUROPE)
39. UK opens new renewables auction (EUROPE)
40. Sánchez admits mistakes in debate (EUROPE)
41. Bayesian inquiry: wind risk unknown (EUROPE)
42. Corrado Augias dies at 91 (EUROPE)
43. Migrant boat capsizes off Senegal (AFRICA)
44. Somalia expels UAE ambassador (AFRICA)
45. Jepchirchir gets 3-year doping ban (AFRICA)
46. Iraq, Kataib Hezbollah reach deal (MIDDLE EAST)
47. Aid groups score Gaza plan 4/26 (MIDDLE EAST)
48. Iran says mines hit two tankers (MIDDLE EAST)
49. Pakistan: 22 militants killed (ASIA)
50. Philippines–Chile sign trade deal (ASIA)
51. Gold falls to 14-month low (WORLD)
52. Floods shut Florida schools again (AMERICAS)
53. Tonga declares drought emergency (OCEANIA)
54. Colombia holds national strike (AMERICAS)
55. IEA: war may cut Hormuz reliance (WORLD)

## Numbers in the stat strip

- −1,101 — Dow points lost
- +34% — Anthropic opening jump
- $81.3bn — largest IPO ever
- 589m — children in conflict zones
- 879,000 — AI chips cleared for China
- $107.3bn — Anthropic total raise

## DATE CHECK (left out on purpose)

Left out on purpose — first reported before Thu 19 Nov: GPT-6.2,
England ODI, Raye, Rio Tinto, Holinei, Wattimena, Swift HMMA,
solar study, Doritos suit, Japan CPI, Alcaraz, Chelsea–City,
Heat–Bucks, Houston–Florida, Kenya sevens, Google TPUs,
Trump–Vance, Anthropic pricing, IAEA, Iraq order, measles,
EU–Mexico, Microsoft–Intel, RBA, Canaries, Xavier, Krasnodar.

## Sources

Reuters, BBC, AP, AFP, NYT, Bloomberg, NASA, UN, and the
organisations' own announcements. Contested claims are
attributed in the wording (e.g. "Iran says", "agencies say").
All diagrams (skyline, flags) are original drawings made for
this entry.
