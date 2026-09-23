# quilt-sandbox

> **Canon that runs.**
> Verifies canon lore by extracting and executing its Python code blocks.

## TL;DR

```python
from quilt_sandbox import run_lore

lore = """
Some canon text.

```python
phi = 1.6180339887
print(f"phi = {phi}")
```
"""

result = run_lore(lore)
print(result)
```

## What this is

The Quilt canon is executable. When canon pieces contain Python code,
this sandbox verifies it runs. Canon that *runs* is canon that
*survives* — the math doesn't lie.

## Architecture

```
lore markdown → extract python blocks → safe_exec (subprocess)
                  ↓
                JSON result {"ok": True, "output": ...}
```

## License

MIT — Casey / SuperInstance, Sept 23, 2026
