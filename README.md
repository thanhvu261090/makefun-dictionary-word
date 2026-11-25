[![make.fun](https://make.fun/badge/u-puan-the-word-you-d-delete-from-the-dictionary-9e774bc2.svg)](https://make.fun/bounty/u-puan-the-word-you-d-delete-from-the-dictionary-9e774bc2)
[![Rank](https://make.fun/badge/u-puan-the-word-you-d-delete-from-the-dictionary-9e774bc2/thanhvu261090/makefun-dictionary-word/rank.svg)](https://make.fun/bounty/u-puan-the-word-you-d-delete-from-the-dictionary-9e774bc2)
[![Reward](https://make.fun/badge/u-puan-the-word-you-d-delete-from-the-dictionary-9e774bc2/thanhvu261090/makefun-dictionary-word/reward.svg)](https://make.fun/bounty/u-puan-the-word-you-d-delete-from-the-dictionary-9e774bc2)

# The Word You'd Delete From the Dictionary

Entry for the [make.fun bounty "The Word You'd Delete From the Dictionary"](https://make.fun/bounty/u-puan-the-word-you-d-delete-from-the-dictionary-9e774bc2): one word to erase from the dictionary forever, with nothing else attached.

## The entry

**irregardless**

It is the dictionary's own typo that got tenure: a double negative dressed up as a real word, listed only as "nonstandard", doing a job "regardless" already does perfectly. Delete it and nothing is lost — the language gets cleaner, and the dictionary stops apologising for it in the footnotes.

## How it works

`main.py` writes exactly that one word (12 characters) to `/output/entry.txt` and prints it. The entry is a fixed string, so every run produces byte-identical output.

Run it:

```sh
python3 main.py
```

Run the self-test (verifies the entry and every gate rule: 1–77 characters, exactly one word, no surrounding whitespace, valid UTF-8):

```sh
python3 main.py --self-test
```
