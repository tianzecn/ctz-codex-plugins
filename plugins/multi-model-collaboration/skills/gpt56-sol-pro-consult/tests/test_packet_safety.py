#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_packet_safety.py"
SPEC = importlib.util.spec_from_file_location("gpt56_packet_safety", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PacketSafetyTests(unittest.TestCase):
    def test_allows_packet_without_credentials(self) -> None:
        result = MODULE.scan("CONTEXT_PACKET_V1\nNo executable credentials are included.")
        self.assertTrue(result["ok"])
        self.assertEqual(result["high_count"], 0)

    def test_blocks_common_token_assignment_containing_s(self) -> None:
        result = MODULE.scan("token=secretvalue12345")
        self.assertFalse(result["ok"])
        self.assertEqual(result["high_count"], 1)

    def test_blocks_cookie_header_containing_newline_sensitive_letters(self) -> None:
        result = MODULE.scan("Cookie: session=secretvalue12345; theme=dark")
        self.assertFalse(result["ok"])
        self.assertEqual(result["high_count"], 1)

    def test_warns_for_complete_absolute_user_path(self) -> None:
        result = MODULE.scan("Review /Users/example/project/src/server.py")
        self.assertTrue(result["ok"])
        self.assertEqual(result["warn_count"], 1)
        self.assertIn("server.py", result["findings"][0]["excerpt"])


if __name__ == "__main__":
    unittest.main()
