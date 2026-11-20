# NOTES — news-image-20261119

One picture that sums up Thursday 19 November 2026: 55 stories,
1 hero story with a drawn diagram, a 12-story river in 2 columns,
a markets strip, a DATE CHECK box, and a 42-item ALSO list in
2 columns. Every story here happened or was first reported on
Thursday 19 November 2026. Items that were first reported on
Wednesday 18 November are listed only in the DATE CHECK box,
marked as left out on purpose.

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
  Verified SHA-256 (20 Nov 2026, layout v2):
  `db8f11a20e7f5c62597f253fe4b77c034025aa611805bc9e518598ecac3ab190`

## The 55 stories

1. **Trump, Xi and Putin sign a 'peace declaration'** (WORLD) — First-ever three-way summit in Shenzhen ends with a pledge against nuclear war.
2. **World court: Myanmar committed genocide** (WORLD) — Myanmar's military acted with genocidal intent against the Rohingya. 9–6.
3. **Anthropic debuts above $2 trillion** (AMERICAS) — Shares open at $111.50, up 34% on the $83 price, in the biggest IPO ever.
4. **Houthi missile hits Riyadh tower** (MIDDLE EAST) — Houthis strike the PIF Tower; Tehran hits ships in Hormuz and a US base.
5. **Dow plunges 1,100 points** (AMERICAS) — S&P 500 falls 2.0% for a sixth straight loss; Nasdaq drops 2.25%.
6. **Aid groups score Gaza plan 4 out of 26** (MIDDLE EAST) — Five agencies say the peace plan is falling short; new evacuation orders.
7. **Kyiv hits Crimean Bridge a third time** (EUROPE) — Rail traffic halts after the strike; Macron urges NATO membership talks.
8. **GTA VI goes on sale worldwide** (AMERICAS) — Rockstar's blockbuster launches on PlayStation 5 and Xbox; Take-Two −3.7%.
9. **589m children lived in war zones** (WORLD) — Save the Children counts 23.4% of children near recorded violence in 2025.
10. **COP31 cuts fossil fuels from draft deal** (WORLD) — Outcry in Antalya as the draft deal drops fossil fuels; talks run to 20 Nov.
11. **OpenAI ships GPT-6.2 Astra and Sol** (AMERICAS) — New models land as Nvidia stops selling H200 chips in China.
12. **Senate rejects Iran war-powers bill** (AMERICAS) — The 51–48 vote leaves the war unchecked; three Republicans backed it.
13. **England win ODI series in Hobart** (OCEANIA) — Duckett's 133 seals a 97-run win over Australia; the series ends 2–1.
14. Trump: "see what happens" on Iran (AMERICAS)
15. Trump blames Vance, NYT reports (AMERICAS)
16. Takaichi, Putin agree to keep talking (ASIA)
17. Rio Tinto pledges $250m mine fund (OCEANIA)
18. APEC adopts trade, data, AI outlook (ASIA)
19. Ramayana passes ₹1,500 crore (ASIA)
20. Indonesia passes asset bill (ASIA)
21. Raye leads Grammy nods with 11 (AMERICAS)
22. Typhoons intensify after heatwaves (ASIA)
23. UK, Norway fund £100m naval craft (EUROPE)
24. Rockstar names GTA VI voice cast (AMERICAS)
25. Students sue over Doritos AI alert (AMERICAS)
26. Visa, Mastercard, JPMorgan data leak (WORLD)
27. USDS stablecoin shrinks 35% (WORLD)
28. Bitcoin ETF holdings hit record (AMERICAS)
29. Japan inflation accelerates (ASIA)
30. Goolsbee open to bigger rate hikes (AMERICAS)
31. $500bn Nvidia pledge, $0 delivered (AMERICAS)
32. Australia jobless 4.9%, most since '21 (OCEANIA)
33. Sensex recovers; auto stocks lead (ASIA)
34. Palo Alto +6.4%; $4.5bn deal (AMERICAS)
35. Insmed +20.6% on Sanofi bid (AMERICAS)
36. South Africa holds rate at 7.25% (AFRICA)
37. Walmart beats, lifts guidance (AMERICAS)
38. Lenovo revenue +48% to $30.2bn (ASIA)
39. Anthropic raises $107bn for chips (AMERICAS)
40. Google builds two new TPUs (AMERICAS)
41. Microsoft to package chips at Intel (AMERICAS)
42. Gemini works in background on Mac (AMERICAS)
43. Vera Rubin NVL72 lands on Azure (AMERICAS)
44. North Korea unveils AI chatbot (ASIA)
45. 879,000 AI chips cleared for China (ASIA)
46. Holinei squats 506kg world record (EUROPE)
47. Alcaraz into ATP Finals semis (EUROPE)
48. Chelsea 1–0 PSG; City 2–0 (EUROPE)
49. Heat 137–130 Bucks (AMERICAS)
50. Houston stuns No. 1 Florida 86–76 (AMERICAS)
51. Wattimena ends Littler defence 10–8 (EUROPE)
52. Kenya take women's sevens gold (AFRICA)
53. Texans lead Colts 14–3 at half (AMERICAS)
54. Taylor Swift wins first HMMA (AMERICAS)
55. Rooftop solar cuts heat deaths (ASIA)

## Numbers in the stat strip

- −1,100 — Dow points lost
- +34% — Anthropic debut jump
- $81.3bn — largest IPO ever
- 589m — children in conflict zones
- 879,000 — AI chips cleared for China
- $107bn — Anthropic's chip bill

## DATE CHECK (left out on purpose)

Left out on purpose — first reported Wed 18 Nov: Anthropic's $83 pricing; OpenAI safety standards; Microsoft Copilot Autopilot; OpenAI's AMD chip gains; Ella Langley's CMA Awards; Jeffries' nomination; Voyager 1's milestone.

## Sources

Reuters, BBC, AP, AFP, NYT, Bloomberg, NASA, UN, and the
organisations' own announcements. Contested claims are
attributed in the wording (e.g. "NYT reports", "agencies say").
All diagrams (skyline, scales of justice, share-price chart) are
original drawings made for this entry.
