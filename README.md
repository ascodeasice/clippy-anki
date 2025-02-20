# clippy-anki

A script that will turn the plover_clippy2 log into csv file.
Which can be added as an anki deck.

## how it works

It reads the clippy's org file, removing ANSI escape sequences, skipping phrases, and write word suggestions into `output.csv`.
Where the first field is the word and the second field is all suggested spellings separated with newlines.

## how to use

1. `python ./main.py ~/.config/plover/clippy_2.org`
2. Import the csv file in anki as the deck
