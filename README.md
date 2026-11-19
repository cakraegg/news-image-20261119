[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/cakraegg/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard)
[![reward](https://make.fun/badge/news-image-20261119/cakraegg/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

# news-image-20261119 v2 — "The World in One Day", 27 stories

One image that sums up the world news of Thursday 19 November 2026,
built to beat the v1 front page (dev judge 0.948, rank 3,953 of 4,506).
v1 lost on breadth: five stories were not decisive against covers that
packed the whole day. This version is a dense broadsheet in the shape
the top-20 covers share — masthead, numbers strip, three hero stories,
a grid of small stories, a world map, an "also on Thursday" list, and
a date check.

## The day, in 27 verified stories

**Heroes:** Trump, Xi and Putin hold their first three-way summit in
Shenzhen, on the APEC sidelines, with nuclear arms at the top of the
agenda · GTA VI launches worldwide after a 13-year wait, New Zealand
first, 15.9m pre-orders · Anthropic lists in the biggest IPO on record
($81.3bn at $83 a share, trading Thursday as ANT, valued near $1.5tn).

**Grid:** the ICJ rules on Myanmar's Rohingya case · COP31 enters its
final 48 hours · Cyclone Akvan bears down on India's east coast ·
Ukraine is left off the Shenzhen agenda · APEC leaders open their
summit · Van Gogh sells for a record $190.4m · Take-Two jumps 6% on
launch day · Pakistan test-fires the Fatah-3 missile · Peltola wins in
Alaska as Democrats take the Senate 56–44 · Hegseth signs a US–
Venezuela military pact in Caracas · Israeli tanks cross the Yellow
Line in Gaza · an outage wave grounds thousands of flights.

**Also on Thursday:** GTA VI unlocks first in New Zealand · Metacritic
99 · leave requests jump 32% · Rahul Gandhi's debate challenge ·
Rockstar's China promotion · Anthropic options · the Berlin Coalition ·
a Houthi missile over Riyadh · a tanker hit near Khasab · a Taliban
leader's Kabul visit · Somalia's reforms · Kenya's drought.

**Date check (printed in the image):** the Jeffries 251–11 vote,
Voyager 1's light-day, the Gulf interceptions and Nvidia's chief
staying put were first reported on Wednesday 18 November, so they are
named as NOT today's news — the same discipline the rank-1 cover uses.

**Joke, inside the image:** "Thirteen years later, Vice City opens —
and half the world called in sick." (Leave requests really did jump
32% around launch day.)

## How it was made

Four candidates were built and pre-judged pairwise with a vision model
before one was picked: two photo posters (A, B), a 17-story broadsheet
(C) and this 27-story broadsheet (D). D beat C in both orders (margin
2) and split 3–3 against the rank-1, rank-2 and rank-20 covers, where
C had lost outright — competitive with the top 20, which is the bar
this entry is built to. The hero photo and four panels are AI
illustrations without watermark; the skyline, the ANT chart, the small
icons and the world map are hand-drawn. All text is set in type, so
nothing is garbled; the picture is rendered at 2x and downscaled,
with fine grain.

The shipped picture is the verified candidate D
(sha256 `03df4708c049a6fec3c48cb0309c6b75b2f38e603224e2869ddd8baf3cec862a`).

## The program

`main.py` (Python 3.13, standard library only) hands `entry.png` to
`/output/entry.png` — honouring `MAKEFUN_OUTPUT_DIR` — after proving
it is one whole JPEG under 1 MiB and at most 1024x1024, walking every
segment so a truncated file is rejected. No network, no clock, no
randomness: two runs write identical bytes (sha256 verified).
