# Template image action items

Findings from a 2026-06-26 review of `images/`. Filenames now encode the literal
client `Window Size` setting (Settings > Client > General), confirmed via
screenshot to be a real dropdown with options `1024x576`, `1280x720`,
`1600x900`, `1920x1080` — not the monitor's physical resolution.

## Confirmed clipped (need a fresh recapture)

- `images/find_match/1600x900.png` — right edge cuts off the "H" in "MATCH".
- `images/play_again/1600x900.png` — right edge cuts off the "N" in "AGAIN";
  no banner border visible at all (text fills the whole frame). Low priority
  since `1600x900` isn't the active client size.
- `images/accept/1920x1080.png` — top row is a flat plateau instead of a
  single apex point, meaning the chevron's top tip is sliced off. Still
  matches and clicks successfully in practice (confirmed live tonight), so
  this is a robustness nit, not a functional bug.
- `images/play_again/1920x1080_default.png` — left chevron point is sliced
  off. Secondary to the bigger issue below.

## Shipped fix

- Added `play_again/1920x1080_mayhem.png` and
  `misc/continue_1920x1080_mayhem.png`, fixing the auto-clicker silently
  failing to click "Play Again"/"Continue" during ARAM Mayhem matches
  (root cause: those two screens use Mayhem-specific button art that
  didn't match the default-skin templates, confirmed via live pixel
  testing — not a resolution or staleness issue).

## Known art mismatch (not a crop issue)

- `images/play_again/1920x1080_default.png` scores only ~0.24 against the
  current ARAM Mayhem-mode "Play Again" button even when pixel-aligned —
  the button art itself differs between default ARAM and Mayhem mode.
  `images/play_again/1920x1080_mayhem.png` was captured fresh tonight to
  cover the Mayhem variant; the `_default` file presumably still covers
  normal ARAM/SR, but that hasn't been verified live.
- `images/misc/continue.png` (gold border, default skin) vs
  `images/misc/continue_1920x1080_mayhem.png` (blue chevron, captured
  tonight) — same situation: two visually distinct "Continue" buttons for
  different modes/screens, not a stale/duplicate pair.

## Untested this session

- `accept/1600x900.png`, `find_match/1920x1080.png`, `misc/continue.png`,
  `misc/skip_stats.png` — visually clean, no clipping found, but not
  exercised against a live screen tonight (client stayed at 1920x1080 the
  whole time, and `continue.png`/`skip_stats.png` never came up while
  watching).

## Open question

- Does `play_again/1920x1080_default.png` (and `misc/continue.png`) still
  match correctly in a **non-Mayhem** ARAM/SR match? If Mayhem is the only
  mode in rotation right now, this can't be verified until that mode ends.
