#!/bin/sh
i3lock --nofork --color=1a1b26ff \
  --inside-color=1a1b26ff --ring-color=7aa2f7ff \
  --insidever-color=1a1b26ff --ringver-color=bb9af7ff \
  --insidewrong-color=1a1b26ff --ringwrong-color=f7768eff \
  --line-uses-inside --separator-color=00000000 \
  --keyhl-color=9ece6aff --bshl-color=ff9e64ff \
  --time-color=c0caf5ff --date-color=565f89ff \
  --verif-color=c0caf5ff --wrong-color=f7768eff \
  --clock --indicator --time-str="%H:%M" --date-str="%a %d %b" \
  --radius=110 --ring-width=8
