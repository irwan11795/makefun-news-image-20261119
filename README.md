# Thursday 19 November 2026 — the world's news in one picture

[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261119-blue)](https://make.fun/c/news-image-20261119)
[![Stories](https://img.shields.io/badge/stories-55-red)](https://github.com/irwan11795/makefun-news-image-20261119)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/irwan11795/makefun-news-image-20261119/blob/main/LICENSE)

One 1024×1024 magazine-style page that sums up Thursday 19 November 2026:
**55 stories** — 1 hero story with a drawn diagram (the Shenzhen summit),
a 12-story river in 2 columns, a markets strip, a DATE CHECK box, and a
42-item ALSO list in 2 columns with region dots, all in large, readable
type. Every story happened or was first reported on 19 November 2026;
items from 18 November are listed only in the DATE CHECK box, marked as
left out on purpose.

![Thursday 19 November 2026 magazine page](entry.png)

## Run it

```sh
python3 main.py   # writes entry.png to $MAKEFUN_OUTPUT_DIR, /output, ./output or tmp
python3 gen.py    # regenerates entry.png + preview-300.png in place
```

Deterministic, stdlib-only (plus Pillow), no network. Two runs produce
byte-identical PNGs — verified SHA-256:
`db8f11a20e7f5c62597f253fe4b77c034025aa611805bc9e518598ecac3ab190`

See [NOTES.md](NOTES.md) for the full story list, sources, and method.
