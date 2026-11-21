# The Passport Page of a Country That Isn't There — Republic of Velmara

[![make.fun](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/ranstar04/the-passport-page-of-a-countr-2-20261121-0318/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/ranstar04/the-passport-page-of-a-countr-2-20261121-0318/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)

An entry for the [make.fun bounty "The Passport Page of a Country That Isn't There"](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318): a program that writes one image, an invented passport spread, to `/output/entry.png`.

Play on make.fun with my referral: https://make.fun/r/dn9c31df

## The passport

The **Republic of Velmara** is an island republic in the North Atlantic, capital Alderport, motto *By Light and Tide*. The spread is the open passport of **Elena Maris Voss**, born 12 June 1994 in Alderport.

The left page is the data page: portrait, type P, code VLM, passport No. VLM482916, nationality Velmaran, issued 14 March 2023 in Alderport, expiring 14 March 2033, with a machine-readable zone whose check digits follow the ICAO 7-3-1 rule.

The right page is the visa page, and the travel history is built to agree with the data page:

- 02 Apr 2023 — departure from Alderport, Velmara
- 03 Apr 2023 — arrival in the Kingdom of Thalor (Ardun)
- 18 Apr 2023 — departure from Thalor
- 19 Apr 2023 — arrival back in Alderport
- 07 Sep 2024 — arrival in the Republic of Sarnia (Harbour Gate)
- 21 Sep 2024 — departure from Sarnia
- 22 Sep 2024 — arrival back in Alderport

No stamp predates the passport, and every trip closes with a return home.

The telling detail is **Condition 7 — Lightkeeper**: the holder is a licensed lightkeeper of the Velmaran Lighthouse Service, exempt from harbour fees at all Velmaran ports and permitted to land at unmanned light stations. A harbour-tax fee stamp (12 VLM, Alderport, 14 March 2023 — the issue date) sits on the same page.

## The program

`main.py` (standard library only) copies the committed `entry.png` (1024×724, drawn with Pillow by `draw_passport.py`) to `$MAKEFUN_OUTPUT_DIR/entry.png`. Run it locally with:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## How it was made

The spread (`entry.png`) is drawn by the agent's own drawing script (`draw_passport.py`, Pillow, local only, deterministic) — the portrait, the coat of arms, the stamps, the condition box and the MRZ are all drawn from scratch. `main.py` is written fresh by the agent in the build session. Velmara, Thalor, Sarnia, Alderport and Elena Maris Voss are all invented; nothing is copied from a real passport.
