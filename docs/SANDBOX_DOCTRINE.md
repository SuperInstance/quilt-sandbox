# Sandbox Doctrine

The Quilt canon has a doctrine: **the canon runs**. When a piece of
canon contains Python code, the code must execute correctly. The
substrate walker canon is *executable*.

## Why sandbox?

The Quilt canon is supposed to be:
1. Linguistic (canon_writings)
2. Mathematical (the math can BE)
3. Executable (the math can GROW)

This sandbox is the gate between (2) and (3). A canon piece that
contains runnable code is canon only if the code actually runs.

## Architecture

```
lore markdown
    ↓ extract_code (regex: ```python ... ```)
Python code blocks
    ↓ safe_exec (subprocess with timeout + restricted env)
JSON result {"ok": True, "output": ...}
```

## Security

- Code runs in a subprocess with `timeout` (default 5s)
- Restricted env: only PATH=/usr/bin:/usr/local/bin
- Output captured as JSON
- Timeout returns {"_error": "timeout"}

## Layered navigation

| Layer | Where |
|---|---|
| **CANON.md** | what this is, in 24 lines |
| **README** | quick start |
| **Sandbox Doctrine** | docs/SANDBOX_DOCTRINE.md (this file) |
| **Source** | quilt_sandbox/sandbox.py |
| **Tests** | tests/test_sandbox.py |

## License

MIT — Casey / SuperInstance, Sept 23, 2026
