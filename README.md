# tv-autoskipper

Skips YouTube ads on a TV (Apple TV, smart TVs, consoles) as soon as the skip
button becomes available. It connects to the YouTube app the same way the phone
app does with "Link with TV code".

## Install

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

## Use

1. On the TV: YouTube > Settings > Link with TV code.
2. Pair once:
   ```bash
   .venv/bin/tv-autoskipper pair <code>
   ```
3. Leave it running:
   ```bash
   .venv/bin/tv-autoskipper run
   ```

Add `-v` before the command (`tv-autoskipper -v run`) to log every ad event.

## Test

```bash
.venv/bin/pytest
```
