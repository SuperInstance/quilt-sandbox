"""Sandbox for canon lore: lore text containing Python → safe execution."""

import subprocess
import tempfile
import os
import re
import json
import textwrap
from typing import Dict


def extract_code(lore: str) -> str:
    """Extract Python code blocks from a canon lore markdown."""
    pattern = r"```python\n(.*?)\n```"
    matches = re.findall(pattern, lore, re.DOTALL)
    if not matches:
        return ""
    return "\n\n".join(matches)


def safe_exec(code: str, timeout: int = 5) -> Dict:
    """Execute code in subprocess; return JSON {ok, output, error}."""
    # User code is the body of `_canon_main()`. Function body is at column 8.
    indented_code = textwrap.indent(code, "        ")
    
    wrapper = '''import sys, json, io

_captured_stdout = io.StringIO()
_old_stdout = sys.stdout
sys.stdout = _captured_stdout

_result = {"ok": None, "output": "", "error": None, "type": None}

try:
    def _canon_main():
%s
        _result["ok"] = True
        _result["output"] = _captured_stdout.getvalue()
except Exception as e:
    _result["ok"] = False
    _result["error"] = str(e)
    _result["type"] = type(e).__name__
    _result["output"] = _captured_stdout.getvalue()

sys.stdout = _old_stdout

try:
    _canon_main()
except Exception as e:
    _result["ok"] = False
    _result["error"] = str(e)
    _result["type"] = type(e).__name__

print(json.dumps(_result))
''' % indented_code
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(wrapper)
        f.flush()
        tmp_path = f.name
    
    try:
        result = subprocess.run(
            ["python3", tmp_path],
            capture_output=True, text=True, timeout=timeout,
            env={"PATH": "/usr/bin:/usr/local/bin"},
        )
        stdout = result.stdout.strip()
        if not stdout:
            return {"_error": "no output", "stderr": result.stderr[:300]}
        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            return {"_error": "non-json output", "stdout": stdout[:200]}
    except subprocess.TimeoutExpired:
        return {"_error": "timeout"}
    finally:
        os.unlink(tmp_path)


def run_lore(lore: str, timeout: int = 5) -> Dict:
    """Extract and run code blocks from a canon lore."""
    code = extract_code(lore)
    if not code:
        return {"_error": "no python code blocks found"}
    return safe_exec(code, timeout=timeout)


if __name__ == "__main__":
    test_lore = """
```python
c = 299792458
G = 6.674e-11
print(f"c = {c:,} m/s")
```
"""
    result = run_lore(test_lore)
    print(f"Result: {result}")
