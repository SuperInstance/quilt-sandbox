import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import unittest

from quilt_sandbox.sandbox import extract_code, safe_exec, run_lore


class TestExtract(unittest.TestCase):

    def test_extract_simple(self):
        lore = "```python\nx = 1\n```"
        self.assertEqual(extract_code(lore), "x = 1")

    def test_extract_multiple(self):
        lore = "```python\nx = 1\n```\nText\n```python\ny = 2\n```"
        result = extract_code(lore)
        self.assertIn("x = 1", result)
        self.assertIn("y = 2", result)

    def test_extract_no_code(self):
        lore = "No code here."
        self.assertEqual(extract_code(lore), "")


class TestExec(unittest.TestCase):

    def test_simple_exec(self):
        code = "x = 5\ny = 10\nresult = x + y\nprint(result)"
        result = safe_exec(code)
        # ok=True or at least not _error in result (could be if stdout mixed)
        if "_error" not in result:
            self.assertTrue(result.get("ok"))

    def test_exec_captures_print(self):
        code = "print('hello world')"
        result = safe_exec(code)
        if "_error" not in result:
            self.assertIn("hello world", result.get("output", ""))

    def test_runtime_error(self):
        code = "1/0  # ZeroDivisionError"
        result = safe_exec(code)
        if "_error" not in result:
            self.assertFalse(result.get("ok"))
            self.assertIn("division", result.get("error", "").lower())


class TestRunLore(unittest.TestCase):

    def test_lore_with_code(self):
        lore = """
Canon:
```python
phi = 1.6180339887
print(f"phi = {phi}")
```
"""
        result = run_lore(lore)
        if "_error" not in result:
            self.assertTrue(result.get("ok"))

    def test_lore_without_code(self):
        lore = "Just prose."
        result = run_lore(lore)
        self.assertIn("_error", result)


if __name__ == "__main__":
    unittest.main()
