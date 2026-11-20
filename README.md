# News of 20 November 2026 — in one image

[![make.fun badge](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![make.fun rank](https://make.fun/badge/news-image-20261120/madara200599/news-of-2026-11-20/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![make.fun reward](https://make.fun/badge/news-image-20261120/madara200599/news-of-2026-11-20/reward.svg)](https://make.fun/bounty/news-image-20261120)

A make.fun bounty entry for **news-image-20261120**: a newspaper front page
that sums up the world news of Friday 20 November 2026 in a single image.

## What it shows

- **Lead:** Trump, Xi and Putin hold the first-ever three-way summit in
  Shenzhen, China, ending with a joint peace declaration (APEC).
- **Cyclone Akvan** makes landfall on India's east coast — 80,000 evacuated
  in Odisha.
- **The ICJ rules Myanmar committed genocide** against the Rohingya in 2017 —
  the first time the world court has found a state guilty of genocide.
- **Kyiv under fire:** Russian drones kill one and damage the Austrian and
  Dutch embassies and St Volodymyr's Cathedral.
- **Cricket:** Henry Nicholls' unbeaten 113 lifts New Zealand to 243/5 on day
  one of the first Test against India in Wellington.
- **Tech:** Anthropic is reportedly valued at $1.5 trillion.
- **Also today:** World Children's Day, APEC leaders in Shenzhen, Fiji's
  drought disaster declaration.

Every story was verified against news reported on 20 November 2026. The
image is drawn entirely in code — no photographs, no downloads.

## How it works

`artwork.py` draws the front page with Pillow (deterministic, offline) and
writes `entry.png` (1024×1024 PNG). `main.py` runs it and copies the image
to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).

```sh
python3 artwork.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Entered via referral code r7k9dyj1
